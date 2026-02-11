import os
from az_runner import azRunner

class azArtifacts:
    def __init__(self, reuse_artifacts):
        self.reuse_artifacts = reuse_artifacts
    def download(self, feed, artifact_name, path, project, source_file):
        if not os.path.isfile(source_file):
            print(f"Downloading {artifact_name} to {source_file}")
            print(f"parameters: {[feed, artifact_name, path, project]}")
            azRunner().run(['artifacts', 'universal', 'download', '--feed', feed, '--name', artifact_name, '--path', path, '--version', '*', '--project', project, '--scope', 'project']) 
        else:
            print(f"reusing existing download {source_file}")