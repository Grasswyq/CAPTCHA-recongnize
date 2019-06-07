import pytesseract
import requests
import hashlib
from PIL import Image,ImageDraw
import sys
import os
import random
import numpy as np
from queue import LifoQueue
import time
import shutil

id='2018300001031'


def get_img(name):
    img=requests.get('http://210.42.121.241/servlet/GenImg')
    fp=open('K:\\img_rec\\Dataset\\'+name+'.png','wb')
    fp.write(img.content)
    fp.close()
    im=Image.open('K:\\img_rec\\Dataset\\'+name+'.png')
    data=im.load()
    for x in range(0,im.size[0]):
        for y in range(0,im.size[1]):
            pix=data[x,y]
            if pix[0]<120 or pix[1]>100 or pix[2]>100:
                im.putpixel((x,y),(255,255,255))
    im=im.convert('L')
    im.save('K:\\img_rec\\Dataset\\'+name+'.png')
    threshold = 230
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
 
    # 图片二值化
    photo = im.point(table, '1')
    photo.save('K:\\img_rec\\Dataset\\'+name+'.png')


def char_draw(im):
    pix=im.load()
    print(pix)
    print(im.size[0],im.size[1])
    print(pix[im.size[0]/2,im.size[1]/2])

    for h in range(0,30):
        for w in range(0,120):
            if pix[w,h]==0:
                break;
    pixel=LifoQueue()
    print(pixel.empty())
    pixel.put([w,h])
    print(pixel.empty())
    res=[]
    while pixel.empty()==False:
        pos=pixel.get()
        print(pos)
        im.putpixel(pos,255)
        pix[pos[0],pos[1]]=32
        res.append(pos)
        
        for dh in range(-1,1):
            for dw in range(0,1):
                if pix[pos[0]+dw,pos[1]+dh]==0:
                    pix[pos[0]+dw,pos[1]+dh]=32
                    pixel.put([pos[0]+dh,pos[1]+dw])
    im.show()

def update(date):
    st=str(int(date)+1)
    if int(st[6:8])>31:
        st=str(int(st)+68)
        if int(st[4:6])>12:
            st=str(int(st)+8700)
    return st

def connect():
    sd=hashlib.md5()
    pwd='19400101'
    pwd=update(pwd)
    sd.update(pwd.encode('utf-8'))
    ha=sd.hexdigest()
    xdvfb=code_img()
    HEADER = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'} 
    src='http://210.42.121.241/servlet/Login?id='+id+'&pwd='+ha+'&xdvfb='+xdvfb
    print(src)
    data=requests.get(src,headers=HEADER)
    fp=open('data.txt','w')
    fp.write(data.text)
    if data.text.find('验证码错误')>0:
        print('验证码错误')
    else:
        if da.text.find('用户名、密码错误')>0:
            print('密码错误')

def create_dataset(num):
    for i in range(0,num):
        get_img(str(i))
        print('success get '+str(i))

def show(pix,px=0,py=0):
    os.system('cls')
    for y in range(0,h):
        sr=''
        for x in range(0,w):
            if px==x and py==y:
                sr=sr+'X'
            else:
                if pix[x,y]==0:
                    sr=sr+'1'
                else:
                    sr=sr+'0'
        print(sr)

def findseed(pix):
    exit_flag=0
    for x in range(0,w):
        for y in range(0,h):
            if pix[x,y]==0:
                exit_flag=1
                break
        if exit_flag==1:
            break
    return [x,y]


def tbuild(pix,t):
    seed=findseed(pix)
    list=[seed]
    p=0
    while len(list)!=p:
        pos=list[p]
        pix[pos[0],pos[1]]=32
        for dx in range(-1,2):
            for dy in range(-1,2):
                if pos[0]+dx<w and pos[1]+dy<h:
                    if pix[pos[0]+dx,pos[1]+dy]==0:
                        pix[pos[0]+dx,pos[1]+dy]=32
                        list.append([pos[0]+dx,pos[1]+dy])
        p=p+1
    if len(list)<20:
        tbuild(pix,t)
    else:
        sub=[w+1,h+1,0,0]           #xmin,ymin,xmax,ymax
        for i in list:
            if i[0]<sub[0]:
                sub[0]=i[0]
            if i[1]<sub[1]:
                sub[1]=i[1]
            if i[0]>sub[2]:
                sub[2]=i[0]
            if i[1]>sub[3]:
                sub[3]=i[1]
        if sub[0]>0:
            sub[0]=sub[0]-1
        if sub[1]>0:
            sub[1]=sub[1]-1
        if sub[2]<w-1:
            sub[2]=sub[2]+1
        if sub[3]<h-1:
            sub[3]=sub[3]+1
        sh=Image.open('K:\\img_rec\\'+str(tag)+'.png')
        char=sh.crop(sub)
        char.save('K:\\img_rec\\train\\'+str(tag)+'_'+str(t)+'.png')

def recover(pix):
    for x in range(0,w):
        for y in range(0,h):
            if pix[x,y]==32:
                pix[x,y]=0
            


if __name__ == "__main__":
    create_dataset(10000)
    for tag in range(0,10000):
        try:
            im=Image.open('K:\\img_rec\\Dataset\\'+str(tag)+'.png')
            shutil.copyfile('K:\\img_rec\\Dataset\\'+str(tag)+'.png','K:\\img_rec\\'+str(tag)+'.png')
            pix=im.load()
            w=im.size[0]
            h=im.size[1]
            for i in range(0,4):
                tbuild(pix,i)
            os.remove('K:\\img_rec\\'+str(tag)+'.png')
            print('success:'+str(tag))
        except:
            os.remove('K:\\img_rec\\'+str(tag)+'.png')
            for ed in range(0,3):
                if os.path.exists('K:\\img_rec\\train\\'+str(tag)+'_'+str(ed)+'.png')==True:
                    os.remove('K:\\img_rec\\train\\'+str(tag)+'_'+str(ed)+'.png')
            print('err')

    #os.remove(str(tag)+'.png')

        
    