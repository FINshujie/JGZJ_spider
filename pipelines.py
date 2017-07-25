# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import MySQLdb.cursors
from scrapy.pipelines.images import ImagesPipeline
from twisted.enterprise import adbapi #异步容器




class JgzjPipeline(object):
    def process_item(self, item, spider):
        return item

class JgzjBookPathPipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        if 'cover_img_url' in item:
            for ok,value in results:
                image_path = value['path']
            item['cover_img_path'] = image_path

        return item


# class MysqlPipeline(object):
#     #同步
#     def __init__(self):
#         self.conn = MySQLdb.connect('localhost','root','0000','books',
#                                     charset = "utf8",use_unicode = True)
#         self.cursor = self.conn.cursor()
#
#     def process_item(self,item,spider):
#         insert_sql = """
#                 insert into ecnomic_books(title,cover_img_url,url,read_nums,comment_nums,cover_img_path)
#                 VALUES (%s,%s,%s,%s,%s,%s)
#             """
#         self.cursor.execute(insert_sql,(item['title'],item['cover_img_url_data'],item['url'],item['read_nums'],
#                                         item['comment_nums'],item['cover_img_path']))
#         self.conn.commit()

class MysqlTwistPipeline(object):
    def __init__(self , dbpool):
        self.dbpool = dbpool


    @classmethod
    def from_settings(cls,settings):
        dbparms = dict(
            host=settings['MYSQL_HOST'],
            db = settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWORD'],
            charset='utf8',
            use_unicode=True,
            cursorclass = MySQLdb.cursors.DictCursor
            )

        dbpool = adbapi.ConnectionPool('MySQLdb',**dbparms)

        return cls(dbpool)

    def process_item(self,item,spider):
        query = self.dbpool.runInteraction(self.do_insert, item)


    def do_insert(self, cursor , item):
        insert_sql = """
                        insert into math_stastic_IT(title,cover_img_url,url,read_nums,comment_nums,cover_img_path)
                        VALUES (%s,%s,%s,%s,%s,%s)
                    """
        cursor.execute(insert_sql,(item['title'],item['cover_img_url_data'],item['url'],item['read_nums'],item['comment_nums'],item['cover_img_path']))
