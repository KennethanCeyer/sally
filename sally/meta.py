import json
import os
import uuid

from sally import file
from sally.file import cleanup_path, unzip

__REPOSITORY_META__ = {
    'caltech': 'https://requestor-proxy.figure-eight.com/figure_eight_datasets/open-images/zip_files_copy/test.zip'
}


class Meta:
    def __init__(self, repository='caltech'):
        self.meta = []
        self.repository = repository

        if repository is not 'caltech':
            self.download_meta()

    def download_meta(self):
        path = os.path.join(os.getcwd(), '.dataset', uuid.uuid4().hex)
        dir_path = os.path.dirname(path)
        cleanup_path(dir_path)
        link = __REPOSITORY_META__[self.repository]
        file.download_link(path, link)
        unzip(path)
        self.parse(dir_path)

    def parse(self, dir_path):
        files = os.listdir(dir_path)

        for file in files:
            sub_file_path = os.path.join(dir_path, file)
            if os.path.isdir(sub_file_path):
                self.parse(sub_file_path)
                continue

            with open(sub_file_path, 'rb') as f:
                text = f.read()
                json_content = json.loads(text)
                self.parse_json(json_content)

    def parse_json(self, json_content):
        meta = []
        images = json_content['images']
        categories = json_content['categories']

        for image in images:
            image_category = list(filter(lambda category: category['id'] == image['id'], categories))
            if len(image_category) < 1:
                continue
            image_category = image_category[0]
            print(image_category)
            image_meta = {
                'file': image['file_name'],
                'category': image_category['supercategory'],
                'sub_category': image_category['name']
            }
            meta.append(image_meta)

        self.meta = meta
