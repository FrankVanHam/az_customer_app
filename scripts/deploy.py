import os, argparse, json
import subprocess, shutil
import zipfile

class azRunner:
    def run(self, p_args):
        this_dir = os.path.dirname(os.path.abspath(__file__))
        args = [os.path.join(this_dir, 'run-az.bat')]
        args.extend(p_args)
        subprocess.run(args) 

class ArtifactDownloader:
    def __init__(self, reuse_artifacts):
        self.reuse_artifacts = reuse_artifacts
    def download(self, feed, artifact_name, path, project, source_file):
        if not os.path.isfile(source_file):
            print(f"Downloading {artifact_name} to {source_file}")
            azRunner().run(['artifacts', 'universal', 'download', '--feed', feed, '--name', artifact_name, '--path', path, '--version', '*', '--project', project, '--scope', 'project']) 
        else:
            print(f"reusing existing download {source_file}")


class Destroyer():
    def empty_directory(self, dir):
        print(f"empting directory {dir}")
        for filename in os.listdir(dir):
            file_path = os.path.join(dir, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    self.remove_file(file_path, silent=True)
                elif os.path.isdir(file_path):
                    self.remove_directory(file_path, silent=True)
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
                ArtifactDownloader(self.reuse_artifacts).download('kermit', artifact_name, base_dir, 'SW', source_file)
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

def main():
    parser = argparse.ArgumentParser('Deploy the artifacts in the target folder')
    parser.add_argument('artifacts', help='The name of the json file artifacts', type=str)
    parser.add_argument('version', help='The version of the build that is used to store the artifacts', type=str)
    parser.add_argument('base_dir', help='The base directory of the deployment.', type=str)
    parser.add_argument('deploy_dir', help='The sub directory artifact extract.', type=str)
    parser.add_argument('base_artifacts', help='The name of the json file with base artifacts', type=str)
    parser.add_argument('base_deploy', help='should the base also be deployed? (true/false).', type=bool)
    parser.add_argument('--debug_settings', help='comma-separated debug settings. 1=reuse artifacts, 2=dont delete artifacts', type=str, required=False, default='')
    args = parser.parse_args()
    
    exit()
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
        Destroyer().empty_directory(base_dir)
        deployer.deploy_base(base_dir, base_artifacts)
    deployer.deploy(artifacts, args.version, base_dir, args.deploy_dir)

if __name__ == '__main__':
    main()