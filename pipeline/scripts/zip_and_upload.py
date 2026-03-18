import os, argparse, json
from az_artifacts import azArtifacts
from az_zipper import azZipper

class ZipAndUpload:
    def __init__(self, debug):
        self.reuse_artifacts = '1' in debug
        self.keep_artifacts = '2' in debug

    def go(self, organization, project, feed, artifacts, version, artifact_dir):
        zipper = azZipper(self.reuse_artifacts)
        uploader = azArtifacts(self.reuse_artifacts, organization, project, feed)
        for key, props in artifacts.items():
            product_path = props["product_path"]
            product_name = props["product_name"]
            # Note: use relative path so we can unzip it like that later during deployment
            target = os.path.join(artifact_dir, product_name + ".zip")
            zipper.zip(product_path, target)
            artifact_name = f"{product_name}-{version}.zip"
            uploader.upload(target, artifact_name)

def main():
    parser = argparse.ArgumentParser('Install the core product and other base artifacts')
    parser.add_argument('organization', help='The name of the organisation, like https://dev.azure.com/fabrikamfiber/', type=str)
    parser.add_argument('project', help='The name of the devops project.', type=str)
    parser.add_argument('feed', help='The name of the artifact feed.', type=str)
    parser.add_argument('products_config', help='The name of the products_config json', type=str)
    parser.add_argument('version', help='The version number of the product we are building.', type=str)
    parser.add_argument('artifact_dir', help='The directory to store the artifacts temporary.', type=str)
    parser.add_argument('--debug_settings', help='comma-separated debug settings. 1=reuse artifacts, 2=dont delete artifacts', type=str, required=False, default='')
    args = parser.parse_args()
    
    artifact_dir = os.path.abspath(args.artifact_dir)
    products_config_file = os.path.abspath(args.products_config)
    debug = args.debug_settings.split(',')

    with open(products_config_file) as f:
        products_config = json.load(f)
    
    if len(products_config) == 0:
        print("Detected that no compile is required so nothing will be installed.")
    else:
        zipper = ZipAndUpload(debug)
        zipper.go(args.organization, args.project, args.feed, products_config, args.version, artifact_dir)

if __name__ == '__main__':
    try:
        main()
        exit(0)
    except Exception as e:
        print(e)
        exit(1)