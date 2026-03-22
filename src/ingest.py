import csv


def read_csv(filepath):
    try:
        with open(filepath, mode="r", newline="") as file:
            reader = csv.DictReader(file)
            return list(reader)

    except FileNotFoundError:
        print(f"Error: File not found - '{filepath}'")
        print("Please check the file path and try again.")
        return []


def remove_duplicates(data):
    seen = set()
    unique = []
    duplicates = 0

    for row in data:
        # Use the id column to detect duplicates
        row_id = row.get("id", "")

        if row_id not in seen:
            seen.add(row_id)
            unique.append(row)
        else:
            duplicates += 1

    if duplicates > 0:
        print(f"Removed {duplicates} duplicate rows")

    return unique


def write_csv(filepath, data):
    if len(data) == 0:
        print(f"No data to write - skipping '{filepath}'")
        return

    try:
        with open(filepath, mode="w", newline="") as file:
            headers = data[0].keys()
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()

            for row in data:
                writer.writerow(row)

        print(f"Saved: {filepath} ({len(data)} rows)")

    except Exception as e:
        print(f"Error saving file '{filepath}': {e}")