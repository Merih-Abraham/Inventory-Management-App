import json
import os

from data import personnel, stock

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

print(f"Base directory : \n{BASE_DIR}")

try:
    os.mkdir(os.path.join(BASE_DIR, "data"))
except Exception as e:
    print(f"Unable to create a directory name data : {e}")


if __name__ == "__main__":
    with open(os.path.join(BASE_DIR, "data/personnel.json"), "w") as file:
        file.write(json.dumps(personnel))
    with open(os.path.join(BASE_DIR, "data/stock.json"), "w") as file:
        file.write(json.dumps(stock))