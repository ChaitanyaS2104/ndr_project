import json
import time

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

                src_ip = event.get("src_ip")
                dest_ip = event.get("dest_ip")
                dest_port = event.get("dest_port")
                
                flow = event.get("flow")
                pkts_toserver = flow.get("pkts_toserver")
                pkts_toclient = flow.get("pkts_toclient")
                bytes_toserver = flow.get("bytes_toserver")
                bytes_toclient = flow.get("bytes_toclient")
                age = flow.get("age")

                print(f"Packet {event} {pkts_toclient} {pkts_toserver} from {src_ip} to {dest_ip} \n")
            
            if(event_type == "alert"):
                src_ip = event.get("src_ip")
                dest_ip = event.get("dest_ip")
                
                signature = event.get("alert.signature")
                severity = event.get("alert.severity")

            

        except json.JSONDecodeError:
            continue