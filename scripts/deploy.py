import os, argparse, json



class Deployer:
    def deploy(self, artifacts, version, target):
        print(f"deploy {version} on {target}")

def main():
    parser = argparse.ArgumentParser("Deploy the artifacts in the target folder")
    parser.add_argument("artifacts", help="The name of the json file artifacts", type=str)
    parser.add_argument("version", help="The version of the build that is used to store the artifacts", type=str)
    parser.add_argument("target", help="The target directory to store the artifacts", type=str)
    args = parser.parse_args()
    
    artifacts_file = os.path.abspath(args.artifacts)
    target = os.path.abspath(args.target)
    
    with open(artifacts_file) as f:
        artifacts = json.load(f)

    deployer = Deployer()
    deployer.deploy(artifacts, parser.version, target)

if __name__ == "__main__":
    main()