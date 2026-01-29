import sys, os, re, json
import argparse

'''
This script detects products in a directory structure by looking for 'product.def' files.
It reads the first line of each 'product.def' file to extract product names and types.'
'''
class ProductDetector:
    def __init__(self):
        self.result = {}

    def detect(self, path, max_depth):
        self.result = {}
        self.do_detect(path, max_depth)
        return self.result
    
    def do_detect(self, path, max_depth):
        print(f"Scanning path: {path} with depth: {max_depth}")
        if max_depth >= 0:
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
                        self.result[product_name] = {"product_path": path, 
                                                     "product_name": product_name,
                                                     "product_type": product_type}

def main():
    parser = argparse.ArgumentParser("detect_products will scan through a given 'path' to find Smallworld layered products and set the results as a comma-separated string in the azure variable 'var_name'.")
    parser.add_argument("path", help="The path to scan through to find Smallworld layered products", type=str)
    parser.add_argument("depth", help="The maximum depth to scan through", type=int)
    parser.add_argument("var_name", help="The name of the variable to set in the azure pipeline", type=str)
    args = parser.parse_args()
    
    path = os.path.abspath(args.path)
    detector = ProductDetector()
    results = detector.detect(path, args.depth)
    result_string = json.dumps(results)
    print(f"##vso[task.setvariable variable={args.var_name};;isOutput=true]{result_string}")

if __name__ == "__main__":
    main()