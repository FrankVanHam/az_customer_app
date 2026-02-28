import os
from az_runner import azRunner

class azInstaller:
    def install(self, the_file, target):
        print(f"Installing {the_file}")
        if os.name == 'nt':
            azRunner().run_bare(['java', '-Daccept_licences=YES', '-Dinstall_language_packs=YES',  '-jar', the_file, target])
        else:
            azRunner().run_bare(['sudo', 'java', '-Daccept_licences=YES', '-Dinstall_language_packs=YES',  '-jar', the_file, target, 'vsts', 'vsts'])
        print(f"Installed {the_file}")
