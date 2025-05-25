import threading
import time
import requests
import json
import server 

def run_server():
    server.main()

if __name__ == "__main__":
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    time.sleep(1)  

    url = "http://127.0.0.1:5000/lead"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        with open("lead_data.json", "w") as f:
            json.dump(data, f, indent=4)

        print("Data saved to lead_data.json")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")