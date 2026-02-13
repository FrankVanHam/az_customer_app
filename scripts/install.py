import os, argparse, json
import subprocess, shutil
import zipfile
from az_runner import azRunner
from az_artifacts import azArtifacts
from az_installer import azInstaller
from az_zipper import azZipper

class Destroyer():
    def empty_directory(self, dir):
        print(f"empting directories (no files) in directory {dir}")
        for filename in os.listdir(dir):
            file_path = os.path.join(dir, filename)
            try:
                if os.path.isdir(file_path):
                    self.remove_directory(file_path, silent=True)
                # if os.path.isfile(file_path) or os.path.islink(file_path):
                #     self.remove_file(file_path, silent=True)
                # elif os.path.isdir(file_path):
                #     self.remove_directory(file_path, silent=True)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
        print(f"emptied directory {dir}")
    def remove_directory(self, dir, silent=False):
        if not silent: print(f"Deleting the directory tree: {dir}")
        shutil.rmtree(dir)
        if not silent: print(f"Deleted the directory tree: {dir}")
    def remove_file(self, file, silent=False):
        if not silent: print(f"Deleting the file: {file}")
        os.unlink(file)
        if not silent: print(f"Deleted the file: {file}")

class Unzipper:
    def unzip(self, source, target):
        with zipfile.ZipFile(source, 'r') as zip_ref:
            zip_ref.extractall(target)

class Deployer:
    def __init__(self, debug):
        self.reuse_artifacts = '1' in debug
        self.keep_artifacts = '2' in debug

    def deploy(self, artifacts, version, base_dir, deploy_dir):
        print(f"deploy {version} on {base_dir} in {deploy_dir}")
        for key, props in artifacts.items():
            product_name = props['product_name']
            product_zip = f"{product_name}.zip"
            artifact_name = f"{product_name}-{version}.zip"
            source_file = os.path.join(base_dir, product_zip)
            if not os.path.isfile(source_file):
                print(f"Downloading {artifact_name} to {base_dir}")
                azArtifacts(self.reuse_artifacts).download('kermit', artifact_name, base_dir, 'SW', source_file)
            else:
                print(f"reusing existing download {source_file}")
            unzip_dir = os.path.join(base_dir, deploy_dir)
            self.unzip(source_file, unzip_dir)
            if not self.keep_artifacts:
                Destroyer().remove_file(source_file)

    def deploy_base(self, base_dir, base_artifacts):
        self.delete_base_dirs(base_dir, base_artifacts)
        for key, props in base_artifacts.items():
            artifact_name = props['artifact_name']
            file_name = props['file_name']
            type = props['product_type']
            source_file = os.path.join(base_dir, file_name)
            ArtifactDownloader(self.reuse_artifacts).download('kermit', artifact_name, base_dir, 'SW', source_file)
            product_path = os.path.join(base_dir, props['product_path'])
            self.deploy_base_product(type, source_file, product_path)
            if not self.keep_artifacts:
                Destroyer().remove_file(source_file)

    def deploy_base_product(self, type, source_file, target_dir):
        match type:
            case 'sw-jar': self.extract_sw_jar(source_file, target_dir)
            case 'zip': self.unzip(source_file, target_dir)
            case _: raise Exception(f"unknown base artifact type {type}")

    def extract_sw_jar(self, source_file, target_dir):
        subprocess.run(['java', '-Daccept_licences=YES', '-Dinstall_language_packs=YES', '-jar', source_file, target_dir])
    
    def unzip(self, source_zip, unzip_dir):
        Unzipper().unzip(source_zip, unzip_dir)

    def delete_base_dirs(self, base_dir, base_artifacts):
        target_dirs = set([v["product_path"] for k,v in base_artifacts.items()])
        for dir in target_dirs:
            dir_to_del = os.path.join(base_dir, dir)
            if os.path.isdir(dir_to_del):
                Destroyer().remove_directory(dir_to_del)

class Installer:
    def __init__(self, debug):
        self.reuse_artifacts = '1' in debug
        self.keep_artifacts = '2' in debug

    def install(self, base_dir, organization, project, feed, artifacts):
        self.download_all(base_dir, organization, project, feed, artifacts)
        self.jar_install(base_dir, self.installable_artifacts_in_order(artifacts))
        self.unzip(base_dir, self.unzippable_artifacts(artifacts))

    def download_all(self, base_dir, organization, project, feed, artifacts):
        arts = azArtifacts(self.reuse_artifacts, organization, project, feed)
        for key, props in artifacts.items():
            if props['product_type'] == 'sw-jar':
                source_file = os.path.join(base_dir, props['file_name'])
                artifact = props['artifact_name']
                arts.download(base_dir, artifact, source_file)
            elif props['product_type'] == 'zip':
                source_file = os.path.join(base_dir, props['file_name'])
                artifact = props['artifact_name']
                arts.download(base_dir, artifact, source_file)
    
    def jar_install(self, base_dir, sorted_artifacts: list):
        installer = azInstaller()
        for props in sorted_artifacts:
            source_file = os.path.join(base_dir, props['file_name'])
            target = os.path.join(base_dir, props["product_path"])
            installer.install(source_file, target)
    
    def unzip(self, base_dir, artifacts: list):
        zipper = azZipper()
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
        installer.install(base_dir, args.organization, args.project, args.feed, artifacts)

if __name__ == '__main__':
    try:
        main()
    except Exception as e: print(e)