import os, argparse, json
from az_artifacts import azArtifacts
from az_installer import azInstaller
from az_zipper import azZipper

class Installer:
    def __init__(self, debug):
        self.reuse_artifacts = '1' in debug
        self.keep_artifacts = '2' in debug

    def install(self, base_dir, organization, project, feed, artifacts, sw_version):
        self.download_all(base_dir, organization, project, feed, artifacts, sw_version)
        self.jar_install(base_dir, self.installable_artifacts_in_order(artifacts))
        self.unzip(base_dir, self.unzippable_artifacts(artifacts))

    def download_all(self, base_dir, organization, project, feed, artifacts, sw_version):
        arts = azArtifacts(self.reuse_artifacts, organization, project, feed)
        for key, props in artifacts.items():
            source_file = os.path.join(base_dir, props['file_name'])
            artifact = props['artifact_name']
            arts.download(base_dir, artifact, source_file, sw_version)
    
    def jar_install(self, base_dir, sorted_artifacts: list):
        installer = azInstaller()
        for props in sorted_artifacts:
            source_file = os.path.join(base_dir, props['file_name'])
            target = os.path.join(base_dir, props["product_path"])
            installer.install(source_file, target)
    
    def unzip(self, base_dir, artifacts: list):
        zipper = azZipper(self.reuse_artifacts)
        for props in artifacts:
            source_file = os.path.join(base_dir, props['file_name'])
            target = os.path.join(base_dir, props["product_path"])
            zipper.unzip(source_file, target)
             
    def installable_artifacts_in_order(self, artifacts: dict):
        return list(filter(lambda x: x['product_type'] == 'sw-jar', sorted( artifacts.values(), key=lambda x: x['order'])))
    
    def unzippable_artifacts(self, artifacts: dict):
        return list(filter(lambda x: x['product_type'] == 'zip', artifacts.values()))

def main():
    parser = argparse.ArgumentParser('Install the core product and other base artifacts')
    parser.add_argument('base_dir', help='The base directory of the install.', type=str)
    parser.add_argument('organization', help='The name of the organisation, like https://dev.azure.com/fabrikamfiber/', type=str)
    parser.add_argument('project', help='The name of the devops project.', type=str)
    parser.add_argument('feed', help='The name of the artifact feed.', type=str)
    parser.add_argument('artifacts', help='The name of the json file base_artifacts', type=str)
    parser.add_argument('products_config', help='The name of the products_config json', type=str)
    parser.add_argument('sw_version', help='The version of the base products to download', type=str)
    parser.add_argument('--debug_settings', help='comma-separated debug settings. 1=reuse artifacts, 2=dont delete artifacts', type=str, required=False, default='')
    args = parser.parse_args()
    
    base_dir = os.path.abspath(args.base_dir)
    artifacts_file = os.path.abspath(args.artifacts)
    products_config_file = os.path.abspath(args.products_config)
    debug = args.debug_settings.split(',')

    with open(artifacts_file) as f:
        artifacts = json.load(f)
    with open(products_config_file) as f:
        products_config = json.load(f)
    
    if len(products_config) == 0:
        print("Detected that no compile is required so nothing will be installed.")
    else:
        installer = Installer(debug)
        installer.install(base_dir, args.organization, args.project, args.feed, artifacts, args.sw_version)

if __name__ == '__main__':
    try:
        main()
        exit(0)
    except Exception as e:
        print(e)
        exit(1)