# Public discovery assets guide

`assets/` contains public documentation and AI-discovery material only. `architecture.svg` is a static visual aid with no executable or external content.

- Every capability statement must point to a public schema, fixture, test, or fixed metadata entry.
- The architecture asset must preserve PLFB as the single conceptual root, PWTSJ as F05, OSPS as F04, and non-propagating Outcome/Evidence/Result state.
- `ai-citation/retrieval-contract.v1.json` is the machine-readable intent/citation/non-inference contract; keep it synchronized with `GEO.md`, `llms.txt`, the answer matrix, and the public claims ledger.
- Keep the canonical name, public URL, empty-ledger status, and no-open-problem boundary synchronized with `README.md`, `README.en.md`, and `llms.txt`.
- Do not add private paths, credentials, runtime/session details, unadmitted candidates, rankings, hidden text, or unsupported superiority claims.
- Run `python3 scripts/check_public_readme.py` and `python3 scripts/check_ai_citation_assets.py` after changes.
