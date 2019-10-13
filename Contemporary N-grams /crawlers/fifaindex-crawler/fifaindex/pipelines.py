# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy.exporters import JsonLinesItemExporter


class PlayerExportPipeline(object):
    def __init__(self, filename):
        self.filename = filename
        self.file = None

    @classmethod
    def from_crawler(cls, crawler):
        output_filename = crawler.settings.get('FILE_NAME')
        return cls(output_filename)

    def open_spider(self, spider):
        # Opening file in binary-write mode
        self.file = open(self.filename, 'ab')
        self.exporter = JsonLinesItemExporter(self.file)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
