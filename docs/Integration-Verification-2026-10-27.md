# Vérification des intégrations satellites — 27 octobre 2026

**Portée :** vérification statique des instantanés de code et de documentation datés du 27 octobre 2026. **Aucune qualification runtime, CI distante, publication ni autorisation de production n’est déduite de cet audit.**

## Frontière Koali Control Panel / qualification système

- `Koali-Control-Panel` **4.1.1** est un outil de développement (démarrage, diagnostics, construction et observation de composants) et non l'autorité des contrats, profils ou releases kOA-Linux.
- `kOA-Linux` conserve la responsabilité de l'assemblage, de l'admission de sources, de la construction d'images et des preuves de qualification. La couche Koali Spaces reste une expérience de composition optionnelle.
- Le workflow de build du Control Panel décrit `uv sync --frozen --all-groups` et une vérification de propreté Git avant une construction explicitement hors ligne. Ce mécanisme **n'atteste pas à lui seul** qu'une image QEMU ni les gates système/sécurité/offline passent.
- Éléments examinés : `Koali-Control-Panel/README.md`, `Koali-Control-Panel/koali_control/orchestration.py`, `Koali-Control-Panel/koali_control/devstack.py`, `koa-linux/README.md`, `koa-linux/docs/status/`.

**Qualification restante :** tests de l'interface Windows et de la stabilisation sur un environnement jetable, puis preuves image, QEMU, recovery, offline et sécurité dans leurs gates dédiés.

## Mise à jour et preuve

Cette page décrit un état vérifié **sur fichiers**. Si le code, les contrats ou les captures de tests ont évolué depuis le snapshot, réexécuter les tests et réviser cette page avant publication.
