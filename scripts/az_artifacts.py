import os, base64, requests, json
from az_runner import azRunner

class azArtifacts:
    def __init__(self, reuse_artifacts, organization, project, feed):
        self.reuse_artifacts = reuse_artifacts
        self.organization = organization
        self.project = project
        self.feed = feed
    def download(self, base_dir, artifact_name, source_file):
        if (not self.reuse_artifacts) or (not os.path.isfile(source_file)):
            print(f"Downloading {artifact_name} to {source_file}")
            print(f"parameters: {[self.organization, self.project, self.feed, base_dir, artifact_name]}")
            azRunner().run(['artifacts', 'universal', 'download', '--feed', self.feed, '--name', artifact_name, '--path', base_dir, '--version', '*', '--project', self.project, '--scope', 'project', '--organization', self.organization]) 
        else:
            print(f"reusing existing download {source_file}")

    def upload(self, source, artifact_name):
        print(f"Getting the new vresion for {artifact_name}")
        new_version = self.next_version(artifact_name)
        print(f"Uploading {source} to {artifact_name} with version {new_version}")
        print(f"parameters: {[self.organization, self.project, self.feed, source, artifact_name]}")
        azRunner().run(['artifacts', 'universal', 'publish', '--feed', self.feed, '--name', artifact_name, '--path', source, '--version', new_version, '--project', self.project, '--scope', 'project', '--organization', self.organization]) 

    def bare_organization(self):
        parts = self.organization.split('/')
        return parts[-1] if parts[-1] != '' else parts[-2]
    
    def auth_headers(self):
        pat = os.environ['AZURE_DEVOPS_EXT_PAT']
        encoded_pat = base64.b64encode(f":{pat}".encode()).decode()
        return {'Authorization': 'Basic '+ encoded_pat}

    def artifact_details(self, artifact_name):
        test_api_url = f'https://feeds.dev.azure.com/{self.bare_organization()}/{self.project}/_apis/packaging/Feeds/{self.feed}/packages?api-version=6.0-preview.1'
        response = requests.get(test_api_url, headers=self.auth_headers())
        if response.status_code == 200:
            js = json.loads(response.text)
            for v in js.get('value',[]):
                if v['name'] == artifact_name:
                    return v
            return None
        raise Exception(f"Failure to get the artifact details in {self.feed} in {response.text}")
    
    def next_version(self, artifact_name):
        details = self.artifact_details(artifact_name)
        if details:
            version = details['versions'][0]['version']
            parts = version.split('.')
            new_version = f'{parts[0]}.{parts[1]}.{int(parts[2])+1}'
        else:
            new_version = '1.0.0'
        return new_version