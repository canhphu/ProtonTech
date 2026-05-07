from typing import Dict, Iterable, List


Row = Dict[str, str]


def normalize_names(rows: Iterable[Row]) -> List[Row]:
    normalized: List[Row] = []
    for row in rows:
        name = row.get("name")
        if name is None:
            normalized.append(dict(row))
            continue

        updated = dict(row)
        updated["name"] = name.strip().title()
        normalized.append(updated)

    return normalized
