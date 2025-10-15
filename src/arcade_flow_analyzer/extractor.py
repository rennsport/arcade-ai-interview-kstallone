"""
Arcade Flow/Actions Extractor

Current: Bare minimum as in loads the JSON, does basic validation,
extracts basic event info, and saves to CSV.

TODO: Extend to extract more information from the flow.json file. Include:
- Steps
- Hotspots
- Page Context
- Click Context
- Search Term
- Page Title
- Page Domain
"""

import json
import csv
from pathlib import Path
from arcade_flow_analyzer.models import FlowData
from pydantic import ValidationError


def process_flow(file_path: str):
    """Load JSON, validate with Pydantic, and extract basic event data"""
    with open(file_path, 'r') as f:
        raw_data = json.load(f)
    try:
        flow_data = FlowData(**raw_data)
    except ValidationError as e:
        raise ValueError(f"Validation failed: {e}")

    events = []
    for event in flow_data.capturedEvents:
        event_data = {
            'type': event.type,
            'timeMs': event.timeMs or 0,
            'clickId': event.clickId or '',
        }
        events.append(event_data)

    return {
        'name': flow_data.name,
        'events': events
    }


def save_to_csv(data, output_path: str):
    """Save events to CSV
    
    Ideally this would be saved to a database or in memory depending on the application,
    but for now we'll save to a CSV file"""
    cache_dir = Path("cache")
    cache_dir.mkdir(exist_ok=True)

    csv_path = cache_dir / output_path

    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        if data['events']:
            fieldnames = data['events'][0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data['events'])

    return str(csv_path)


if __name__ == "__main__":
    try:
        result = process_flow("flow.json")
        csv_path = save_to_csv(result, "actions.csv")
        print(f"Flow: {result['name']}")
        print(f"Events: {len(result['events'])}")
        print(f"CSV: {csv_path}")
    except Exception as e:
        print(f"Error: {e}")
