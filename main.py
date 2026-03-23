import argparse
import os
from src.ingest import read_csv, write_csv
from src.validate import clean_dataset
from src.report import generate_report

CLEAN = "data/clean_data.csv"
REJECTED = "data/rejected_data.csv"


def pick_file():
    # Get all CSV files inside the data/ folder
    files = []
    for f in os.listdir("data/"):
        if f.endswith(".csv"):
            files.append(f)

    if len(files) == 0:
        print("No CSV files found in data/ folder.")
        return None

    print("Available files in data/:")
    for i in range(len(files)):
        print(f"  {i + 1}. {files[i]}")

    choice = input("\nEnter the number of the file you want to use: ")

    if not choice.isnumeric():
        print("Invalid input. Please enter a number.")
        return None

    index = int(choice) - 1

    if index < 0 or index >= len(files):
        print("Invalid choice. Please pick a number from the list.")
        return None

    selected = f"data/{files[index]}"
    print(f"\nSelected: {files[index]}\n")
    return selected


def run_clean(raw):
    data = read_csv(raw)

    if len(data) == 0:
        print("Cleaning stopped: no data was loaded.")
        return

    clean, rejected = clean_dataset(data)

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
        raw = pick_file()
        if raw:
            print("--- Cleaning Data ---")
            run_clean(raw)

    elif args.command == "analyze":
        print("--- Analyzing Data ---")
        run_analyze()

    elif args.command == "all":
        raw = pick_file()
        if raw:
            print("--- Step 1: Cleaning Data ---")
            run_clean(raw)
            print("\n--- Step 2: Analyzing Data ---")
            run_analyze()

    print("\n=== Done ===")


main()