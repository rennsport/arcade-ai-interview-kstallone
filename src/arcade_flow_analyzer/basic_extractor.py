import json
from pathlib import Path
from .models import FlowData
from pydantic import ValidationError


def load_flow_data():
    """Load and validate the flow.json file using Pydantic"""
    flow_json = Path("flow.json")
    if not flow_json.exists():
        raise FileNotFoundError("flow.json not found!")

    with open(flow_json, 'r') as f:
        raw_data = json.load(f)
    
    try:
        # Validate the data using Pydantic model
        flow_data = FlowData(**raw_data)
        print("JSON passes flow model validation")
        return flow_data
    except ValidationError as e:
        print("JSON does not pass flow model validation")
        print(e)
        raise
    except Exception as e:
        print(f"Error parsing flow data: {e}")
        raise


def extract_basic_info(flow_data: FlowData):
    """Extract basic flow information"""
    print("Basic Flow Information")
    print("=" * 20)
    
    print(f"Flow Name: {flow_data.name}")
    print(f"Description: {flow_data.description}")
    print(f"Created By: {flow_data.createdBy}")
    print(f"Team ID: {flow_data.teamId}")
    print(f"Use Case: {flow_data.useCase}")
    print(f"AI Generated: {'Yes' if flow_data.hasUsedAI else 'No'}")
    print(f"Schema Version: {flow_data.schemaVersion}")
    print(f"Status: {flow_data.status}")


def extract_captured_events(flow_data: FlowData):
    """Extract captured events"""
    print("Captured Events")
    print("=" * 20)
    print(f"Total Events: {len(flow_data.capturedEvents)}")
    print()
    for event in flow_data.capturedEvents:
        print(f"Event: {event.type}")
        print(f"Time: {event.timeMs}")
        print(f"Start Time: {event.startTimeMs}")
        print(f"End Time: {event.endTimeMs}")
        print(f"Click ID: {event.clickId}")
        print(f"Frame X: {event.frameX}")
        print(f"Frame Y: {event.frameY}")
        print()


def extract_steps_info(flow_data: FlowData):
    """Extract steps information"""
    print("Steps")
    print("=" * 20)
    print(f"Total Steps: {len(flow_data.steps)}")
    print()
    for step in flow_data.steps:
        print(f"Step: {step.type}")
        print(f"ID: {step.id}")
        print(f"Title: {step.title}")
        print(f"Subtitle: {step.subtitle}")
        print()


def main():
    """Main function"""
    flow_data = load_flow_data()
    print()
    extract_basic_info(flow_data)
    print()
    extract_captured_events(flow_data)
    print()
    extract_steps_info(flow_data)


if __name__ == "__main__":
    main()
