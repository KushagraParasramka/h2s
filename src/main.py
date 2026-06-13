import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.schema_validator import validateSchema


## Load data
candidates = []
cursor = open("public/candidates.jsonl", "r")
for _ in range (100):
    candidate = cursor.readline()
    candidates.append(json.loads(candidate))

print (len(candidates))
for candidate in candidates:
    print(validateSchema(candidate))
