import urllib.request
import sys
import urlopen
from pprint import pprint
from lxml import html
from html.parser import HTMLParser
count = 0
class MyHTMLParser(HTMLParser):
    def __init__(
        self,
        decode_html_entities = True,
        data_seperator = ' ',   
    ):
        HTMLParser.__init__(self)
        self.data_seperator=data_seperator
        self.is_td=False
        self.is_th=False
        self.current_table=[]
        self.cell=[]
        self.row=[]
        self.tables=[]
        self.count=0

    def handle_starttag(self,tag,attrs):

        if tag == 'td' or tag == 'TD':
            self.is_td = True
        elif tag == 'th' or tag == 'TH':
            self.is_th = False
    def handle_endtag(self,tag):
        if tag == 'td' or tag == 'TD':
            self.is_td = False
        elif tag == 'th' or tag == 'TH':
            self.is_th = False
        if tag == ['td','TD']:
            final_cell = self.data_seperator.join(self.cell).strip()
            self.row.append(final_cell)
            self.cell = []
        elif tag == 'tr' or tag == 'TR':
            self.current_table.append(self.row)
            self.row = []
        elif tag == 'table' or tag == 'TABLE':
            self.tables.append(self.cell)
            self.current_table = []
            

    def handle_data(self,data):
        if self.is_th or self.is_td:
            self.cell.append(data.strip())
            self.count = self.count+1


#testing code
#
#
#
# wanted_grade = input("enter the wanted grade:")

# parser = MyHTMLParser()
# url = "http://course-query.acad.ncku.edu.tw/qry/qry001.php?dept_no=F7"
# page = urllib.request.urlopen(url)

# mystr = page.read().decode("utf8")

# parser.feed(mystr)
# flag = 0
# grade = 0
# for i in range(0,parser.count):
#     print(parser.tables[0][i])
#     if parser.tables[0][i]== '甲乙':
#         print("年級：\t\t"+parser.tables[0][i+1])
#         grade = parser.tables[0][i+1]
#         flag = 1
#     elif parser.tables[0][i]== 'N' and flag == 1 and grade == wanted_grade:
#         print("課程: \t\t"+parser.tables[0][i+1])
#         print("必選修: \t"+parser.tables[0][i+2])
#         print("學分數: \t"+parser.tables[0][i+3])
#         print("授課老師: \t"+parser.tables[0][i+4])
#         print("\n\n")
#         flag = 0
#     else:
#         continue
