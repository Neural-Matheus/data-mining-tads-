import json
from collections import Counter

def process_locations(entries):
    counts = {}
    for entry in entries:
        location = entry.get('location')
        if not isinstance(location, str):
            continue
        normalized_location = location.strip().lower()
        if normalized_location == "":
            continue
        counts[normalized_location] = counts.get(normalized_location, 0) + 1
    return sorted(counts.items(), key=lambda x: -x[1])

def generate_locations_csv(locations):
    header = "Location,Occurrences"
    rows = [f"{loc},{count}" for loc, count in locations]
    return header + "\n" + "\n".join(rows)

def process_locations_data(users):
    locations = process_locations(users)
    return generate_locations_csv(locations)

if __name__ == "__main__":
    with open('dados.json', 'r') as f:
        users = json.load(f)
    locations_csv = process_locations_data(users)
    print(locations_csv)
