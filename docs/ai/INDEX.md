<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-AI-LOT7-INDEX",
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
# Navigation IA — koa-linux

**Objet constaté :** Plateforme kOA-Linux-Koali : assemblage par profils, admission d’artefacts, hôte et cycle de vie.

**Frontière de responsabilité :** Les contrats d’assemblage, locks, profils et règles de sécurité du dépôt restent propriétaires; les outils de contrôle ne décident pas seuls de l’admission/activation.

**Source :** `SmartDump_20261120_221507.zip` → `koa-linux_Code_snapshot.zip` (20 novembre 2026). Le chemin Windows est une déclaration de snapshot, pas une vérification de l'état actuel.

**Statut :** Documentation de navigation dérivée de sources propriétaires, à revoir. Ce document ne vaut ni profil d'ingénierie mesuré, ni certification, ni permission d'exécution.

## Ordre de lecture — fichiers réellement présents dans la capture

1. [`README.md`](../../README.md) — SHA-256 `beae6816db560ea0…` dans la capture.
2. [`assembly/README.md`](../../assembly/README.md) — SHA-256 `e74d20a8acfb9677…` dans la capture.
3. [`ci/README.md`](../../ci/README.md) — SHA-256 `d88df187a15c6e6d…` dans la capture.
4. [`Cargo.toml`](../../Cargo.toml) — SHA-256 `3df4330ab967fe0e…` dans la capture.
5. [`docs/README.md`](../../docs/README.md) — SHA-256 `cdc4cbbd93fe2ef4…` dans la capture.

## Parcours recommandé pour une intervention assistée par IA

1. Identifier la question, le sous-système concerné et les responsabilités du propriétaire.
2. Lire les documents ci-dessus **dans cet ordre**; consulter les contrats et consignes propriétaires plus récents si le checkout a évolué.
3. Partir de la carte d’autorité documentaire, vérifier le profil primaire et les overlays compatibles, résoudre les verrouillages puis exécuter les validations d’assemblage propriétaire.
4. Établir les vérifications effectivement disponibles dans la révision locale, consigner les résultats et ne conclure qu'à l'intérieur du périmètre couvert.
5. Proposer les changements; demander une décision explicite avant toute écriture à effet, déploiement, publication ou promotion de preuves.

## Risque propre à ce dépôt

Un build local, une simulation QEMU ou un résultat LevelUpDiag ne prouve pas qu’un service a été admis sur un hôte de production.

## Compléments

- [`AI_CONTEXT.md`](AI_CONTEXT.md) : règles de travail et frontières de confiance.
- `AGENTS.md` : s'il existe déjà chez le propriétaire, ses consignes priment sur ces propositions; sinon l'overlay peut en ajouter un sans remplacement.
- `PROFIL_INGENIERIE.md` : optionnel, uniquement après exécution réelle de RepoSurveyor sur un dépôt local et accord explicite pour sa copie.
- Le Framework Kristal v11 est un standard documentaire **facultatif** : lire le profil réellement verrouillé, sans imposer de migration.
