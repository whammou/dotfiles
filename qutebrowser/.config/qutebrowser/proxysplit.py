#!/usr/bin/env python3
"""proxysplit.py - per-destination SOCKS5 proxy for qutebrowser.

QtWebEngine has no per-site proxy support: QWebEngineProfile.setHttpProxy
does not exist in PyQt6 6.11, PAC is unimplemented on QtWebEngine, and the
--proxy-server/--proxy-pac-url CLI flags are ignored. The only working hook
is the application-wide QNetworkProxyFactory, which QtWebEngine queries with
an empty URL - so it can only ever return ONE global proxy. This script is
that global proxy: a SOCKS5 server on 127.0.0.1:1081 that forwards the dev
server through the hysteria tunnel (127.0.0.1:1080) and everything else
directly.

qutebrowser setting: c.content.proxy = "socks5://127.0.0.1:1081"
Started by qutebrowser-daemon (see ~/.local/bin/qutebrowser-daemon).
"""

import asyncio
import logging
import socket

LISTEN_HOST = "127.0.0.1"
LISTEN_PORT = 1081

# Destination only reachable through the hysteria SOCKS5 tunnel.
TUNNEL_HOST = "192.168.0.104"
TUNNEL_PORT = 5173
SOCKS_HOST = "127.0.0.1"
SOCKS_PORT = 1080

CONNECT_TIMEOUT = 10.0

_REPLY_OK = bytes([0x05, 0x00, 0x00, 0x01, 0, 0, 0, 0, 0, 0])
_REPLY_NOT_SUPPORTED = bytes([0x05, 0x07, 0x00, 0x01, 0, 0, 0, 0, 0, 0])
_REPLY_FAILURE = bytes([0x05, 0x01, 0x00, 0x01, 0, 0, 0, 0, 0, 0])

log = logging.getLogger("proxysplit")


def _is_tunnel(host: str, port: int) -> bool:
    return host == TUNNEL_HOST and port == TUNNEL_PORT


async def _socks5_connect(reader, writer, host, port) -> None:
    """Negotiate a SOCKS5 CONNECT to host:port through the tunnel."""
    writer.write(bytes([0x05, 0x01, 0x00]))  # version, 1 method, no-auth
    await writer.drain()
    resp = await reader.readexactly(2)
    if resp[0] != 0x05 or resp[1] != 0x00:
        raise ConnectionError(f"tunnel auth rejected: {resp!r}")
    if ":" in host:
        addr = bytes([0x04]) + socket.inet_pton(socket.AF_INET6, host)
    else:
        addr = bytes([0x01]) + socket.inet_aton(host)
    writer.write(bytes([0x05, 0x01, 0x00]) + addr + port.to_bytes(2, "big"))
    await writer.drain()
    resp = await reader.readexactly(4)
    if resp[1] != 0x00:
        raise ConnectionError(f"tunnel connect failed: rep={resp[1]}")
    atyp = resp[3]
    if atyp == 0x01:
        await reader.readexactly(6)
    elif atyp == 0x03:
        length = (await reader.readexactly(1))[0]
        await reader.readexactly(length + 2)
    elif atyp == 0x04:
        await reader.readexactly(18)
    else:
        raise ConnectionError(f"tunnel bad atyp: {atyp}")


async def _parse_request(header: bytes, reader):
    """Read the SOCKS5 request, returning (cmd, host, port)."""
    ver, cmd, _rsv, atyp = header
    if ver != 0x05:
        raise ConnectionError(f"bad version: {ver}")
    if atyp == 0x01:
        host = socket.inet_ntop(socket.AF_INET, await reader.readexactly(4))
    elif atyp == 0x03:
        length = (await reader.readexactly(1))[0]
        host = (await reader.readexactly(length)).decode("ascii", "replace")
    elif atyp == 0x04:
        host = socket.inet_ntop(socket.AF_INET6, await reader.readexactly(16))
    else:
        raise ConnectionError(f"bad atyp: {atyp}")
    port = int.from_bytes(await reader.readexactly(2), "big")
    return cmd, host, port


async def _relay(reader, writer, peer_reader, peer_writer) -> None:
    """Bidirectional copy; tear both down when either direction ends."""

    async def _pump(src, dst):
        try:
            while True:
                data = await src.read(65536)
                if not data:
                    break
                dst.write(data)
                await dst.drain()
        except (ConnectionError, asyncio.IncompleteReadError):
            pass
        finally:
            for w in (writer, peer_writer):
                try:
                    w.close()
                except Exception:
                    pass

    await asyncio.gather(
        _pump(reader, peer_writer),
        _pump(peer_reader, writer),
    )


async def _handle_client(reader, writer) -> None:
    peer = writer.get_extra_info("peername")
    try:
        greeting = await reader.readexactly(2)
        if greeting[0] != 0x05:
            raise ConnectionError(f"not a SOCKS5 greeting: {greeting!r}")
        nmethods = greeting[1]
        if nmethods:
            await reader.readexactly(nmethods)
        writer.write(bytes([0x05, 0x00]))  # no-auth
        await writer.drain()

        header = await reader.readexactly(4)
        cmd, host, port = await _parse_request(header, reader)
        if cmd != 0x01:  # CONNECT only; BIND/UDP ASSOCIATE unsupported
            writer.write(_REPLY_NOT_SUPPORTED)
            await writer.drain()
            return

        if _is_tunnel(host, port):
            tunnel_reader, tunnel_writer = await asyncio.wait_for(
                asyncio.open_connection(SOCKS_HOST, SOCKS_PORT), CONNECT_TIMEOUT
            )
            await _socks5_connect(tunnel_reader, tunnel_writer, TUNNEL_HOST, TUNNEL_PORT)
            log.info(
                "%s -> tunnel %s:%s via %s:%s",
                peer, TUNNEL_HOST, TUNNEL_PORT, SOCKS_HOST, SOCKS_PORT,
            )
            peer_reader, peer_writer = tunnel_reader, tunnel_writer
        else:
            peer_reader, peer_writer = await asyncio.wait_for(
                asyncio.open_connection(host, port), CONNECT_TIMEOUT
            )
            log.info("%s -> direct %s:%s", peer, host, port)

        writer.write(_REPLY_OK)
        await writer.drain()
        await _relay(reader, writer, peer_reader, peer_writer)
    except (ConnectionError, asyncio.IncompleteReadError, OSError) as exc:
        log.warning("client %s: %s", peer, exc)
        try:
            writer.write(_REPLY_FAILURE)
            await writer.drain()
        except Exception:
            pass
    except Exception:
        log.exception("client %s: unexpected error", peer)
    finally:
        try:
            writer.close()
        except Exception:
            pass


async def _main() -> None:
    server = await asyncio.start_server(_handle_client, LISTEN_HOST, LISTEN_PORT)
    log.info(
        "proxysplit listening on %s:%s (tunnel %s:%s -> %s:%s)",
        LISTEN_HOST, LISTEN_PORT, TUNNEL_HOST, TUNNEL_PORT, SOCKS_HOST, SOCKS_PORT,
    )
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s"
    )
    try:
        asyncio.run(_main())
    except KeyboardInterrupt:
        pass
