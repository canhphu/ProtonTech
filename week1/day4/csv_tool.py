import argparse
import csv
import os
from typing import Dict, Iterable, List, Optional


Row = Dict[str, str]


def read_csv(path: str) -> List[Row]:
    with open(path, "r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return list(reader)


def filter_rows(
    rows: Iterable[Row],
    column: str,
    contains: Optional[str] = None,
    min_value: Optional[float] = None,
    max_value: Optional[float] = None,
) -> List[Row]:
    filtered: List[Row] = []
    for row in rows:
        if column not in row:
            continue

        value = row.get(column, "")
        if contains is not None and contains.lower() not in value.lower():
            continue

        if min_value is not None or max_value is not None:
            try:
                numeric = float(value)
            except ValueError:
                continue
            if min_value is not None and numeric < min_value:
                continue
            if max_value is not None and numeric > max_value:
                continue

        filtered.append(row)

    return filtered


def compute_stats(rows: Iterable[Row], column: str) -> Dict[str, Optional[float]]:
    values: List[float] = []
    for row in rows:
        value = row.get(column)
        if value is None:
            continue
        try:
            values.append(float(value))
        except ValueError:
            continue

    if not values:
        return {"count": 0, "min": None, "max": None, "mean": None}

    total = sum(values)
    return {
        "count": len(values),
        "min": min(values),
        "max": max(values),
        "mean": total / len(values),
    }


def write_csv(path: str, rows: Iterable[Row], fieldnames: List[str]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Process CSV files with filters and stats.")
    parser.add_argument("input", help="Path to input CSV")
    parser.add_argument("--output", help="Optional output CSV for filtered rows")
    parser.add_argument("--filter-column", help="Column used for filtering")
    parser.add_argument("--contains", help="Substring to match")
    parser.add_argument("--min", dest="min_value", type=float, help="Minimum numeric value")
    parser.add_argument("--max", dest="max_value", type=float, help="Maximum numeric value")
    parser.add_argument("--stats-column", help="Column used for numeric statistics")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = read_csv(args.input)

    filtered_rows = rows
    if args.filter_column:
        filtered_rows = filter_rows(
            rows,
            column=args.filter_column,
            contains=args.contains,
            min_value=args.min_value,
            max_value=args.max_value,
        )

    if args.stats_column:
        stats = compute_stats(filtered_rows, args.stats_column)
        print("Stats:")
        print(stats)

    if args.output:
        fieldnames = list(rows[0].keys()) if rows else []
        if not fieldnames:
            raise ValueError("No rows available to infer CSV headers")
        write_csv(args.output, filtered_rows, fieldnames)
        print(f"Saved {len(filtered_rows)} rows to {os.path.abspath(args.output)}")


if __name__ == "__main__":
    main()
