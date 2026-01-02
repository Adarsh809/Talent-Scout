import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

DATA_PATH = Path("candidate_data.json")

def load_all_candidates() -> List[Dict[str, Any]]:
    if not DATA_PATH.exists():
        return []
    try:
        return json.loads(DATA_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []

def save_candidate(candidate: Dict[str, Any]) -> None:
    """
    Append candidate record to JSON file (simulated DB).
    """
    data = load_all_candidates()
    candidate["timestamp"] = datetime.utcnow().isoformat()
    data.append(candidate)
    DATA_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")
