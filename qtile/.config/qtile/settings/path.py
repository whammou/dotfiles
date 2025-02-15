from os import path


qtile_path = path.join(path.expanduser('~'), ".config", "qtile")
script_path = path.join(qtile_path, "scripts")
wallpaper_path = path.join(path.expanduser('~'), ".wallpaper")


def run_script(script_name):
    return path.join(script_path, script_name)


def in_terminal(package, terminal="kitty", parameters=None):
    package_launch = "-e " + package

    if parameters == None:
        return " ".join([terminal, package_launch])
    else:
        return " ".join([terminal, parameters, package_launch])
