import azure.functions as func
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.Function)

@app.route(route="fasting_glucose")
def http_trigger1(req: func.HttpRequest) -> func.HttpResponse:
    data = None
    try:
        data = req.get_json()
    except ValueError:
        pass

    glucose = req.params.get("fasting_glucose")
    if data and glucose is None:
        glucose = data.get("fasting_glucose")

    if glucose is None:
        return func.HttpResponse(
            json.dumps({"error": "Field 'fasting_glucose' is required."}),
            status_code=400, mimetype="application/json",
        )

    try:
        glucose_val = float(glucose)
    except (TypeError, ValueError):
         return func.HttpResponse(
        json.dumps({"error": "'fasting_glucose' must be a number."}),
        status_code=400, mimetype="application/json"
    )

    status = "normal" if glucose_val < 100 else "abnormal"
    category = "Normal (<100 mg/dL)" if status == "normal" else "Abnormal (>=100 mg/dL)"

    result = {
        "fasting_glucose": glucose_val,
        "status": status,
        "rule": "normal if fasting_glucose < 100 mg/dL (ADA/CDC)",
        "category": category,
    }