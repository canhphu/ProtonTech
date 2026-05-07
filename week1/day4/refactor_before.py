def normalize_names(rows):
    output = []
    for row in rows:
        name = row.get("name")
        if name is None:
            output.append(row)
        else:
            row["name"] = name.strip().title()
            output.append(row)
    return output
