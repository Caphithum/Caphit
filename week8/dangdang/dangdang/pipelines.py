# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql

class Demo1Pipeline:
    def open_spider(self,spider):
        print("opened")

        try:
            self.con =pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="lzyft1030", db="ddbookdb", charset="utf8")
            self.cursor = self.con.cursor(pymysql.cursors.DictCursor)#创建游标
            self.cursor.execute("delete from books")
            self.opend = True
            self.count = 0
        except Exception as err:
            print(err)
            self.opend = False

    def close_spider(self,spider):
        if self.opend:
            self.con.commit()#提交
            self.con.close()#关闭
            self.opend = False
        print("closed")
        print("总共爬取",self.count,"本书籍")

    def process_item(self, item, spider):
        #查看传输过来的数据
        try:
            #把数据存入到mysql中
            if self.opend:
                self.cursor.execute("insert into books(btitle, bauthor, bpublisher, bdate, bprice, bdetail) values(%s, %s, %s ,%s ,%s, %s)", \
                            (item["title"], item["author"], item["publisher"], item["date"], item["price"], item["detail"]))
                #计算书籍数量
                self.count+= 1
        except Exception as err:
            print(err)

        return item


