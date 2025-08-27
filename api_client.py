

import requests #library for HTTP requests
from models.machine_status import MachineStatus
from typing import List, Optional
import traceback #to send errors in console
import os
from dotenv import load_dotenv  # library to work with .env


load_dotenv() # load the variables


class Apiclient:
    def __init__(self, base_url: str = "https://laundryapi-production.up.railway.app"): #server's url
        self.base_url = base_url
        self.api_key = os.getenv("TELEGRAM_API_KEY")
        if not self.api_key:
            raise ValueError("❌ TELEGRAM_API_KEY is not set in .env")
        
        self.headers = { #headers with api-key
            "x-api-key": self.api_key #standart header name used by API
        }

    def get_machine_status(self, machine_id: str) -> Optional[MachineStatus]: #gets machine id and returns machine status
        try:
            url = f"{self.base_url}/status/{machine_id}" #creating a http request
            response = requests.get(url, headers=self.headers, timeout=5) #get request that waits 5 seconds
            response.raise_for_status() #if server returns code 4xx or 5xx creates an exclusion

            data = response.json() #transfers json from server into python dictionary

            if not all(k in data for k in ["device_id", "status", "timestamp"]): #check if all keys are present
                print(f"⚠️ Incomplete data received for {machine_id}: {data}")
                return None

            return MachineStatus( #create and return object
                machine_id=data["device_id"],
                status=data["status"],
                timestamp=data["timestamp"]
            )

        except Exception as e:
            self.handle_error(f"get_machine_status({machine_id})", e) #for any errors raise this and return none
            return None

    def get_all_statuses(self) -> List[MachineStatus]:
        try:
            url = f"{self.base_url}/status" #url without an id so server has to sent the whole base in the json
            response = requests.get(url, headers=self.headers, timeout=5)
            response.raise_for_status()

            all_data = response.json() 
            result = []

            for machine_id, entry in all_data.items():
                if not all(k in entry for k in ["status", "timestamp"]): 
                    print(f"⚠️ Incomplete entry for {machine_id}: {entry}") #check all the keys. if smth is missing - skip
                    continue

                result.append(MachineStatus(
                    machine_id=machine_id,
                    status=entry["status"],
                    timestamp=entry["timestamp"]
                ))

            return result

        except Exception as e:
            self.handle_error("get_all_statuses", e)
            return []

    @staticmethod
    def handle_error(context: str, error: Exception):
        print(f"❌ API error in {context}: {error}")
        traceback.print_exc() #outputs the full trace to where the error occurred