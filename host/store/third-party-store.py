#!/usr/bin/env python3
"""Optional third-party desktop applications; never a system-channel updater."""
from __future__ import annotations

import argparse
import fcntl
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

REMOTE = 'koali-flathub'
REMOTE_FILE = 'https://flathub.org/repo/flathub.flatpakrepo'
CATALOG = (
    ('org.mozilla.firefox', 'Firefox', 'Navigateur web'),
    ('org.videolan.VLC', 'VLC', 'Audio et vidéo'),
    ('org.mozilla.thunderbird', 'Thunderbird', 'Courriel et calendrier'),
    ('io.github.peazip.PeaZip', 'PeaZip', 'Archives 7z/ZIP — alternative graphique à 7-Zip'),
    ('com.github.dail8859.NotepadNext', 'Notepad Next', 'Éditeur — alternative à Notepad++, pas le même logiciel'),
    ('org.libreoffice.LibreOffice', 'LibreOffice', 'Documents, tableur et présentations'),
    ('org.keepassxc.KeePassXC', 'KeePassXC', 'Gestionnaire de mots de passe local'),
)
ALLOWED_IDS = frozenset(row[0] for row in CATALOG)
NATIVE_COMMANDS = {
    'org.mozilla.firefox': ('firefox', 'firefox-esr'),
    'org.mozilla.thunderbird': ('thunderbird',),
    'org.videolan.VLC': ('vlc',),
    'org.libreoffice.LibreOffice': ('libreoffice',),
    'io.github.peazip.PeaZip': ('peazip',),
    'com.github.dail8859.NotepadNext': ('notepadnext',),
    'org.keepassxc.KeePassXC': ('keepassxc',),
}


def run(args, **kwargs):
    return subprocess.run(args, text=True, check=False, **kwargs)


def dialog(kind, text):
    return run(['zenity', kind, '--no-markup', '--title=Applications tierces', '--width=640', '--text=' + text]).returncode


def installed(app_id):
    if any(shutil.which(command) for command in NATIVE_COMMANDS.get(app_id, ())):
        return True
    for scope in ('--user', '--system'):
        if run(['flatpak', 'info', scope, app_id], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
            return True
    return False


def selection():
    args = ['zenity', '--list', '--checklist', '--title=Installer les essentiels',
            '--text=Applications tierces Flathub. Décochez celles que vous ne souhaitez pas installer.\nInternet requis. Les permissions sont celles des paquets Flathub.',
            '--width=950', '--height=480', '--column=Installer', '--column=Identifiant',
            '--column=Application', '--column=Usage', '--hide-column=2', '--print-column=2', '--separator=|']
    for app_id, name, description in CATALOG:
        args.extend(['TRUE', app_id, name, description])
    result = run(args, stdout=subprocess.PIPE)
    if result.returncode != 0:
        return []
    selected = result.stdout.strip().split('|') if result.stdout.strip() else []
    if any(item not in ALLOWED_IDS for item in selected):
        raise ValueError('Sélection inconnue.')
    return list(dict.fromkeys(selected))


def configure_remote(log):
    # A dedicated name avoids changing the user's existing Flathub remote.
    # Verify any pre-existing remote before trusting its name.
    existing = run(['flatpak', 'remotes', '--user', '--columns=name,url'], stdout=subprocess.PIPE, stderr=log)
    if existing.returncode:
        raise RuntimeError('Impossible de lire les dépôts Flatpak.')
    for line in existing.stdout.splitlines():
        fields = line.split()
        if fields and fields[0] == REMOTE:
            if len(fields) != 2 or fields[1].rstrip('/') != 'https://dl.flathub.org/repo':
                raise RuntimeError('Le dépôt koali-flathub existant ne correspond pas à Flathub.')
            return
    result = run(['flatpak', 'remote-add', '--user', '--from', REMOTE, REMOTE_FILE], stdout=log, stderr=log)
    if result.returncode:
        raise RuntimeError('Configuration de Flathub impossible. Vérifiez la connexion réseau.')


def install_apps(app_ids, log):
    if not set(app_ids) <= ALLOWED_IDS:
        raise ValueError('Application hors présélection.')
    results = []
    for app_id in app_ids:
        if installed(app_id):
            results.append((app_id, 'déjà installé'))
            continue
        result = run(['flatpak', 'install', '--user', '--noninteractive', '--assumeyes', REMOTE, app_id + '//stable'], stdout=log, stderr=log)
        success = result.returncode == 0 and installed(app_id)
        results.append((app_id, 'installé' if success else 'échec'))
    return results


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('store', 'essentials', 'catalog'))
    args = parser.parse_args(argv)
    if args.action == 'catalog':
        print(json.dumps(CATALOG, ensure_ascii=False, indent=2))
        return 0
    if sys.platform != 'linux' or os.getuid() == 0:
        print('À lancer dans une session Linux utilisateur, sans sudo.', file=sys.stderr)
        return 2
    required = ['flatpak', 'zenity'] + (['gnome-software'] if args.action == 'store' else [])
    missing = [command for command in required if not shutil.which(command)]
    if missing:
        message = 'Infrastructure manquante : ' + ', '.join(missing) + '. Consultez host/store/README.md.'
        print(message, file=sys.stderr)
        if shutil.which('zenity'):
            dialog('--error', message)
        return 2
    state = Path(os.environ.get('XDG_STATE_HOME', str(Path.home() / '.local/state'))) / 'koali-store'
    state.mkdir(parents=True, exist_ok=True, mode=0o700)
    with (state / 'installation.lock').open('w') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            dialog('--info', 'Une opération est déjà en cours.')
            return 1
        selected = selection() if args.action == 'essentials' else []
        if args.action == 'essentials' and not selected:
            return 0
        if args.action == 'store' and dialog('--question', 'Ouvrir GNOME Logiciels et configurer Flathub pour votre compte ?\nLes applications sont fournies par des tiers.') != 0:
            return 0
        log_path = state / 'last-install.log'
        progress = None
        try:
            progress = subprocess.Popen(['zenity', '--progress', '--pulsate', '--no-cancel', '--auto-close',
                '--title=Applications tierces', '--text=Préparation et téléchargement en cours…'], stdin=subprocess.PIPE)
            with log_path.open('w') as log:
                configure_remote(log)
                results = install_apps(selected, log) if selected else []
            if args.action == 'store':
                # GNOME Software owns its own window/lifecycle.
                subprocess.Popen(['gnome-software'], stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
                return 0
            names = {item[0]: item[1] for item in CATALOG}
            failed = any(status == 'échec' for _, status in results)
            message = '\n'.join(f'{names[app]} : {status}' for app, status in results)
            message += '\n\nJournal : ' + str(log_path)
            if failed:
                message += '\nRelancez le raccourci pour réessayer les applications manquantes.'
            if progress:
                progress.terminate(); progress.wait(); progress = None
            dialog('--warning' if failed else '--info', message)
            return 1 if failed else 0
        except (OSError, RuntimeError, ValueError) as exc:
            dialog('--error', str(exc) + '\nJournal : ' + str(log_path))
            return 2
        finally:
            if progress:
                progress.terminate()
                progress.wait()


if __name__ == '__main__':
    raise SystemExit(main())
