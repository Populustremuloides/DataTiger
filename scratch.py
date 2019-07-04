import os
import time

filename = os.path.join(os.getcwd(), "DatabaseName.txt")
with open(filename, "r") as file:
    line = file.readline()

    print(line)
    time.sleep(5.5)