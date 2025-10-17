import json
import functions_framework

@functions_framework.http
def hello_http(request):
    """HTTP Cloud Function.
    Expects JSON with 'fasting_glucose' (or query param fallback).
    Returns JSON classification of fasting glucose.
    """
    data = request.get_json(silent=True) or {}
    args = request.args or {}

    glucose = data.get("fasting_glucose", args.get("fasting_glucose"))

    if glucose is None:
        return(
            json.dumps({"error": "Field 'fasting_glucose' is required."}),
            400,
            {"Content-Type": "application/json"},
        )

    try:
        glucose_val = float(glucose)
    except (TypeError, ValueError):
        return (
            json.dumps({"error": "'fasting_glucose' must be a number."}),
            400,
            {"Content-Type": "application/json"},
        )

    status = "normal" if glucose_val < 100 else "abnormal"
    category = (
        "normal (<100 mg/dL)"
        if status == "normal"
        else "Elevated/Abnormal (>=100 mg/dL)"
    )

    payload = {
        "fasting_glucose": glucose_val,
        "status": status,
    }
    

    return json.dumps(payload), 200, {"Content-Type": "application/json"}
    
