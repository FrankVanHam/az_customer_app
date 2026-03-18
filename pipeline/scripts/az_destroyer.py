import os, shutil

class azDestroyer():
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