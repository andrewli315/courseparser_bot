from transitions.extensions import GraphMachine
from MyHTMLParser import MyHTMLParser
import urllib.request
from urllib.error import URLError, HTTPError
import sys
import urlopen
from pprint import pprint
from lxml import html
from html.parser import HTMLParser
class TocMachine(GraphMachine):
    data = []
    temp = [] 
    count_1 = 0
    count_2 = 0
    count_3 = 0
    count_4 = 0

    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model = self,
            **machine_configs
        )

    def is_going_to_grade1(self, update):
        text = update.message.text
        return text.lower() == 'grade1'
    def is_going_to_grade2(self, update):
        text = update.message.text
        return text.lower() == 'grade2'
    def is_going_to_grade3(self, update):
        text = update.message.text
        return text.lower() == 'grade3'
    def is_going_to_grade4(self, update):
        text = update.message.text
        return text.lower() == 'grade4'
    def is_going_to_dummy(self, update,):
        text = update.message.text
        return text.lower() != 'grade1' and text.lower()!='grade2' and text.lower() != 'grade3' and text.lower() != 'grade4' and text.lower() != 'comment' and text.lower() != 'parse'
    def parseweb(self, update):
        text = update.message.text
        return text.lower() == 'parse'

    def on_enter_grade1(self, update):
        str=''
        for i in range(0,self.count_1):
            str = str+'\n'
            for j in range(0,len(self.data[i])):
                str = str + '\t' + self.data[i][j]
        update.message.reply_text('Result'+str)
        self.go_back(update)
    
    def on_enter_grade2(self, update):
        str=''
        for i in range(self.count_1,self.count_1+self.count_2):
            str = str+'\n'
            for j in range(0,len(self.data[i])):
                str = str + '\t' + self.data[i][j]
        update.message.reply_text('result'+ str)
        self.go_back(update)

    def on_enter_grade3(self, update):
        str=''
        for i in range(self.count_1+self.count_2,self.count_1+self.count_2+self.count_3):
            str = str+'\n'
            for j in range(0,len(self.data[i])):
                str = str + self.data[i][j]
        update.message.reply_text('result'+str)
        self.go_back(update)

    def on_enter_grade4(self, update):
        str=''
        for i in range(self.count_1+self.count_2+self.count_3,self.count_1+self.count_2+self.count_3+self.count_4):
            str = str+'\n'
            for j in range(0,len(self.data[i])):
                str = str + self.data[i][j]
        update.message.reply_text('result'+str)
        self.go_back(update)

    def on_enter_dummy(self, update):
        update.message.reply_text("please input \'parse \' first")
        update.message.reply_text("then choose command:\ngrade1\ngrade2\ngrade3\ngrade4\n")
        self.go_back(update)

    def on_enter_parse(self, update):
        
        self.data = []
        self.temp = [] 
        self.count_1 = 0
        self.count_2 = 0
        self.count_3 = 0
        self.count_4 = 0
        parser = MyHTMLParser()
        url = "http://course-query.acad.ncku.edu.tw/qry/qry001.php?dept_no=F7"
        try:
            page = urllib.request.urlopen(url,timeout=10)
            mystr = page.read().decode("utf8")
        except URLError as error:
            update.message.reply_text("FAILED TO CONNECT WEB")
            print("error: ")
            print(error)
            self.go_back(update)
        except HTTPError as error:
            update.message.reply_text("FAILED TO CONNECT WEB")
            print("error: ")
            print(error)
            self.go_back(update)
        else:
            
            parser.feed(mystr)
            flag = 0
            grade = 0
            for i in range(0,parser.count):
                if parser.tables[0][i]== '甲乙':
                    grade = parser.tables[0][i+1]
                    self.temp.append(parser.tables[0][i+1])
                    flag = 1
                elif parser.tables[0][i]== 'N' and flag == 1 :
                    if grade == '1':
                        self.count_1 = self.count_1 + 1
                    elif grade == '2':
                        self.count_2 = self.count_2 + 1
                    elif grade == '3':
                        self.count_3 = self.count_3 + 1
                    elif grade == '4':
                        self.count_4 = self.count_4 + 1
                    
                    self.temp.append(parser.tables[0][i+1])
                    self.temp.append(parser.tables[0][i+2])
                    self.temp.append(parser.tables[0][i+3])
                    self.temp.append(parser.tables[0][i+4])
                    self.data.append(self.temp)
                    self.temp = []
                    flag = 0
                else:
                    continue
            update.message.reply_text("parsing complete")
            self.go_back(update)

    def on_exit_grade1(self, update):
        print('Leaving grade1')
    def on_exit_grade2(self, update):
        print('Leaving grade2')
    def on_exit_grade3(self, update):
        print('Leaving grade3')
    def on_exit_grade4(self, update):
        print('Leaving grade4')
    def on_exit_dummy(self, update):
        print('Leaving dummy')
    def on_exit_parse(self, update):
        print('Leaving parse')
