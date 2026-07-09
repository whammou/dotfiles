---
name: codegraph-explorer
description: "MUST USE for deep codebase exploration. Queries the pre-indexed codegraph knowledge graph — returns verbatim source, call paths, and blast radius in ONE call. Supersedes manual Read/Grep/Glob loops. Use for understanding module structure, symbol relationships, call flows, or editing with blast-radius awareness. Triggers: codegraph, explore architecture, find symbol, trace flow, understand module, map codebase, code analysis."
---

# Codegraph Explorer — MCP-Powered Codebase Intelligence

**NOTE:** `skill_mcp` and MCP-generated tools (`codegraph_codegraph_explore`) are only available to the **main orchestrator agent** (Sisyphus). Subagents do not inherit MCP access due to a platform-level scoping constraint. If you are a subagent, skip to [Subagents: Request from Orchestrator](#subagents-request-from-orchestrator).

---

## Main Agent: Using Codegraph Directly

Call `codegraph_codegraph_explore` with a natural-language query or symbol names:

```plaintext
codegraph_codegraph_explore(query="<natural language or symbol names>")
```

### Workflow

#### 1. Entry Point Discovery
```plaintext
codegraph_codegraph_explore(query="main entry point, plugin init, require structure, module loading")
```

#### 2. Symbol/Module Deep Dive
```plaintext
codegraph_codegraph_explore(query="<ModuleName> <FunctionName> — get source, callers, and callees")
```

#### 3. Flow Tracing
```plaintext
codegraph_codegraph_explore(query="How does <SymbolA> reach <SymbolB>? Trace the call path.")
```

#### 4. Blast Radius
```plaintext
codegraph_codegraph_explore(query="<SymbolName> — what depends on it, what it affects")
```

#### 5. Architecture Survey
```plaintext
codegraph_codegraph_explore(query="Architecture of <module path/> — key types, functions, and their relationships")
```

### Query Tips

| Goal | Query Style |
|------|-------------|
| **Find a symbol** | `<name>` — returns all matching definitions with source |
| **Understand a flow** | `<StartSymbol> <EndSymbol>` — surfaces the call path between them |
| **Blast radius** | `<Symbol> what depends on it` |
| **Architecture** | `Architecture of <area> — key modules, types, patterns` |
| **Bug investigation** | `<Symbol> how does <behavior> work — trace the logic` |

### Critical Rules

- **Do NOT re-verify codegraph results with grep/read.** Codegraph results come from a full AST parse. Re-checking is slower and wastes tokens.
- **Do NOT Read files that codegraph already returned source for.** The source is already in your context.
- **One call usually answers the whole question.** Don't over-query — call once with the full picture, then follow up only if needed.
- **After editing**, codegraph may lag ~1s behind. If the response shows a staleness banner, Read those specific files directly.
- **If no `.codegraph/` index exists**, run `codegraph init` in the project root to create one. If initialization succeeds, proceed with `codegraph_explore`. If init fails (e.g., unsupported project type, permission denied, toolchain missing), fall back to Read/Grep/Glob — the skill is useless without an index.

---

## Subagents: Request from Orchestrator

Since this subagent cannot directly call MCP tools, request codegraph data from the orchestrator:

> "I need codegraph data on `<symbol/module>`. Please run `codegraph_codegraph_explore` with query `'<your query>'` and pass me the results."

The orchestrator will run the query and inject the source + call paths into your context.
