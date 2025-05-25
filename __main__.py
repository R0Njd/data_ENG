import threading
import time
import requests
import json
import server  

if __name__ == "__main__":
    server_thread = threading.Thread(target=server.main(), daemon=True)
    server_thread.start()

    time.sleep(1)  

    url = "http://127.0.0.1:5000/lead"

    response = requests.get(url)
    data = response.json()

    with open("lead_data.json", "w") as f:
        json.dump(data, f, indent=4)



    

 