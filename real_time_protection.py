import time
import psutil 
import system_virus_check
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler




def check_virus(item_path):
    virus_result = system_virus_check.convert_hash(item_path.encode('utf-8', 'ignore').decode('utf-8', 'ignore'))
    if virus_result is None:
        return


class FileEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        check_virus(event.src_path)

    def on_modified(self, event):
        if event.is_directory:
            return
        check_virus(event.src_path)

    def on_deleted(self, event):
        if event.is_directory:
            return
        check_virus(event.src_path)


if __name__ == "__main__":
    # Specify the directories to monitor
    directories_to_watch = psutil.disk_partitions(all=True)

    # Create an observer for each directory
    observers = []
    for directory in directories_to_watch:
        observer = Observer()
        event_handler = FileEventHandler()
        observer.schedule(event_handler, path=directory, recursive=True)
        observers.append(observer)

        for observer in observers:
            observer.start()

        try:
            while True:
                time.sleep(1)

        except KeyboardInterrupt:
            for observer in observers:
                observer.stop()

        for observer in observers:
            observer.join()

