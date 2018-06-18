import json
import os
import uuid

from sally import file

__REPOSITORY_META__ = {
    'coco': 'http://images.cocodataset.org/annotations/image_info_test2017.zip'
}

class Meta:
    def __init__(self, repository='coco'):
        self.repository = repository
        self.download_meta()

    def download_meta(self):
        path = os.path.join(os.getcwd(), '.dataset', uuid.uuid4().hex)
        link = __REPOSITORY_META__[self.repository]
        file.download(path, link)
        self.parse(path)

    def parse(self, path):
        with open(path, 'r') as f:
            json_content = json.loads(f)
            self.parse_json(json_content)

    def parse_json(self, json_content):
        meta = []
        images = json_content['images']
        categories = json_content['categories']

        for image in images:
            image_category = list(filter(lambda category: category['id'] == image['id'], categories)).get(0)
            image_meta = {
                'file': image['name'],
                'category': image_category['supercategory'],
                'sub_category': image_category['category']
            }
            meta.append(image_meta)
