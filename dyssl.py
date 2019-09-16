#coding=utf-8
#1将名字提取出来，从字符串的第三个字符开始提取名字，直到遇到逗号
#2将电话号码提取出来，利用正则表达式匹配电话号码,分片
#3从剩余字符串中搜索省，然后将省前的字符串提取，分片
#4从剩余字符串中搜索市，然后将市前的字符串提取，分片
#5从剩余字符串中搜索县和区，然后将其前的字符串提取，分片
#6从剩余字符串中搜索镇和道，然后将其前的字符串提取，分片
#最后的字符串就是剩余地址,但是要去掉.

import json
import re
import io

def getname (message):
    start = 2
    end = message.find(',')
    name = message[start:end]
    message1 = message[end+1:]
    #print(message1)
    #print(name)
    return  message1,name

def getnumber(message1):
    number = re.findall(r'\d{9,12}', message1)[0]
    message2 = message1[:message1.find(number)]+message1[message1.find(number)+len(number):]
    #print(message2)
    #print(number)
    return message2,number

def getshen(message2):
    zhixiashi=["北京市","天津市","上海市","重庆市"]
    for each in zhixiashi:
        if message2[:3] == each:
            shen = each[:2]
            message3 = message2
            return message3,shen
    pshen = message2.find('省')
    pxingzhengqu = message2.find('行政区')
    pzizhiqu = message2.find('自治区')
    if pshen != -1:
        shen = message2[:message2.find('省')+1]
        message3 = message2[message2.find('省')+1:]
    elif pxingzhengqu != -1:
        shen = message2[:message2.find('行政区')+1]
        message3 = message2[message2.find('行政区')+1:]
    elif pxingzhengqu != -1:
        shen = message2[:message2.find('自治区')+1]
        message3 = message2[message2.find('自治区')+1:]
    else:
        for each in chinadict.keys():
            if each.find(message2[0:2]) != -1:
                shen = each
                if each[len(each)-1] == '省':
                    message3 = message2[len(each)-1:]
                if each[len(each)-1] == '行政区':
                    message3 = message2[len(each)-3:]
                if each[len(each)-1] == '自治区':
                    message3 = message2[len(each)-3:]
                break
    #print(message3)
    #print(shen)
    return message3,shen

def getshi(shen,message3):
    pshi = message3.find('市')
    if pshi != -1:
        shi = message3[:pshi+1]
        message4 = message3[pshi+1:]
    else:
        for each in chinadict[shen]:
            if each.find(message3[:2]) != -1:
                shi = each
                i = 0
                while (i < len(shi) and shi[i] == message3[i]):
                    i += 1
                message4 = message3[i:]
    #print(message4)
    #print(shi)
    return message4,shi

def getxianqu(message4):
    pxian = message4.find('县')
    pqu = message4.find('区')
    if pxian != -1:
        xianqu = message4[:message4.find('县')+1]
        message5 = message4[message4.find('县')+1:]
    elif pqu != -1:
        xianqu = message4[:message4.find('区') + 1]
        message5 = message4[message4.find('区') + 1:]
    else:
        xianqu = ""
        message5 = message4
    #print(message5)
    #print(xianqu)
    return message5,xianqu

def getzhendao(message5):
    pdao = message5.find('道')
    pzhen = message5.find('镇')
    pxiang = message5.find('乡')
    if pxiang != -1:
        zhendao = message5[:message5.find('道') + 1]
        message6= message5[message5.find('道') + 1:]
    elif pzhen != -1:
        zhendao = message5[:message5.find('镇') + 1]
        message6 = message5[message5.find('镇') + 1:]
    elif pxiang != -1:
        zhendao = message5[:message5.find('乡') + 1]
        message6 = message5[message5.find('乡') + 1:]
    else:
        zhendao = ""
        message6 = message5
    #print(message6)
    #print(zhendao)
    return message6,zhendao

def getdetail(message6):
    detail = message6[:len(message6)-1]
    #print(detail)
    return detail


filename ='city_code.json'
with open(filename,'r',encoding='utf-8') as file:
    chinadict=json.load(file)
message = input()
message1,name = getname(message)
message2,number = getnumber(message1)
message3,shen = getshen(message2)
message4,shi = getshi(shen,message3)
message5,xianqu = getxianqu(message4)
message6,zhendao = getzhendao(message5)
detail = getdetail(message6)
address = [shen, shi, xianqu, zhendao, detail]
final={
    "姓名": name,
    "手机": number,
    "地址": address
}
result = json.dumps(final,ensure_ascii=False)
print(result)