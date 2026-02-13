import os
from az_runner import azRunner

class azZipper:
    def __init__(self):
        pass
    def unzip(self, the_file, target):
        print(f"Unzipping {the_file} to {target}")
        if os.name == 'nt':
            print(['7z', 'x', '-o'+target, the_file])
            azRunner().run_bare(['7z', 'x', '-y', '-o'+target, the_file])
        else:
            azRunner().run_bare(['unzip', the_file,'-d', target])
        print(f"Unzipped {the_file} to {target}")
