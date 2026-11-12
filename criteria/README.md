# Criteria

The canonical [pipeline catalog](catalog.yaml) contains 45 stable IDs across visual feedback, design systems, UX, PWA, accessibility, motion, performance, tool adoption, evaluation and local resources. Category YAML files are exact subsets. The separate [product catalog](product/catalog.yaml) contains 31 criteria for general websites/webapps and applicable PWA features.

Data files are strict JSON with a `.yaml` extension (no comments; scripts parse them with a JSON parser). Fields are English: `id`, `level`, `category`, `platforms`, `requirement`, `research_evidence`, `test`, `passing`, `action`, `effort`; the product catalog adds `profiles`, `feature`, `evidence_required`, `priority` and `capabilities`. Levels MUST/SHOULD/MAY express obligations within the selected project/research contract. They are neither universal legislation nor universal style rules.

S/M/L are initial estimates (up to one day / two to five days / more than five days). Observe the actual product before estimating implementation. Each source reference resolves through [sources.yaml](../report/sources.yaml); documented capability is not measured product effect.

Record pass/fail/unknown/not_applicable with actual scope and evidence. An unknown is a missing check, not an observed defect. The general product audit applies profiles and confirmed features; the pipeline catalog describes a specific optional research contract.
