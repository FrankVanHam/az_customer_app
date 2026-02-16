import os, argparse, json
import subprocess, shutil
import zipfile
from az_artifacts import azArtifacts
from az_installer import azInstaller
from az_zipper import azZipper
from az_destroyer import azDestroyer

class Deployer:
    def __init__(self, debug):
        self.reuse_artifacts = '1' in debug
        self.keep_artifacts = '2' in debug

    def deploy(self, organization, project, feed, artifacts_config, version, base_dir, deploy_dir):
        print(f"deploy {version} on {base_dir} in {deploy_dir}")
        destroyer = azDestroyer()
        artifacts = azArtifacts(self.reuse_artifacts, organization, project, feed)
        for key, props in artifacts_config.items():
            product_name = props['product_name']
            product_zip = f"{product_name}.zip"
            artifact_name = f"{product_name}-{version}.zip"
            source_file = os.path.join(base_dir, product_zip)
            if not os.path.isfile(source_file):
                print(f"Downloading {artifact_name} to {base_dir}")
                artifacts.download(base_dir, artifact_name, source_file)
            else:
                print(f"reusing existing download {source_file}")
            unzip_dir = os.path.join(base_dir, deploy_dir)
            self.unzip(source_file, unzip_dir)
            if not self.keep_artifacts:
                destroyer.remove_file(source_file)

    def deploy_base(self, organization, project, feed, base_dir, base_artifacts):
        destroyer = azDestroyer()
        artifacts = azArtifacts(self.reuse_artifacts, organization, project, feed)
        self.delete_base_dirs(base_dir, base_artifacts)
        for key, props in base_artifacts.items():
            artifact_name = props['artifact_name']
            file_name = props['file_name']
            type = props['product_type']
            source_file = os.path.join(base_dir, file_name)
            artifacts.download( base_dir, artifact_name, source_file)
            product_path = os.path.join(base_dir, props['product_path'])
            self.deploy_base_product(type, source_file, product_path)
            if not self.keep_artifacts:
                destroyer.remove_file(source_file)

    def deploy_base_product(self, type, source_file, target_dir):
        match type:
            case 'sw-jar': self.extract_sw_jar(source_file, target_dir)
            case 'zip': self.unzip(source_file, target_dir)
            case _: raise Exception(f"unknown base artifact type {type}")

    def extract_sw_jar(self, source_file, target_dir):
        azInstaller().install(source_file, target_dir)
    
    def unzip(self, source_zip, unzip_dir):
        azZipper(self.reuse_artifacts).unzip(source_zip, unzip_dir)

    def delete_base_dirs(self, base_dir, base_artifacts):
        destroyer = azDestroyer()
        target_dirs = set([v["product_path"] for k,v in base_artifacts.items()])
        for dir in target_dirs:
            dir_to_del = os.path.join(base_dir, dir)
            if os.path.isdir(dir_to_del):
                destroyer.remove_directory(dir_to_del)

def main():
    parser = argparse.ArgumentParser('Deploy the artifacts in the target folder')
    parser.add_argument('organization', help='The name of the organisation, like https://dev.azure.com/fabrikamfiber/', type=str)
    parser.add_argument('project', help='The name of the devops project.', type=str)
    parser.add_argument('feed', help='The name of the artifact feed.', type=str)
    parser.add_argument('artifacts', help='The name of the json file artifacts', type=str)
    parser.add_argument('version', help='The version of the build that is used to store the artifacts', type=str)
    parser.add_argument('base_dir', help='The base directory of the deployment.', type=str)
    parser.add_argument('deploy_dir', help='The sub directory artifact extract.', type=str)
    parser.add_argument('base_artifacts', help='The name of the json file with base artifacts', type=str)
    parser.add_argument('base_deploy', help='should the base also be deployed? (true/false).', type=bool)
    parser.add_argument('--debug_settings', help='comma-separated debug settings. 1=reuse artifacts, 2=dont delete artifacts', type=str, required=False, default='')
    args = parser.parse_args()
    
    artifacts_file = os.path.abspath(args.artifacts)
    base_artifacts_file = os.path.abspath(args.base_artifacts)
    base_dir = os.path.abspath(args.base_dir)
    debug = args.debug_settings.split(',')
    
    with open(artifacts_file) as f:
        artifacts = json.load(f)
    with open(base_artifacts_file) as f:
        base_artifacts = json.load(f)
    
    deployer = Deployer(debug)
    if args.base_deploy:
        print(f"base deploy enabled, first deleting the entire base then installing the base and the products")
        azDestroyer().empty_directory(base_dir)
        deployer.deploy_base(args.organization, args.project, args.feed, base_dir, base_artifacts)
    deployer.deploy(args.organization, args.project, args.feed, artifacts, args.version, base_dir, args.deploy_dir)

if __name__ == '__main__':
    main()