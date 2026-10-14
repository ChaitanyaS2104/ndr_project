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

                srcip = event.get("src_ip")
                dstip = event.get("dest_ip")
                
                sport = event.get("src_port")
                dsport = event.get("dest_port")
                
                
                proto = event.get("proto")

                service = event.get("app_proto")

                flow = event.get("flow")
                
                state = flow.get("state")

                dur = flow.get("age")
                sbytes = flow.get("bytes_toserver")
                dbytes = flow.get("bytes_toclient")
                
                spkts = flow.get("pkts_toserver")
                dpkts = flow.get("pkts_toclient")

                print(f"Packet {event} {pkts_toclient} {pkts_toserver} from {src_ip} to {dest_ip} \n")
            
            if(event_type == "alert"):
                src_ip = event.get("src_ip")
                dest_ip = event.get("dest_ip")
                
                signature = event.get("alert.signature")
                severity = event.get("alert.severity")

            

        except json.JSONDecodeError:
            continue