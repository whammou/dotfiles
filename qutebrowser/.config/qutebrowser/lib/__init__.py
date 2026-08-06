# lib package: pure helper modules for the qutebrowser config.
#
# Modules here are IMPORTED by the sourced config files (settings.py, keys.py,
# sites.py, tabcss.py) through regular import machinery, never config.source()d
# themselves. They must stay free of qutebrowser's injected globals (`c`,
# `config`), because those names only exist while a config file is being
# sourced. Pure constants/functions only.
