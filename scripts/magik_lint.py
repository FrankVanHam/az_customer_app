import sys, os, re, json
import argparse
from az_runner import azRunner

'''
'''
class Linter:
    MAX_NR_OF_FILES = 5
    def __init__(self):
        pass

    def run(self, change_file, lint_jar):
        changes = self.read_changes(change_file)
        batched_changes = [changes[i:i + self.MAX_NR_OF_FILES] for i in range(0, len(changes), self.MAX_NR_OF_FILES)]
        res = 0
        for batch in batched_changes:
            args = ['java', '-jar', lint_jar]
            args.extend(batch)
            process_result = azRunner().run_bare(args)
            res = res or process_result.returncode
        return res

    
    def read_changes(self, change_file):
        changes = []
        if os.path.isfile(change_file):
            with open(change_file, "r") as f:
                for line in f:
                    changes.append(line.strip())
        else:
            raise Exception(f"Change file {change_file} does not exist.")
        return changes
    
def convert_to_exit_code(code, failed_exit_codes):
    if code == 0: return 0
    for allowed in failed_exit_codes:
        if code & allowed: return 1
    return 0

def main():
    parser = argparse.ArgumentParser("Run magik-lint on the files that changed. Run the program in the repository root directory.")
    parser.add_argument("changes", help="The file containing the changes in the repository", type=str)
    parser.add_argument("lint_jar", help="The magik-lint jar file", type=str)
    parser.add_argument("fail_exit_codes", help="A comma separated list of exit codes that trigger a fail", type=str)
    args = parser.parse_args()
    
    changes = os.path.abspath(args.changes)
    lint_jar = os.path.abspath(args.lint_jar)
    failed_exit_codes = map( lambda x : int(x.strip()), args.fail_exit_codes.split(','))

    linter = Linter()
    exit_code = linter.run(changes, lint_jar)
    program_exit_code = convert_to_exit_code(exit_code, failed_exit_codes)
    exit(program_exit_code)
 
if __name__ == "__main__":
    main()