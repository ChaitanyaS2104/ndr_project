import json
import time
import joblib
import pandas as pd
from models.network_log import NetworkLog
from models.alert_log import AlertLog

# 1. Load your saved machine learning model and preprocessor
print("Loading preprocessor and trained ML model...")
preprocessor = joblib.load("suricata_preprocessor.pkl")
model = joblib.load("suricata_nids_model.pkl")
print("Model and preprocessor loaded successfully! Starting live monitoring...\n")

file_path = "/var/log/suricata/eve.json"

with open(file_path, "r") as f:
    f.seek(0, 2)

    while True:
        line = f.readline()

        if not line:
            time.sleep(0.05)
            continue
        
        try:
            event = json.loads(line.strip())
            event_type = event.get("event_type")
            
            # --- HANDLE FLOW LOGS + REAL-TIME ML INFERENCE ---
            if event_type == "flow":
                # Step A: Validate and parse raw JSON with Pydantic
                parsed_flow = NetworkLog.model_validate(event)
                
                # Step B: Convert Pydantic object to a DataFrame row matching training features
                flow_dict = {
                    'dur': [parsed_flow.dur],
                    'sbytes': [parsed_flow.sbytes],
                    'dbytes': [parsed_flow.dbytes],
                    'spkts': [parsed_flow.spkts],
                    'dpkts': [parsed_flow.dpkts],
                    'proto': [parsed_flow.proto],
                    'service': [parsed_flow.service],
                    'state': [parsed_flow.state]
                }
                df_input = pd.DataFrame(flow_dict)
                
                # Step C: Apply saved preprocessor (scaling & one-hot encoding)
                X_processed = preprocessor.transform(df_input)
                
                # Step D: Run ML Model Prediction
                prediction = model.predict(X_processed)[0]
                probability = model.predict_proba(X_processed)[0]
                
                # Step E: Output results
                if prediction == 1:
                    confidence = probability[1] * 100
                    print(f"🚨 [ALERT/THREAT DETECTED] Flow: {parsed_flow.srcip}:{parsed_flow.sport} -> {parsed_flow.dstip}:{parsed_flow.dsport} | Confidence: {confidence:.2f}%")
                else:
                    print(f"✅ [NORMAL FLOW] {parsed_flow.srcip} -> {parsed_flow.dstip} ({parsed_flow.proto})")
            
            # --- HANDLE SURICATA SIGNATURE ALERTS ---
            elif event_type == "alert":
                parsed_alert = AlertLog.model_validate(event)
                print(f"⚠️ [SURICATA RULE MATCH] [Severity {parsed_alert.severity}] {parsed_alert.srcip}:{parsed_alert.sport} -> {parsed_alert.dstip}:{parsed_alert.dsport}")
                print(f"         Signature: {parsed_alert.signature}\n")

        except json.JSONDecodeError:
            continue
        except Exception as e:
            # Catch any unexpected transformation/parsing errors so the live loop never dies
            continue