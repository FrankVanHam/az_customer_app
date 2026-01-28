import sys, os, re
import argparse

'''
This script detects products in a directory structure by looking for 'product.def' files.
It reads the first line of each 'product.def' file to extract product names and types.'
'''
class ProductDetector:
    def __init__(self):
        self.result = []

    def detect(self, path, max_depth, scope):
        self.result = []
        self.do_detect(path, max_depth, scope)
        return self.result
    
    def do_detect(self, path, max_depth, scope):
        if max_depth == 0:
            return
        contents = os.listdir(path)
        for item in contents:
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                res = self.detect_file(item_path, scope)
                if res:
                    self.result.append(res)
                self.do_detect(item_path, max_depth - 1, scope)
            else:
                pass
    
    def detect_file(self, path, scope):
        item_path = os.path.join(path, "product.def")
        if os.path.isfile(item_path):
            with open(item_path, "r") as f:
                line = f.readline().strip()
                parts = re.split("[ \t]", line)
                if len(parts) == 2:
                    product_name = parts[0]
                    product_type = parts[1].lower()
                    if product_name and (product_type == "layered_product"):
                        if product_name:
                            if scope == "name":
                                return product_name
                            elif scope == "path":
                                return path
                            else:
                                return None
                return None
        return None

def main():
    parser = argparse.ArgumentParser("detect_products will scan through a given 'path' to find Smallworld layered products and set the results as a comma-separated string in the azure variable 'var_name'.")
    parser.add_argument("path", help="The path to scan through to find Smallworld layered products", type=str)
    parser.add_argument("depth", help="The maximum depth to scan through", type=int)
    parser.add_argument("scope", help="The scope of the detection result: name or path", type=str)
    parser.add_argument("var_name", help="The name of the variable to set in the azure pipeline", type=str)
    args = parser.parse_args()
    
    path = os.path.abspath(args.path)
    detector = ProductDetector()
    results = detector.detect(path, args.depth, args.scope)
    result_string = ",".join(results)
    print(f"##vso[task.setvariable variable={args.var_name};]{result_string}")


if __name__ == "__main__":
    main()