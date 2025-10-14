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


if __name__ == "__main__":
    flow_data = load_flow_data()
    extract_basic_info(flow_data)
