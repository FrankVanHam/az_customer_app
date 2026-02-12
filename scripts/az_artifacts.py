import os
from az_runner import azRunner

class azArtifacts:
    def __init__(self, reuse_artifacts, organization, project, feed):
        self.reuse_artifacts = reuse_artifacts
        self.organization = organization
        self.project = project
        self.feed = feed
    def download(self, base_dir, artifact, source_file):
        if (not self.reuse_artifacts) or (not os.path.isfile(source_file)):
            print(f"Downloading {artifact} to {source_file}")
            print(f"parameters: {[self.organization, self.project, self.feed, base_dir, artifact]}")
            azRunner().run(['artifacts', 'universal', 'download', '--feed', self.feed, '--name', artifact, '--path', base_dir, '--version', '*', '--project', self.project, '--scope', 'project', '--organization', self.organization]) 
        else:
            print(f"reusing existing download {source_file}")