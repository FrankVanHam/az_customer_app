import os, argparse, json
from az_runner import azRunner

class Reporter:
    def go(self, jar, exec, target, products_config):
        args = ['java', '-jar', jar, '--jacoco-file', exec, '--jacoco-xml', target]
        for key, props in products_config.items():
            product_path = os.path.abspath(props["product_path"])
            args.extend(['--product-path', product_path])
        azRunner().run_bare(args)
        #    java -jar $(Pipeline.Workspace)/$(JACOCO_REPORTER_JAR) --product-path /home/vsts/work/1/s/customer_engine_prd --product-path /home/vsts/work/1/s/customer_prd --jacoco-file  $(Pipeline.Workspace)/jacoco.exec --jacoco-xml  $(Pipeline.Workspace)/coverage_results.xml

def main():
    parser = argparse.ArgumentParser('Run jacoco reporter to generate code coverage report')
    parser.add_argument('jar', help='The location of the jacoco reporter jar file', type=str)
    parser.add_argument('exec', help='The loation of the jacoco.exec file', type=str)
    parser.add_argument('target', help='The target location of the XML file.', type=str)
    parser.add_argument('products_config', help='The name of the products_config json', type=str)
    args = parser.parse_args()
    
    target = os.path.abspath(args.target)
    products_config_file = os.path.abspath(args.products_config)

    with open(products_config_file) as f:
        products_config = json.load(f)
    
    if len(products_config) == 0:
        print("Detected that no products have been tested so no report is created.")
    else:
        reporter = Reporter()
        reporter.go(args.jar, args.exec, target, products_config)

if __name__ == '__main__':
    try:
        main()
        exit(0)
    except Exception as e:
        print(e)
        exit(1)