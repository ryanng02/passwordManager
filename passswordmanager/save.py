import json
import os

class Saver:
    def __init__(self, file):
        self.file = file

    def save(self, data):
        with open(self.file, "w") as file: #w is write
            json.dump(data, file, indent=4) #json method dump is to put data in file; indent =4 will format it and make it readable in file

    def read(self):
        with open(self.file, "r") as file: #r is read access only
            data = file.read()

            if os.stat(self.file).st_size == 0: #checking if anything in the file
                return[]
            
            return json.loads(data) #convert data into an array instead of just text