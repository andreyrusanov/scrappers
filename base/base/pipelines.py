# -*- coding: utf-8 -*-
import os
import sys
from scrapy import Request
from scrapy.pipelines.files import FilesPipeline
# figure out with encoding
reload(sys)
sys.setdefaultencoding('utf-8')


class SaveLessonPipeline(FilesPipeline):
    def process_item(self, item, spider):
        super(SaveLessonPipeline, self).process_item(item, spider)

    # TODO: use info?
    def file_path(self, request, response=None, info=None):
        url = request.url
        media_ext = os.path.splitext(url)[1]  # change to request.url after deprecation
        return 'begin_english/{}/{}{}'.format(request.meta['chapter'], os.path.splitext(url)[0].split('/')[-1], media_ext)

    def get_media_requests(self, item, info):
        return [Request(x, meta=dict(chapter=item['chapter'])) for x in item.get(self.FILES_URLS_FIELD, [])]

