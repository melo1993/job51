# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors

class JobspiderPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            port=settings["MYSQL_PORT"],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass = MySQLdb.cursors.DictCursor,
            use_unicode= True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)

    def process_item(self, item, spider):
        if spider.name=='job51':
            d = self.dbpool.runInteraction(self.refresh_job51, item, spider)
            d.addErrback(self.handle_error, item, spider)
            d.addBoth(lambda _: item)
            return d


    def refresh_job51(self, conn, item, spider):
        conn.execute("""
                select 1 from t_spider_51job where jobid = %s
        """, (item["id"],))
        ret = conn.fetchone()

        if ret:
            conn.execute("""
                update t_spider_51job set companyname=%s,jobname = %s, city = %s, link = %s, salary = %s, time_range = %s, edu=%s, jobcount=%s, updatetime=%s, linker=%s, contact_phonenum=%s,lang=%s,benefit=%s,email=%s,companydescription=%s,responsibility=%s,qualification=%s, address=%s where jobid = %s
            """, (item['companyname'],
                  item['name'],
                  item['city'],
                  item['link'],
                  item['salary'],
                  item['time_range'],
                  item['edu'],
                  item['count'],
                  item['updatetime'],
                  item['linker'],
                  item['contact_phonenum'],
                  item['lang'],
                  item['benefit'],
                  item['email'],
                  item['companydescription'],
                  item['responsibility'],
                  item['qualification'],
                  item['address'],
                  item["id"]))

        else:
            conn.execute("""
                insert into t_spider_51job(jobid,companyname,jobname,city,link,salary,time_range,edu,jobcount,updatetime,linker,contact_phonenum,lang,email,benefit,companydescription,responsibility,qualification,address)
                select %s, %s,%s, %s, %s,%s,%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s from dual
            """, (item["id"],
                  item["companyname"],
                  item['name'],
                  item['city'],
                  item['link'],
                  item['salary'],
                  item['time_range'],
                  item['edu'],
                  item['count'],
                  item['updatetime'],
                  item['linker'],
                  item['contact_phonenum'],
                  item['lang'],
                  item['email'],
                  item['benefit'],
                  item['companydescription'],
                  item['responsibility'],
                  item['qualification'],
                  item['address']))


    # 异常处理
    def handle_error(self, failue, item, spider):
        print failue