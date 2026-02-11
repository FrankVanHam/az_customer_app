import subprocess, os

class azRunner:
    def run(self, p_args):
        this_dir = os.path.dirname(os.path.abspath(__file__))
        if os.name == 'nt':
            args = [os.path.join(this_dir, 'run-az.bat')]
        else:
            args = [os.path.join(this_dir, 'sudo', 'run-az.sh')]
        args.extend(p_args)
        subprocess.run(args)