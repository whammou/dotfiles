from os import path


qtile_path = path.join(path.expanduser("~"), ".config", "qtile")
script_path = path.join(qtile_path, "scripts")
qtile_service = path.join(qtile_path, "services")
wallpaper_path = path.join(path.expanduser("~"), ".wallpaper")


def run_script(script_name):
    return path.join(script_path, script_name)


def in_terminal(package, terminal="kitty", parameters=None, app_id=None):
    app_id_flag = f"--app-id={app_id} " if app_id else ""
    package_launch = "-e " + package

    if parameters is None:
        return " ".join([terminal, app_id_flag + package_launch])
    else:
        return " ".join([terminal, app_id_flag + parameters, package_launch])
