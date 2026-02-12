import subprocess, os, stat

class azRunner:
    def run(self, p_args):
        this_dir = os.path.dirname(os.path.abspath(__file__))
        if os.name == 'nt':
            args = [os.path.join(this_dir, 'run-az.bat')]
        else:
            sh_file = os.path.join(this_dir, 'run-az.sh')
            if not os.access(sh_file, os.X_OK):
                print(f"the file {sh_file} is not executable, making it executable for the owner")
                st = os.stat(sh_file)
                os.chmod(sh_file, st.st_mode | stat.S_IEXEC)
            args = ["sh", sh_file]
        args.extend(p_args)
        subprocess.run(args)

    def run_bare(self, args):
        subprocess.run(args)