import os
import shutil

import requests
from tqdm import tqdm


def cleanup_path(dir_path):
    shutil.rmtree(dir_path)
    os.makedirs(dir_path, exist_ok=True)


def download_link(path, link):
    dir_path = os.path.dirname(path)
    cleanup_path(dir_path)
    download_request(path, link)


def download_request(path, link):
    response = requests.get(link, stream=True)
    total_length = response.headers.get('content-length')

    with tqdm(total=100) as pbar:
        with open(path, 'wb') as f:
            if total_length is None:
                f.write(response.content)
            else:
                total_length = int(total_length)
                for data in response.iter_content(chunk_size=4096):
                    f.write(data)
                    pbar.update(len(data) / total_length * 100)
