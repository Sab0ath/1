
from tkinter import *
import tkinter.messagebox
from tkinter.filedialog import askdirectory
from tkinter.ttk import *
from PIL import Image,ImageTk
from io import BytesIO
import requests
import os
import time
from json import JSONDecoder,JSONDecodeError
import re
import base64


headers = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.9(0x17000929) NetType/WIFI Language/zh_CN",
    # "Referer": "https://weixin.zijinshe.com/cms/webapp/home/answer/index.html",
    "Origin": "https://weixin.zijinshe.com"
}
#
imgurl=''

#
NOT_WHITESPACE=re.compile(r'[^\s]')
def decode_stacked(document,pos=0,decoder=JSONDecoder()):
    while True:
        match = NOT_WHITESPACE.search(document,pos)
        if not match:
            return
        pos=match.start()

        try:
            obj,pos = decoder.raw_decode(document,pos)
        except JSONDecodeError:
            raise
        yield  obj

#
def get_select(grades,course,volume):
    select1="""SELECT * FROM ossobject [*] o WHERE o.book.gradesStr like  '%{},%' \
AND o.book.course in ('{}') AND o.book.volume in  ('{}','3') \
AND o.book.category in  ('keben','jiaofu','keben_answer','jiaofu_answer')""".format(grades,course,volume)
    select1_base64=base64.b64encode(select1.encode())
    return select1_base64

#
root = Tk()
root.title('练习册下载器')
root.geometry('640x530')
# root.iconbitmap('./logo.ico')
#

#
cmb1 = Combobox(root,state='readonly',width=30)
cmb2 = Combobox(root,state='readonly',width=30)
cmb3 = Combobox(root,state='readonly',width=30)
cmb1['value']=('一年级','二年级','三年级','四年级','五年级','六年级','七年级','八年级','九年级')
cmb2['value']=('数学','语文','英语','物理','化学','生物','历史','道德与法制')
cmb3['value']=('上半学期','下半学期')
#
cmb1.current(0)
cmb2.current(0)
cmb3.current(0)
cmb1.grid(row=0,column=0,pady=5)
cmb2.grid(row=1,column=0,pady=5)
cmb3.grid(row=2,column=0,pady=5)
#

#
y_scroll = Scrollbar(root)
y_scroll.grid(row=3,column=1,sticky=N+S)
x_scroll = Scrollbar(root,orient=HORIZONTAL)
x_scroll.grid(row=4,column=0,sticky=W+E)
#
lb = Listbox(root,height=15,width=40,yscrollcommand=y_scroll.set,xscrollcommand=x_scroll.set)
lb.grid(row=3,column=0,padx=15,pady=5)
#
y_scroll.config(command=lb.yview)
x_scroll.config(command=lb.xview)

#
def printlist():
    url="https://prd.oss.leziedu.com/"
    global imgurl
    # print(lb.curselection())
    v = lb.curselection()
    #
    i= list(v)
    # list1[i[0]]
    imgurl = "{}{}".format(url,list1[i[0]]["thumbCoverPath"])
    # print(imgurl)
    #
    imgreq = requests.get(imgurl, headers=headers)
    image = Image.open(BytesIO(imgreq.content))
    tk_image = ImageTk.PhotoImage(image)
    # https://www.jb51.net/article/162969.htm
    imglabel.config(image=tk_image)
    imglabel.image=tk_image #keep a reference!


#
def is_listbox_right(event):
    if lb.curselection() and lb.get(0):
        printlist()
    else:
        tkinter.messagebox.showwarning('wrong!', '没有找到教材,重新选择！')


#
lb.bind('<Double-Button-1>', is_listbox_right)



#