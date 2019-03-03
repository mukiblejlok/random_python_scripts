import os
import requests


def download_file(remote_path, dest_path):
    # check if file already exists
    if os.path.exists(dest_path):
        return None

    # Download remote data ...
    r = requests.get(remote_path)
    # ... and save it to local destination
    with open(dest_path, 'wb') as wf:
        wf.write(r.content)
        print("  - Saved.")

