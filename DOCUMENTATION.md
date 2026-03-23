# Technical Documentation

This document explains the design decisions behind the Heart Disease Data Pipeline — not just what the code does, but why it was built the way it was.

---

## Overall Architecture

The pipeline is split into four files, each with one clear responsibility. This is called modular design. When something breaks or needs to change, you only touch one file instead of hunting through a single massive script. Data always flows in one direction — `main.py` coordinates everything, `ingest.py` handles files, `validate.py` handles data rules, and `report.py` handles analysis.

---

## main.py

`main.py` is the controller. It does not do any data logic itself — it just coordinates the other files. `argparse` was used for the CLI because it is the standard Python approach and automatically handles wrong commands and generates help messages. `pick_file()` was added so the program is not hardcoded to a specific filename — it reads whatever CSVs are in the `data/` folder and lets the user choose, making the pipeline reusable. The early return check when data is empty prevents silent failures from passing empty data downstream.

---

## ingest.py

`ingest.py` handles all file input and output so that `main.py` does not need to know how files work. `csv.DictReader` was used so rows are accessed by name like `row['age']` instead of by position, which is more readable. `FileNotFoundError` is caught explicitly to print a clear message instead of crashing with a raw Python error. In `write_csv`, the file is opened before checking if data is empty — opening in `"w"` mode clears the file immediately, which fixed a bug where rejected rows from a previous run would stay in the file even after being fixed. A `set` is used for duplicate detection instead of a list because checking membership in a set is instant regardless of size, which matters a lot with 270,000 rows.

---

## validate.py

`validate.py` decides whether a row is trustworthy. Each field has its own `try/except` block so if multiple fields fail, all errors are reported — not just the first one. `int(float(value))` is used instead of just `int(value)` to handle values stored as `"58.0"` instead of `"58"`. Two separate sets track duplicates — one for duplicate IDs and one for exact row copies. Encoded values like `Sex` and `Chest pain type` are converted to readable text only after validation passes, so the rejected file always contains the original raw values.

---

## report.py

`report.py` only reads data and never modifies it, so it is safe to run multiple times. It uses lowercase keys to match the normalized headers that `clean_dataset()` produces. The chest pain distribution uses a dictionary so it works regardless of how many types exist in the data. Heart disease rate is shown as a percentage rather than a raw count so it stays meaningful when comparing datasets of different sizes.