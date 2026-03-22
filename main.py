import argparse
from src.ingest import read_csv, write_csv, remove_duplicates
from src.validate import check_row
from src.report import generate_report

RAW = "data/raw_data2.csv"
CLEAN = "data/clean_data.csv"
REJECTED = "data/rejected_data.csv"


def run_clean():
    data = read_csv(RAW)

    if len(data) == 0:
        print("Cleaning stopped: no data was loaded.")
        return

    # Remove duplicate rows before validating
    data = remove_duplicates(data)

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
        print("Run 'python main.py clean' first.")
        return

    generate_report(data)


def main():
    parser = argparse.ArgumentParser(description="Heart Disease Data Pipeline")

    parser.add_argument(
        "command",
        choices=["clean", "analyze", "all"],
        help="'clean' to validate data | 'analyze' to generate report | 'all' to do both"
    )

    args = parser.parse_args()

    print("=== Heart Disease Data Pipeline ===\n")

    if args.command == "clean":
        print("--- Cleaning Data ---")
        run_clean()

    elif args.command == "analyze":
        print("--- Analyzing Data ---")
        run_analyze()

    elif args.command == "all":
        print("--- Step 1: Cleaning Data ---")
        run_clean()
        print("\n--- Step 2: Analyzing Data ---")
        run_analyze()

    print("\n=== Done ===")


main()