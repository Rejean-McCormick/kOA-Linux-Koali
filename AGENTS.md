# Consignes agents — koa-linux

> Proposition rédigée à partir du SmartDump du 20 novembre 2026. Ce fichier ne remplace pas une décision, un contrat ni une politique du propriétaire. En cas de consigne plus récente, **la consigne propriétaire prévaut**.

- Commencer par [`docs/ai/INDEX.md`](docs/ai/INDEX.md), puis [`docs/ai/AI_CONTEXT.md`](docs/ai/AI_CONTEXT.md).
- Domaine : Plateforme kOA-Linux-Koali : assemblage par profils, admission d’artefacts, hôte et cycle de vie.
- Autorité : Les contrats d’assemblage, locks, profils et règles de sécurité du dépôt restent propriétaires; les outils de contrôle ne décident pas seuls de l’admission/activation.
- Précaution principale : Un build local, une simulation QEMU ou un résultat LevelUpDiag ne prouve pas qu’un service a été admis sur un hôte de production.
- Avant de modifier, relire les sources propriétaire listées dans l'index, les éventuels locks et les tests du dépôt actif.
- Ne lancer ni effet distant, ni déploiement, ni publication, ni migration, ni promotion de preuves sans approbation explicite.
- Les rapports RepoSurveyor sont des **profils d'ingénierie**, pas des certificats de maturité. Ne pas les inventer.
- Le Framework Kristal v11 reste facultatif et non bloquant, sauf contrat adopté explicitement par ce propriétaire.
