import os

class JunkRemover:
    def __init__(self):
        self.temp_directories = [
            r'C:\Windows\Temp',
            os.environ.get('TEMP'),
            os.path.join(os.environ.get('USERPROFILE'), 'AppData', 'Local', 'Temp'),
            os.path.join(os.environ.get('USERPROFILE'), 'AppData', 'Local', 'Microsoft', 'Windows', 'INetCache'),
            os.path.join(os.environ.get('USERPROFILE'), 'AppData', 'Local', 'Microsoft', 'Windows', 'Temporary Internet Files'),
            os.path.join(os.environ.get('USERPROFILE'), 'AppData', 'LocalLow', 'Temp'),
            os.path.join(os.environ.get('USERPROFILE'), 'AppData', 'Roaming', 'Microsoft', 'Windows', 'Cookies'),
            os.path.join(os.environ.get('USERPROFILE'), 'AppData', 'Roaming', 'Microsoft', 'Windows', 'Recent'),
        ]

    def remove_temp_files(self):
        for directory in self.temp_directories:
            directory_path = os.path.expandvars(directory)
            if os.path.exists(directory_path):
                self._remove_files(directory_path)

    def _remove_files(self, curr_path):
        try:
            for file_or_dir in os.listdir(curr_path):
                new_path = os.path.join(curr_path, file_or_dir)
                if os.path.isdir(new_path):
                    self._remove_files(new_path)
                elif os.path.isfile(new_path):
                    try:
                        os.remove(new_path)
                        print(f"{new_path} successfully removed.")
                    except Exception as e:
                        print(f"Error removing {new_path}: {e}")
        except Exception as e:
            print(f"Error in {curr_path}: {e}")

if __name__ == "__main__":
    scanner = JunkRemover()
    scanner.remove_temp_files()
