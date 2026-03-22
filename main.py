from src.ingest import read_csv, write_csv
from src.validate import check_row
from src.report import generate_report

RAW = "data/raw_data1.csv"
CLEAN = "data/clean_data.csv"
REJECTED = "data/rejected_data.csv"


def run_clean():
    data = read_csv(RAW)

    if len(data) == 0:
        print("Cleaning stopped: no data was loaded.")
        return

    clean = []
    rejected = []

    for row in data:
        valid, error = check_row(row)

        if valid:
            clean.append(row)
        else:
            row["error"] = error
            rejected.append(row)

    write_csv(CLEAN, clean)
    write_csv(REJECTED, rejected)

    print(f"Total rows:    {len(data)}")
    print(f"Clean rows:    {len(clean)}")
    print(f"Rejected rows: {len(rejected)}")


def run_analyze():
    data = read_csv(CLEAN)

    if len(data) == 0:
        print("Analysis stopped: no clean data found.")
        return

    generate_report(data)


def main():
    print("=== Heart Disease Data Pipeline ===\n")

    print("--- Step 1: Cleaning Data ---")
    run_clean()

    print("\n--- Step 2: Analyzing Data ---")
    run_analyze()

    print("\n=== Done ===")


main()