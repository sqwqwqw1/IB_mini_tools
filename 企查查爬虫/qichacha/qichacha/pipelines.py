# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import JsonLinesItemExporter
import pandas as pd
import os

class QichachaPipeline(object):

    def __init__(self):
        self.file = open(os.path.join(os.path.dirname(__file__), 'firm_list.json'),'wb')
        self.exporter = JsonLinesItemExporter(self.file, ensure_ascii=False)
        self.exporter.start_exporting()

    def process_item(self,item,spider):
        self.exporter.export_item(item)
        return item

    def close_spider( self,spider):
        self.exporter.finish_exporting()
        self.file.close()
        df = pd.read_json(os.path.join(os.path.dirname(__file__), 'firm_list.json'), lines=True)
        df.to_excel(os.path.join(os.path.dirname(__file__), 'firm_list.xlsx'), index=None)
