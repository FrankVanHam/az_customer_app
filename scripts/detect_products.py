import sys, os, re, json
import argparse

'''
This script detects products in a directory structure by looking for 'product.def' files.
It reads the first line of each 'product.def' file to extract product names and types.'
'''
class ProductDetector:
    def __init__(self):
        self.changes = []
        self.result = {}

    def detect(self, path, max_depth, adds, change_file):
        self.changes = self.read_changes(change_file)
        self.result = {}
        self.do_detect(path, max_depth)
        self.do_add_adds(adds)
        return self.result
    
    def read_changes(self, change_file):
        changes = []
        if os.path.isfile(change_file):
            with open(change_file, "r") as f:
                for line in f:
                    changes.append(os.path.abspath(line.strip()))
        else:
            raise Exception(f"Change file {change_file} does not exist.")
        return changes
    
    def do_detect(self, path, max_depth):
        if max_depth >= 0:
            #print(f"Scanning path: {path} with depth: {max_depth}")
            found_it = self.detect_file(path)
            if not found_it:
                contents = os.listdir(path)
                for item in contents:
                    item_path =  os.path.join(path, item)
                    if os.path.isdir(item_path):
                        self.do_detect(item_path, max_depth - 1)
    
    def detect_file(self, path):
        item_path = os.path.join(path, "product.def")
        if os.path.isfile(item_path):
            with open(item_path, "r") as f:
                line = f.readline().strip()
                parts = re.split("[ \t]", line)
                if len(parts) >= 2:
                    product_name = parts[0]
                    product_type = parts[-1].lower()
                    if product_name and (product_type == "layered_product"):
                        if self.any_changes_in_path(path):
                            print(f"Detected product {product_name} of type {product_type} at {path} with changes.")
                            self.add_product(path, product_name, product_type)
                        else :
                            print(f"No changes detected for product {product_name} at {path}, skipping.")
    
    def add_product(self, path, product_name, product_type):
        self.result[product_name] = {"product_path": path, 
                                        "product_name": product_name,
                                        "product_type": product_type}
        
    def do_add_adds(self, adds):
        for path in adds:
            if os.path.isdir(path):
                if self.any_changes_in_path(path):
                    self.add_product(path, os.path.basename(path), "additional_repository")
            else:
                print(f"Additional path {path} is not a directory, skipping.")

    def any_changes_in_path(self, product_path):
        for change in self.changes:
            print(f"Comparing change {change} with product path {product_path}")
            if change.startswith(product_path):
                return True
        return False

def main():
    parser = argparse.ArgumentParser("detect_products will scan through a given 'path' to find Smallworld layered products and set the results as a comma-separated string in the azure variable 'var_name'.")
    parser.add_argument("path", help="The path to scan through to find Smallworld layered products", type=str)
    parser.add_argument("depth", help="The maximum depth to scan through", type=int)
    parser.add_argument("adds", help="A list of additional directories in the repository", type=str)
    parser.add_argument("changes", help="The file containing the changes in the repository", type=str)
    parser.add_argument("target", help="The name of the json file to create", type=str)
    args = parser.parse_args()
    
    adds = [os.path.abspath(x.strip()) for x in args.adds.split(',')]
    path = os.path.abspath(args.path)
    changes = os.path.abspath(args.changes)
    target = os.path.abspath(args.target)
    
    detector = ProductDetector()
    results = detector.detect(path, args.depth, adds, changes)
    with open(target, 'w') as f:
        json.dump(results, f)

if __name__ == "__main__":
    main()