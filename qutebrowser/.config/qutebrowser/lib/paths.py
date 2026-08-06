# Paths shared between config modules.
#
# NOTE: This module must stay free of qutebrowser's injected globals (`c`,
# `config`): it is imported through Python's regular import machinery, where
# those names do not exist. Keep it pure constants only.
CSS_DIR = "~/.config/qutebrowser/css/"
