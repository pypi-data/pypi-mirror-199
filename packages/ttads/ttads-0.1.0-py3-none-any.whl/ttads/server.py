import re
import threading
import zipfile
from datetime import datetime
from io import BytesIO
from pathlib import Path
from time import sleep

import click
import yaml
from flask import Flask, send_file

from tunnel import Tunnel

ENCODING = 'UTF-8'
PATTERN_VERSION = r'(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:-(?P<pre>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?(?:\+(?P<build>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?'


class TappServer:

    def __init__(self, project_data, port=8080):

        self.port = port
        self.project_data = project_data
        self.app = Flask(self.__class__.__name__)
        self.app.route('/<download_name>')(self.serve_tapp)
        self.thread = threading.Thread(target=self.start_app)
        self.start()

    def start(self):
        self.thread.start()

    def start_app(self):
        self.app.run(port=self.port)

    def close(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.close()

    def wait(self):
        while self.thread.is_alive():
            sleep(1)

    def serve_tapp(self, download_name):

        name = Path(download_name).stem

        if name not in self.project_data:
            return f'Unknown project "{name}"'

        path = Path(self.project_data[name]['path'])

        byte_buffer = BytesIO()
        with zipfile.ZipFile(byte_buffer, mode='w') as zip_file:

            for file_path in path.iterdir():

                if not file_path.is_file():
                    continue

                text = self.update_version(name, file_path)
                if text is not None:
                    zip_file.writestr(file_path.name, text.encode(ENCODING))
                else:
                    zip_file.write(file_path, arcname=file_path.name)

        byte_buffer.seek(0)

        response = send_file(byte_buffer, as_attachment=True, download_name=download_name)
        return response

    def version_replacer(self, match):
        build = datetime.now().strftime("%Y.%m.%d-%H.%M.%S")
        version_mmp = '.'.join(match.group(name) for name in ['major', 'minor', 'patch'])
        version = '+'.join(['development', build])
        version = '-'.join([version_mmp, version])
        text_new = match.group(0).replace(match.group(1), version)
        return text_new

    def update_version(self, name, path):

        project_data = self.project_data[name]
        path_rel = str(path.relative_to(project_data['path']))
        version_updates = project_data.get('version_updates', {})

        if path_rel not in version_updates:
            return

        text_old = path.read_text(encoding=ENCODING)
        pattern = version_updates[path_rel]
        pattern = pattern.format(version=PATTERN_VERSION)
        text = re.sub(pattern, self.version_replacer, text_old)
        return text

def start(project_data, port):
    with TappServer(project_data, port) as tapp_server:
        with Tunnel(port) as tunnel:
            for name in tapp_server.project_data:
                msg = f'Serving project "{name}": `tasmota.urlfetch("{tunnel.tunnel.public_url}/{name}.tapp")`'
                print(msg)
            tapp_server.wait()


@click.command()
@click.option('--project', '-p', multiple=True, metavar='PATH')
@click.option('--port', '-pt', default=8080, show_default=True)
def start_cli(project, port):
    projects = project
    project_data = {}
    for project in projects:
        if ':' in project:
            name, path = project.split(':')
        else:
            name, path = Path(project).stem, project

        path = Path(path)
        if (path_config := path / 'ttads.yml').exists():
            data = yaml.safe_load(path_config.read_text())
            data['path'] = path / data['path']
        else:
            data = {'path': path.absolute(), 'name': name}

        data.setdefault('name', name)

        project_data[name] = data

    start(project_data, port)


if __name__ == '__main__':
    start_cli()
