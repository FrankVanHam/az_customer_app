import os
from az_runner import azRunner

class azArtifacts:
    def __init__(self, reuse_artifacts):
        self.reuse_artifacts = reuse_artifacts
    def download(self, base_dir, organization, project, feed, artifact, source_file):
        if not os.path.isfile(source_file):
            print(f"Downloading {artifact} to {source_file}")
            print(f"parameters: {[feed, artifact, base_dir, project]}")
            azRunner().run(['artifacts', 'universal', 'download', '--feed', feed, '--name', artifact, '--path', base_dir, '--version', '"*"', '--project', project, '--scope', 'project', '--organization', organization]) 
        else:
            print(f"reusing existing download {source_file}")