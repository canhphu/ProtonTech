from typing import List, Dict


def average_score(rows: List[Dict[str, str]]) -> float:
    # Bug: dividing by len(rows) without checking empty list
    total = 0.0
    for row in rows:
        total += float(row["score"])
    return total / len(rows)


if __name__ == "__main__":
    sample = [
        {"name": "A", "score": "10"},
        {"name": "B", "score": "20"},
    ]
    print("Average:", average_score(sample))
