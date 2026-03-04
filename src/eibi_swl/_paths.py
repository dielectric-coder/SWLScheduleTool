"""XDG-aware path resolution for config and schedule data."""

import os
import shutil

_PKG_DIR = os.path.dirname(os.path.abspath(__file__))
_PKG_DATA = os.path.join(_PKG_DIR, "swl-schedules-data")


def resolve_data_dir():
    """Return the writable schedule-data directory.

    In dev/editable installs the package directory itself is writable,
    so we use swl-schedules-data/ next to the scripts.  For system or
    venv installs (site-packages is read-only) we fall back to
    ~/.local/share/eibi-swl/ and seed it from the bundled defaults.
    """
    if os.access(_PKG_DIR, os.W_OK):
        return _PKG_DATA

    xdg_data = os.environ.get("XDG_DATA_HOME", os.path.expanduser("~/.local/share"))
    user_data = os.path.join(xdg_data, "eibi-swl")

    if not os.path.isdir(user_data):
        os.makedirs(user_data, exist_ok=True)
        # Seed with bundled defaults
        if os.path.isdir(_PKG_DATA):
            for name in os.listdir(_PKG_DATA):
                src = os.path.join(_PKG_DATA, name)
                dst = os.path.join(user_data, name)
                if os.path.isfile(src) and not os.path.exists(dst):
                    shutil.copy2(src, dst)

    return user_data


def resolve_config():
    """Return the path to swlconfig.conf.

    In dev/editable installs, look next to the scripts.
    For system installs, use ~/.config/eibi-swl/swlconfig.conf,
    seeding from the bundled sample if needed.
    """
    local_conf = os.path.join(_PKG_DIR, "swlconfig.conf")
    if os.path.isfile(local_conf):
        return local_conf

    xdg_config = os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))
    user_conf_dir = os.path.join(xdg_config, "eibi-swl")
    user_conf = os.path.join(user_conf_dir, "swlconfig.conf")

    if not os.path.isfile(user_conf):
        os.makedirs(user_conf_dir, exist_ok=True)
        sample = os.path.join(_PKG_DIR, "swlconfig.conf.sample")
        if os.path.isfile(sample):
            shutil.copy2(sample, user_conf)

    return user_conf
