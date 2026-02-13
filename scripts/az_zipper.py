import os
from az_runner import azRunner

class azZipper:
    def __init__(self, reuse_artfacts):
        self.reuse_artfacts = reuse_artfacts

    def unzip(self, the_file, target):
        print(f"Unzipping {the_file} to {target}")
        if os.name == 'nt':
            azRunner().run_bare(['7z', 'x', '-y', '-tzip', '-o'+target, the_file])
        else:
            azRunner().run_bare(['unzip', the_file,'-d', target])
        print(f"Unzipped {the_file} to {target}")

    def zip(self, source, target):
        if not os.path.isfile(target):
            print(f"Zipping {source} to {target}")
            if os.name == 'nt':
                azRunner().run_bare(['7z', 'a', '-y', '-tzip', '-o'+target, target])
            else:
                azRunner().run_bare(['zip', the_file,'-d', target])
            print(f"Zipped {source} to {target}")
        else:
            print(f"Reusing existing zip {target}")