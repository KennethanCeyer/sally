import os
import shutil
import tarfile
import zipfile

import requests
from tqdm import tqdm

from sally.logger import LogLevel, log
import inquirer


def cleanup_path(dir_path):
    log('clean-up `%s`' % dir_path, LogLevel.INFO)
    if os.path.isdir(dir_path):
        shutil.rmtree(dir_path)
    os.makedirs(dir_path, exist_ok=True)
    log('clean-up is completed `%s`' % dir_path, LogLevel.SUCCESS)


def download_link(path, link):
    return download_request(path, link)


def download_request(path, link):
    response = requests.get(link, stream=True)
    total_length = response.headers.get('content-length')
    log('start to download (size: %s bytes)' % total_length, LogLevel.INFO)

    questions = [
        inquirer.Confirm('install', message='continue to install dataset on your disk?', default = True)
    ]
    answers = inquirer.prompt(questions)
    if not answers['install']:
        log('install process is canceled', LogLevel.ERROR)
        return -1

    with tqdm(total=100) as pbar:
        with open(path, 'wb') as f:
            if total_length is None:
                f.write(response.content)
            else:
                total_length = int(total_length)
                for data in response.iter_content(chunk_size=4096):
                    f.write(data)
                    pbar.update(len(data) / total_length * 100)

    log('download is completed', LogLevel.SUCCESS)


def unzip(path):
    log('extract download file `%s`' % path, LogLevel.INFO)
    if path.endswith('tar.gz') or path.endswith('tar'):
        tar = tarfile.open(path, 'r:gz' if path.endswith('tar.gz') else 'r:')
        tar.extractall(os.path.dirname(path))
        tar.close()
    else:
        zip_ref = zipfile.ZipFile(path)
        zip_ref.extractall(os.path.dirname(path))
        zip_ref.close()

    os.remove(path)
    log('extract is completed', LogLevel.SUCCESS)
