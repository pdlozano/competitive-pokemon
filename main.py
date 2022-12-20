from pathlib import Path
from typing import TypedDict
import os
import re
import shutil

current = Path()
files = os.listdir(current)
files = [file for file in files if os.path.isfile(current / file)]

regex = r'((?P<directory>[^-]+)-?(?P<identifier>.+))?\.(?P<extension>.+)'
regex = re.compile(regex)


class File(TypedDict):
    original: str
    extension: str
    directory: str
    identifier: str


def get_file_details(file: str) -> File:
    out = regex.search(file)
    directory = out.group('directory')
    identifier = out.group('identifier')
    extension = out.group('extension')
    
    return {
        'original': file,
        'directory': directory,
        'identifier': identifier,
        'extension': extension,
    }


def process_file(file: File) -> None:
    if file['extension'] == "py" or file['original'] == "index.html":
        return None

    destination_dir = current / file['directory'] / file['identifier']
    destination_dir.mkdir(parents=True, exist_ok=True)

    shutil.move(
        current / file['original'],
        destination_dir / f"index.{file['extension']}",
    )
    return None


def create_link(directory: str, file: str) -> str:
    link = f"/{directory}/{file}"

    return f"<a href='{link}'>{directory} - {file}</a>"


def create_index(path: Path) -> None:
    dirs = os.listdir(path)
    dirs = [directory for directory in dirs if not os.path.isfile(directory)]

    links = []
    for directory in dirs:
        files = os.listdir(directory)
        links = [*links, *[create_link(directory, file) for file in files]]

    links = "</li><li>".join(links)
    links = f"<li>{links}</li>"

    with open("index.html", "w") as file:
        file.write(f"""
            <!doctype html>

            <html lang="en">
                <head>
                    <title>Competitive Pokemon Replays | David Lozano</title>
                </head>

                <body>
                    <h1>Competitive Pokemon Replays</h1>

                    <ul>
                        {links}
                    </ul>
                </body>
            </html>
        """)


if __name__ == "__main__":
    for file in files:
        details = get_file_details(file)
        process_file(details)

    create_index(current)
