# -*- coding: utf-8 -*-
import os
import sys
import scrapy
from ..items import LessonItem


# figure out with encoding
reload(sys)
sys.setdefaultencoding('utf-8')


class BeginEnglishSpider(scrapy.Spider):
    name = "begin_english"
    allowed_domains = ["begin-english.ru"]
    start_urls = (
        'http://www.begin-english.ru/audio/audiouroki-davydova/',
    )

    custom_settings = dict(destination=os.path.join(os.path.dirname(__file__), '..', 'output', 'begin_english'))

    def parse(self, response):
        links = response.selector.css('#content > ul > li > a')
        for link in links:
            url = response.urljoin(link.xpath('@href').extract()[0])
            chapter = link.xpath('text()').extract()[0]
            yield scrapy.Request(url, callback=self.parse_chapter, meta=dict(chapter=chapter))

    def parse_chapter(self, response):
        chapter = response.meta['chapter']
        audio = response.selector.css('audio')
        for index, entry in enumerate(audio):
            link = response.urljoin(entry.css('source').xpath('@src').extract()[0])
            yield LessonItem(file_urls=[link], title=index, chapter=chapter)
