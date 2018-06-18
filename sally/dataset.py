import os
import uuid
import zipfile

from sally.file import download_link

__REPOSITORY_LINK_ = {
    'coco': 'http://images.cocodataset.org/annotations/panoptic_annotations_trainval2017.zip'
}


def download(name='dataset', repository='coco'):
    file_name = '%s.zip' % uuid.uuid4().hex
    path = os.path.join(os.getcwd(), name, file_name)
    try_download(path, repository)
    try_unzip(path)
    try_extract(path)


def try_download(path, repository='coco'):
    link = __REPOSITORY_LINK_[repository]
    download_link(path, link)


def try_unzip(path):
    with zipfile.ZipFile(path, 'r') as zip_ref:
        zip_ref.extractall(os.path.dirname(path))


def try_extract(path, is_root=True):
    if not os.path.isdir(path):
        return

    dir_path = os.path.dirname(path)
    files = os.listdir(dir_path)

    for file in files:
        if is_root:
            try_extract(os.path.join(dir_path, file), False)
            return

        os.move(os.path.join(dir_path, file), os.path.join(dir_path, '..'))
