import sys
import os
import json
from typing import Optional, Any

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.enum import DataType

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
            requiredFields = tempObj.get("required", None)
            if not requiredFields:
                return {
                    "status": False,
                    "data": None
                }
            return {
                "status": True,
                "data": requiredFields
            }

        except Exception as e:
            print("ERROR ========> getRequired ======> ", e)
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
                if obj != "properties":
                    candidate = candidate.get(obj)
            if candidate:
                return {
                    "status": True,
                    "data": candidate,
                    "schema": tempObj
                }
            else:
                return {
                    "status": False,
                    "data": None,
                    "schema": None
                }

        except Exception as e:
            print("ERROR ========> checkField =======>", e)
            return {
                "status": False,
                "data": None,
                "schema": None
            }
        
    def validateType(self, obj: dict = {}, schema: dict|None = None)-> dict:
        if not obj or not type(obj):
            print("None object")
            return {
                "status": False,
                "data": None
            }
        if not schema or not schema.get("type", None):
            print("No schema")
            return {
                "status": True,
                "data": None
            }
        try:
            dtype = type(obj).__name__
            schemaType = schema.get("type", None)
            if dtype not in DataType[schemaType]:
                return {
                    "status": False,
                    "data": None
                }
            
            match schemaType:
                case "string":
                    return {
                        "status": True,
                        "data": "string"
                    }
                case "integer":
                    return {
                        "status": True,
                        "data": "integer"
                    }
                case "object":
                    return {
                        "status": True,
                        "data": "object"
                    }
                case "enum":
                    return {
                        "status": True,
                        "data": "enum"
                    }
                case "array":
                    return {
                        "status": True,
                        "data": "array"
                    }
                case "number":
                    return {
                        "status": True,
                        "data": "number"
                    }
                case "boolean":
                    return {
                        "status": True,
                        "data": "boolean"
                    }

        except Exception as e:
            print("ERROR ========> validateType ======> ", e)
            return {
                "status": False,
                "data": None
            }