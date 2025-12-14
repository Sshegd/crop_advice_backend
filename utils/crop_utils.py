def extract_crop_name(activity_logs: dict) -> str:
    """
    Extract cropName from any activity log safely
    """
    if not activity_logs:
        return "Unknown Crop"

    for _, log in activity_logs.items():
        name = log.get("cropName")
        if name:
            return name.title()

    return "Unknown Crop"
