# Root cause fix report - 2026-04-29

## Exact root cause

`script/sync_multilingual_readmes.py` rebuilt every localized README directly from `README.md` and then reapplied locale string substitutions, including `News` and `Menu`.

That made localized `News/Menu` look like regeneratable derived content instead of protected human-maintained content. Any generic sync run could therefore overwrite curated localized updates with the English/base-template version.

A secondary compatibility wrinkle also existed in the repo history: some localized README files still kept the English `Menu` heading even when their section body was localized. Protection therefore needed to match both localized and legacy English heading variants when preserving existing sections.

## Files/scripts changed

- `script/sync_multilingual_readmes.py`
  - added module docstring documenting that localized `News/Menu` are protected assets
  - added `--rewrite-protected-sections` explicit opt-in flag
  - added section extraction/replacement helpers
  - default behavior now preserves existing localized `News/Menu` blocks from each README before writing
  - added verification guard that raises if protected sections change during a default sync
  - added legacy heading fallback support so preservation still works for files that kept English `Menu`/`News` headings
- `tmp/insert_multilingual.py`
  - clarified in the docstring that it must not be expanded into a generic sync that rewrites localized `News/Menu`
- `tmp/verify_sync_protected_sections.py`
  - lightweight verification script that snapshots localized `News/Menu` hashes, runs the sync, and fails if protected sections or localized README files change unexpectedly

## How the protection now works

Default mode:
- build the localized README from the English base as before
- before writing, extract the current localized `News` and `Menu` blocks from the existing file
- replace the newly generated versions with the extracted current blocks
- verify those protected blocks are byte-identical after the sync
- write the result only after the guard passes

Explicit override:
- `python3 script/sync_multilingual_readmes.py --rewrite-protected-sections`
- this is the only mode that allows the script to regenerate localized `News/Menu`

## Verification performed

1. Ran default sync:
   - `python3 script/sync_multilingual_readmes.py`
2. Ran safeguard verification:
   - `python3 tmp/verify_sync_protected_sections.py`
3. Result:
   - verification passed
   - localized `News/Menu` hashes stayed unchanged
   - no localized README diff was introduced by the default sync

## Commit hash / push status

- Commit hash: pending
- Push status: pending
