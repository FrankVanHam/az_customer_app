import os
from az_runner import azRunner

class azZipper:
    def __init__(self):
        pass
    def unzip(self, the_file, target):
        print(f"Unzipping {the_file} to {target}")
        azRunner().run_bare(['unzip', the_file, target])
