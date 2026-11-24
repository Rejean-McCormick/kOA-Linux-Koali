<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-AI-LOT7-CONTEXT",
  "document_class": "explanatory_markdown",
  "status": "draft",
  "language": "fr",
  "layer": "documentation_support",
  "scope": [
    "global"
  ],
  "canonical_refs": [],
  "decision_ids": [],
  "requirement_ids": [],
  "lock_ids": [],
  "exception_ids": [],
  "depends_on": [],
  "tags": [
    "lot7",
    "non-authoritative",
    "historical-source"
  ]
}
KOA:DOC-META:END -->

<!-- kOA Doc Server · Docs IA · lot 03 · projet : koa-linux · proposition dérivée à valider -->
# Contexte IA — koa-linux

## Identité et périmètre observés

Plateforme kOA-Linux-Koali : assemblage par profils, admission d’artefacts, hôte et cycle de vie.

**Limite d'autorité :** Les contrats d’assemblage, locks, profils et règles de sécurité du dépôt restent propriétaires; les outils de contrôle ne décident pas seuls de l’admission/activation.

**Provenance :** `SmartDump_20261120_221507.zip` → `koa-linux_Code_snapshot.zip` (20 novembre 2026). Les sources citées sont celles de cette capture; le propriétaire du dépôt conserve l'autorité sur les révisions présentes et futures.

## Avant toute proposition de modification

1. Déterminer si le travail demandé porte sur **un document, un contrat, une donnée, un exécutable ou un résultat dérivé**.
2. Consulter les fichiers propriétaires, dans cet ordre :
   - [`README.md`](../../README.md)
   - [`assembly/README.md`](../../assembly/README.md)
   - [`ci/README.md`](../../ci/README.md)
   - [`Cargo.toml`](../../Cargo.toml)
   - [`docs/README.md`](../../docs/README.md)

3. Vérifier les éventuels `AGENTS.md`, manifests, locks, schémas ou décisions de ce checkout; ne pas traiter cette fiche dérivée comme un substitut.
4. Cartographier producteur, consommateur, format, version et permissions pour chaque frontière franchie.

## Procédure adaptée

**Tâche type :** Partir de la carte d’autorité documentaire, vérifier le profil primaire et les overlays compatibles, résoudre les verrouillages puis exécuter les validations d’assemblage propriétaire.

**Éviter précisément :** Un build local, une simulation QEMU ou un résultat LevelUpDiag ne prouve pas qu’un service a été admis sur un hôte de production.

**Contrôles attendus avant la conclusion :** identifier les tests, validateurs et rapports réellement présents sur le système cible; exécuter uniquement ceux qui sont non destructifs et appropriés; relier chaque résultat à une révision et un environnement précis. En absence de code/test (ou si les sources sont insuffisantes), écrire « non vérifié », jamais « PASS ».

## Utilisation par kOA Doc Server

- **Lecture et export :** n'inclure que les documents explicitement sélectionnés, avec chemins relatifs, empreintes et provenance.
- **RepoSurveyor :** profils mesurés séparément à partir du code local. Ne pas fabriquer `ENGINEERING_PROFILE.md` depuis cette fiche; l'alias français est `PROFIL_INGENIERIE.md` après génération réelle.
- **Diagnostics :** observations datées, preuves historiques et états certifiés restent distincts. Aucune promotion automatique.
- **Wikis et vues :** documents dérivés, jamais propriétaires des contrats ni des permissions.
- **Confidentialité :** filtrer secrets, données personnelles, médias sous droits, caches, backups et rapports privés avant un ZIP de contexte IA.
- **Standard Kristal Framework v11 :** si pertinent, consulter le cadre comme référence possible, sans l'exiger pour naviguer ni forcer une migration du profil historique du dépôt.

## État de cette fiche

`DOCUMENTATION_REDACTIONNELLE_A_REVOIR` : elle facilite le démarrage d'un agent, mais **ne prouve aucun état d'intégration, publication, conformité ni maturité**.
