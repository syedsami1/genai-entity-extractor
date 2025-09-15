import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from entity_extractor import extract_entities
from db import insert_data, init_db

WATCH_FOLDER = "watch_folder"

class Handler(FileSystemEventHandler):
    def on_created(self, event):
        if event.src_path.endswith(".txt"):
            with open(event.src_path, "r", encoding="utf-8") as f:
                text = f.read()
            entities = extract_entities(text)
            filename = event.src_path.split("/")[-1]
            insert_data(filename, entities["persons"], entities["dates"])
            print(f"✅ Processed {filename}: {entities}")

def start_watching():
    observer = Observer()
    observer.schedule(Handler(), WATCH_FOLDER, recursive=False)
    observer.start()
    print(f"👀 Watching folder: {WATCH_FOLDER}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    init_db()
    start_watching()
