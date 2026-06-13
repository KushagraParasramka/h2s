import sys
import os
import json
from typing import Optional, Any

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class Schema:
    def __init__(self):
        schemaFile = open("public/candidate_schema.json")
        self.schema = json.loads(schemaFile.read())

    def printSchema(self):
        print(self.schema)

    def getRequired(self, path: str = "")-> dict[str, Any]:
        if not path:
            nesting = []
        else:
            nesting = path.split(".")
        try:
            tempObj = self.schema
            for obj in nesting:
                tempObj = tempObj.get(obj)
            requiredFields = tempObj.get("required")
            return {
                "status": True,
                "data": requiredFields
            }

        except Exception as e:
            print("ERROR ========> getREquired ======> ", e)
            return {
                "status": False,
                "data": None
            }
        
    def checkField(self, path: str = None, candidate: dict = {})-> dict:
        if not path:
            nesting = []
        else:
            nesting = path.split(".")
        try:
            tempObj = self.schema
            for obj in nesting:
                tempObj = tempObj.get(obj)
                candidate = candidate.get(obj)
            if candidate:
                return {
                    "status": True,
                    "data": tempObj
                }
            else:
                return {
                    "status": False,
                    "data": None
                }

        except Exception as e:
            print("ERROR ========> checkField =======>", e)
            return False
        
    def validateType(self, obj: Any = None)-> dict:
        try:
            if not obj:
                print("None object")
                return {
                    "status": False,
                    "data": None
                }
            dtype = type(obj)
            if not dtype:
                print("No type object found")
                return {
                    "status": False,
                    "data": None
                }
            
            match dtype:
                case "string":
                    pass
                case "integer":
                    pas
                case "object":
                    pass
                case "enum":
                    pass

        except Exception as e:
            print("ERROR ========> validateType ======> ", e)
            return {
                "status": False,
                "data": None
            }