#!/usr/bin/env python3
"""Install the two launchers in this user's Linux application menu, offline."""
import os
from pathlib import Path
import shutil
import sys


def desktop_quote(value):
    # Desktop Entry Exec escaping, not shell escaping.
    return '"' + value.replace('\\', '\\\\\\\\').replace('"', '\\\\"').replace('`', '\\\\`').replace('$', '\\\\$').replace('%', '%%') + '"'


def main():
    if sys.platform != 'linux' or os.getuid() == 0:
        raise SystemExit('Lancez ce script dans la session Linux utilisateur, sans sudo.')
    source = Path(__file__).resolve().parent
    data = Path(os.environ.get('XDG_DATA_HOME', str(Path.home() / '.local/share')))
    target = data / 'koali-store'
    target.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source / 'third-party-store.py', target / 'third-party-store.py')
    applications = data / 'applications'
    applications.mkdir(parents=True, exist_ok=True)
    for name in ('koali-store.desktop', 'koali-essentials.desktop'):
        text = (source / name).read_text()
        text = text.replace('/usr/libexec/koa/third-party-store.py', desktop_quote(str(target / 'third-party-store.py')))
        (applications / name).write_text(text)
    print('Raccourcis ajoutés au menu Applications : Store et Installer les essentiels.')
    print('Aucun téléchargement effectué. Le premier lancement configure Flathub après confirmation.')


if __name__ == '__main__':
    main()
