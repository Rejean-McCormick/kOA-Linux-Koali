# Store et essentiels — applications tierces

Cette extension fournit deux entrées de menu Linux : **Store — applications tierces**
et **Installer les essentiels**. Le store est GNOME Logiciels avec son greffon
Flatpak, utilisant Flathub. Les logiciels restent des applications externes ;
ils ne deviennent pas des modules métiers Koali.

La présélection contient Firefox, VLC, Thunderbird, PeaZip, Notepad Next,
LibreOffice et KeePassXC. PeaZip est l'alternative graphique à 7-Zip ; Notepad Next
est une réimplémentation multiplateforme distincte de Notepad++. Cette livraison
n'installe pas les exécutables Windows ni Wine.

## Utiliser sur une machine Linux existante

Prérequis à installer par le gestionnaire de la distribution : Python 3, Flatpak,
GNOME Logiciels **avec son greffon Flatpak**, Zenity, une session graphique avec
D-Bus utilisateur et un backend xdg-desktop-portal adapté au compositeur.

Depuis la racine du dépôt, sans sudo :

```sh
python3 host/store/setup-user.py
```

Ouvrir ensuite le menu Applications. Ce script copie seulement les lanceurs ;
il ne télécharge rien. On peut aussi exécuter directement :

```sh
python3 host/store/third-party-store.py store
python3 host/store/third-party-store.py essentials
```

Le raccourci des essentiels affiche une liste modifiable. Valider cette liste
configure le dépôt utilisateur `koali-flathub` et installe les éléments choisis.
Annuler ne configure rien. Le store demande confirmation avant sa configuration.
Les paquets de la présélection sont installés avec `flatpak --user`, sans sudo.
Les applications déjà présentes via Flatpak utilisateur/système ou une commande
native connue sont ignorées. Les échecs partiels sont visibles et réessayables.
Les téléchargements des runtimes partagés peuvent dépasser largement la taille
des applications. Une première installation nécessite Internet.

Le journal se trouve dans `$XDG_STATE_HOME/koali-store/last-install.log`
(par défaut `~/.local/state/koali-store/last-install.log`). Un verrou évite deux
installations simultanées par ces raccourcis. Le store conserve sa propre gestion
des installations et des mises à jour. Aucun changement de logiciel par défaut
n'est effectué par le raccourci.

## Intégration image kOA

- `host/image/package-sets/user-lightweight.yaml` exige désormais les capacités
  `third-party-flatpak`, `third-party-software-store`, `desktop-install-dialogs`.
- L'adaptateur de distribution doit les résoudre vers les paquets exacts admis
  (versions, empreintes, provenance), incluant le greffon Flatpak du store.
  Cette livraison ne fournit pas de nouveaux artefacts binaires signés.
- `.koa/runtime-paths.json` projette le script et les deux fichiers `.desktop`.
- Les deux politiques sous `profiles/native-applications/` autorisent uniquement
  le lancement des raccourcis dans `user_lightweight`, via les contrôles existants.
- Les quatre applications natives de conformité déjà déclarées par le profil
  restent présentes. La présélection évite de les réinstaller lorsqu'elles sont
  détectées. Les autres applications ne sont pas intégrées à l'image par défaut.

Les nouveaux logiciels installés ne reçoivent pas automatiquement une admission
au broker natif Koali. Ils sont accessibles par le store/menu du bureau ; une
projection dans Koali Spaces nécessite leurs propres politiques d'admission et
de données. Les profils Flatpak se trouvent généralement sous `~/.var/app/` :
leur sauvegarde et leur compatibilité ne sont pas garanties par les politiques
natives existantes. L'installation tierce n'est pas une activation du Release Set
et ne modifie pas les mécanismes de mise à jour ou de rollback du système.

Aucune modification n'est nécessaire dans les snapshots Control Panel et Spaces
pour ces lanceurs Linux. Cette livraison ne fournit pas de store Windows.

## Vérification

```sh
python3 tests/system/test_third_party_store.py
```

Tests isolés sans réseau : annulation, sélection fermée, dépôt inattendu, reprise,
échecs partiels, installation utilisateur et catalogue sans effet de bord.
Les trois tests de `test_native_workspace_package_set.py` passent également ; les
deux politiques sont acceptées par les lecteurs du broker. La suite pytest
complète n'a pas été exécutée (pytest absent de l'environnement de livraison).

À vérifier dans la VM cible avant publication : résolution des nouveaux paquets,
présence des deux entrées de menu, greffon Flatpak du store, sélection/annulation,
installation réelle, relance après coupure réseau, permissions, audio et portails.
Aucune image système n'a été construite ou démarrée dans cet environnement.

## Sources des applications

- [Flatpak : commandes et portée utilisateur](https://docs.flatpak.org/en/latest/using-flatpak.html)
- [Firefox](https://flathub.org/apps/org.mozilla.firefox)
- [VLC](https://flathub.org/apps/org.videolan.VLC)
- [Thunderbird : instructions de l'éditeur](https://support.mozilla.org/en-US/kb/installing-thunderbird-linux)
- [PeaZip](https://flathub.org/apps/io.github.peazip.PeaZip)
- [Notepad Next](https://flathub.org/apps/com.github.dail8859.NotepadNext)
- [LibreOffice](https://flathub.org/apps/org.libreoffice.LibreOffice)
- [KeePassXC](https://flathub.org/apps/org.keepassxc.KeePassXC)
