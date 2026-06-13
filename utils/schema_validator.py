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
            path = queue.pop[0]
            result = schema.checkField(path = path, candidate = candidate)
        
    except Exception as e:
        return False