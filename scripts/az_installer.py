import os
from az_runner import azRunner

class azazInstaller:
    def __init__(self):
        pass
    def install(self, the_file, target):
        print(f"Installing {the_file}")
        azRunner().run_bare(['sudo', 'java', '-Daccept_licences=YES', '-Dinstall_language_packs=YES',  '-jar', the_file, target, 'vsts', 'vsts'])
