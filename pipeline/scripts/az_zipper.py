import os
from az_runner import azRunner

class azZipper:
    def __init__(self, reuse_artfacts):
        self.reuse_artfacts = reuse_artfacts

    def unzip(self, source_zip, target_dir):
        print(f"Unzipping {source_zip} to {target_dir}")
        if os.name == 'nt':
            azRunner().run_bare(['7z', 'x', '-y', '-tzip', '-o'+target_dir, source_zip])
        else:
            azRunner().run_bare(['unzip', source_zip,'-d', target_dir])
        print(f"Unzipped {source_zip} to {target_dir}")

    def zip(self, source_dir, target_zip):
        if not os.path.isfile(target_zip):
            print(f"Zipping {source_dir} to {target_zip}")
            if os.name == 'nt':
                azRunner().run_bare(['7z', 'a', '-y', '-tzip', '-o'+target_zip, source_dir])
            else:
                azRunner().run_bare(['zip', '-r', target_zip, source_dir])
            print(f"Zipped {source_dir} to {target_zip}")
        else:
            print(f"Reusing existing zip {target_zip}")