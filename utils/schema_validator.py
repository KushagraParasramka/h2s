import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.schema import Schema


schema = Schema()

def validateSchema(candidate: dict = None)-> bool:
    if not candidate:
        print("no candidate")
        return False
    
    try:
        queue = [""]
        while len(queue):
            path = queue.pop(0)
            result = schema.checkField(path = path, candidate = candidate)
            if(not result.get("status")):
                # print(f"Field not found : {path}")
                continue
                # return True
            validated = schema.validateType(result.get("data"), result.get("schema"))
            if not validated.get("status"):
                print(f"Validation failed : {path}")
                return False
            fields = schema.getRequired(path)
            if not fields.get("status"):
                continue
            for field in fields.get("data", []):
                if validated.get("data") == "array":
                    sub_path = path + ".items"
                    queue.append(sub_path)
                elif validated.get("data")=="object":
                    sub_path = path + ".properties." + field if path else "properties." + field
                    queue.append(sub_path)
        return True
        
    except Exception as e:
        print("ERROR", e)
        return False