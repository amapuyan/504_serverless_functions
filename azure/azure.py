import azure.functions as func
import logging
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="http_trigger1")
def http_trigger1(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request")

    try:
        data = req.get_json()
    except ValueError:
        data = {}

    glucose = data.get("fasting_glucose") or req.params.get("fasting_glucose") 
    

    if glucose is None:
        return func.HttpResponse(
            json.dumps({"error": "Please provide 'fasting_glucose' in mg/dL."}),
            status_code=400,
            mimetype="application/json",
        )

    try:
        glucose_val = float(glucose)
    except (TypeError, ValueError):
        return func.HttpResponse(
            json.dumps({"error": "'fasting_glucose' must be a number."}),
            status_code=400,
            mimetype="application/json"
        )

    status = "normal" if glucose_val < 100 else "abnormal"
    result = {"fasting_glucose": glucose_val, "status": status}

    return func.HttpResponse(
        json.dumps(result),
        status_code=200,
        mimetype="application/json"
    )