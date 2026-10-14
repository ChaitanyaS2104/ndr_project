import json
import time
from models.network_log import NetworkLog
from models.alert_log import AlertLog

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
            
            if(event_type == "flow"):
                parsed_flow = NetworkLog.model_validate(event)

                print(f"Parsed Log {parsed_flow}\n")
            
            if(event_type == "alert"):
                parsed_alert = AlertLog.model_validate(event)
                
                print(f"Parsed Log {parsed_alert}\n")

            

        except json.JSONDecodeError:
            continue