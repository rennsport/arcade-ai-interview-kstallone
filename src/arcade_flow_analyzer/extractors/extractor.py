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
from ..models import FlowData
from pydantic import ValidationError
from datetime import datetime


def ms_to_datetime(timestamp_ms: int) -> str:
    """Convert milliseconds timestamp to readable datetime"""
    if timestamp_ms and timestamp_ms > 0:
        try:
            timestamp_seconds = timestamp_ms / 1000.0
            dt = datetime.fromtimestamp(timestamp_seconds)
            return dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        except Exception:
            return ""
    return ""


def process_flow(file_path: str):
    """Load JSON, validate with Pydantic, and extract basic event data"""
    with open(file_path, 'r') as f:
        raw_data = json.load(f)
    try:
        flow_data = FlowData(**raw_data)
    except ValidationError as e:
        raise ValueError(f"Validation failed: {e}")

    events = []
    steps_lookup = {step.id: step for step in flow_data.steps if step.id}

    for event in flow_data.capturedEvents:
        event_id = event.clickId or f"event_{len(events)}"
        step_data = steps_lookup.get(event_id)

        event_data = {
            'type': event.type,
            'timestamp_datetime': ms_to_datetime(event.timeMs or 0),
            'start_time_datetime': ms_to_datetime(event.startTimeMs or 0),
            'end_time_datetime': ms_to_datetime(event.endTimeMs or 0),
            'duration_seconds': 0,
            'click_text': '',
            'hotspot_label': '',
            'page_url': '',
            'page_title': '',
            'clickId': event.clickId or '',
        }
        if event.startTimeMs and event.endTimeMs:
            event_data['duration_seconds'] = (event.endTimeMs - event.startTimeMs) / 1000.0
        events.append(event_data)

        if step_data and step_data.clickContext:
            event_data['click_text'] = step_data.clickContext.text or ''
        
        if step_data and step_data.hotspots:
            hotspot = step_data.hotspots
            if hotspot:
                event_data['hotspot_label'] = hotspot[0].label or ''
        
        if step_data and step_data.pageContext:
            page_context = step_data.pageContext
            page_url = page_context.url or ''
            event_data['page_url'] = page_url
            event_data['page_title'] = page_context.title or ''

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
