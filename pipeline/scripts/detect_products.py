import sys, os, re, json
import argparse

'''
This script detects products in a directory structure by looking for 'product.def' files.
It reads the first line of each 'product.def' file to extract product names and types.'
'''
class ProductDetector:
    def __init__(self):
        pass

    def detect(self, artifacts, change_file):
        changes = self.read_changes(change_file)
        result = {}
        for key, props in artifacts.items():
            path = os.path.abspath(props.get("product_path"))
            if path and os.path.isdir(path):
                if self.any_changes_in_path(path, changes):
                    result[key] = props
                    print(f"Detected product {key} at {path} with changes.")
                else:
                    print(f"No changes detected for product {key} at {path}, skipping.")
        return result
    
    def read_changes(self, change_file):
        changes = []
        if os.path.isfile(change_file):
            with open(change_file, "r") as f:
                for line in f:
                    changes.append(os.path.abspath(line.strip()))
        else:
            raise Exception(f"Change file {change_file} does not exist.")
        return changes

    def any_changes_in_path(self, product_path, changes):
        for change in changes:
            print(f"Comparing change {change} with product path {product_path}")
            if change.startswith(product_path):
                return True
        return False

def main():
    parser = argparse.ArgumentParser("detect_products will scan through a given 'path' to find Smallworld layered products and set the results as a comma-separated string in the azure variable 'var_name'.")
    parser.add_argument("changes", help="The file containing the changes in the repository", type=str)
    parser.add_argument("artifacts", help="The name of the json file artifacts", type=str)
    parser.add_argument("target", help="The name of the json file to create", type=str)
    args = parser.parse_args()
    
    changes = os.path.abspath(args.changes)
    artifacts_file = os.path.abspath(args.artifacts)
    target = os.path.abspath(args.target)
    
    with open(artifacts_file) as f:
        artifacts = json.load(f)

    detector = ProductDetector()
    results = detector.detect(artifacts, changes)

    with open(target, 'w') as f:
        json.dump(results, f)

if __name__ == "__main__":
    main()