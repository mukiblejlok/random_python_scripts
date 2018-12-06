import requests
from bs4 import BeautifulSoup
import os
import inspect
import argparse


SPECIAL_FOLDER_NAMES = ('name', 'last modified', 'size',
                        'description', 'parent directory')

DOWNLOADABLE_EXTENSIONS = ("csv", "zip", "txt", "pdf")


def process_folder(remote_folder_path, dest_folder_path, **kwargs):
    depth = len(inspect.stack())
    # Check depth
    max_depth = kwargs.get('max_depth', 10)
    if depth > max_depth:
        print("{} ╠═■({}) Too Deep.".format(' ║' * depth,
                                                          max_depth + 1))
        return

    # Create local folder if not exists
    if not os.path.exists(dest_folder_path):
        os.makedirs(dest_folder_path)
    # Read content of folder
    r = requests.get(remote_folder_path)
    soup = BeautifulSoup(r.content, "html5lib")
    # Find all links in folder
    for element in soup.find_all('a'):
        # Exclude all special names form results
        if element.text.lower() in SPECIAL_FOLDER_NAMES:
            continue
        # Get actual link
        link = element.get('href')

        # Check if it is another level folder or a file
        # folder name ends with "/"
        # file name ends with one of DOWNLOADABLE_EXTENSIONS
        if link.endswith("/"):

            print("{} ╠{}".format(" ║" * depth, link))
            # Create new folder paths ...
            new_remote_folder_path = os.path.join(remote_folder_path, link)
            new_dest_folder_path = os.path.join(dest_folder_path, link)
            # ... and go deeper
            process_folder(new_remote_folder_path, new_dest_folder_path,
                           **kwargs)
        # Check if it is a file
        elif link.endswith(DOWNLOADABLE_EXTENSIONS):
            print("{} ╠═{}".format(" ║" * (depth), link),
                  end=' ')
            # Create new file paths ...
            remote_file_path = os.path.join(remote_folder_path, link)
            dest_file_path = os.path.join(dest_folder_path, link)
            # ... and download it
            download_file(remote_file_path, dest_file_path)


def download_file(remote_path, dest_path):
    # check if file already exists
    if os.path.exists(dest_path):
        print(" - Already exists.")
        return None

    try:
        # Download remote data ...
        r = requests.get(remote_path)
        # ... and save it to local destination
        with open(dest_path, 'wb') as wf:
            wf.write(r.content)
            print("  - Saved.")
    except Exception as e:
        print(e)


if __name__ == '__main__':
    # Command Line arguments Creation
    desc = 'Downloads files from remote location.'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-s', dest='source_path', required=True,
                        help='Source Path | REQUIRED')
    parser.add_argument('-d', dest='dest_path', required=True,
                        help='Local Destination path | REQUIRED')
    parser.add_argument('-m', dest='max_depth', required=False, default=3,
                        help='Maximum Search Depth | Default = 3')
    args = parser.parse_args()
    P = {"source_path": args.source_path,
         "dest_path": args.dest_path,
         "max_depth": int(args.max_depth)}

    # Clear Console
    os.system('cls' if os.name == 'nt' else 'clear')
    # Print Configuration
    for k, v in P.items():
        print("{:15}:  {}".format(k, v))

    print()
    print("=" * 20)

    # +1 is because of first
    process_folder(P['source_path'], P['dest_path'], max_depth=P['max_depth'] + 1)
