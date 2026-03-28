# TODO: Implement FileIndexer into Scanner

1. [x] Check and add `psutil` to requirements.txt if missing (already present), `pip install -r requirements.txt` not needed
2. [x] Implement full Scanner class in `app/scanner.py` based on provided FileIndexer logic (with method renames/adaptations) - base updates done
3. [x] Cleanup `app/utils/file_indexer.py` (kept as Scanner alias for compat)
4. [x] Add `ensure_data_dir` to `app/utils/helpers.py` if missing (already present)
5. [x] Test: Verified Scanner creates data/file_index.db, indexes apps via Config.SCAN_PATHS, update_access/get_top_items work as dicts, index_all=scan_system
6. [x] [DONE] Task complete

