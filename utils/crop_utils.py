# utils/crop_utils.py
from typing import List, Dict, Union

def extract_crop_name(
    activity_logs: Union[List[Dict], Dict[str, Dict]]
) -> str | None:
    """
    Safely extract crop name from activity logs.
    Supports both:
    - List[Dict] (Firebase arrays)
    - Dict[str, Dict] (indexed logs)
    """

    if not activity_logs:
        return None

    # 🔁 Normalize to iterable of logs
    if isinstance(activity_logs, dict):
        logs = activity_logs.values()
    elif isinstance(activity_logs, list):
        logs = activity_logs
    else:
        return None

    for log in logs:
        if not isinstance(log, dict):
            continue

        # Common keys used in Firebase
        for key in ["cropName", "crop", "selectedCrop", "primaryCropName"]:
            if key in log and log[key]:
                return str(log[key]).strip()

        # Nested safety (optional)
        if "details" in log and isinstance(log["details"], dict):
            crop = log["details"].get("cropName")
            if crop:
                return str(crop).strip()

    return None
