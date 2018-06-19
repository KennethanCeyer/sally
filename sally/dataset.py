import os
import shutil
import uuid

from sally.file import download_link, cleanup_path, unzip
from sally.meta import Meta
from sally.logger import log, LogLevel

__REPOSITORY_LINK__ = {
    'caltech': {
        'link': 'http://www.vision.caltech.edu/Image_Datasets/Caltech101/101_ObjectCategories.tar.gz',
        'ext': 'tar.gz'
    }
}


class DataSet:
    def __init__(self, name='dataset', repository='caltech'):
        self.name = name
        self.repository = repository
        self.meta = Meta(self.repository)

    def download(self):
        log('install dataset from repository `%s`' % self.repository, LogLevel.INFO)
        file_name = '%s.%s' % (uuid.uuid4().hex, __REPOSITORY_LINK__[self.repository]['ext'])
        path = os.path.join(os.getcwd(), self.name, file_name)
        dir_path = os.path.dirname(path)
        cleanup_path(dir_path)
        code = self.try_download(path)

        if code == -1:
            log('process is refused', LogLevel.ERROR)
            return code

        unzip(path)
        self.try_extract(dir_path)

    def try_download(self, path):
        link = __REPOSITORY_LINK__[self.repository]['link']
        return download_link(path, link)

    def try_extract(self, dir_path):
        for path, dirs, files in reversed(list(os.walk(dir_path))):
            for file in files:
                diff_path = os.path.abspath(os.path.join(path, file)).replace(os.path.abspath(dir_path), '')
                file_name = '_'.join(diff_path.split('/')[2:]).lower()
                if not os.path.exists(os.path.join(dir_path, file_name)):
                    shutil.move(os.path.join(path, file), os.path.join(dir_path, file_name))
            if os.path.exists(path) and path is not dir_path:
                os.rmdir(path)
