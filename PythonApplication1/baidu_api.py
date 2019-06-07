from aip import AipOcr
import os
import cv2 as cv
import shutil
from PIL import Image
import time
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

APP_ID='16427841'
API_KEY='Qo2TM8bvgGFmGZeF800kmDWs'
SECRET_KEY='enB16fen0UKymBUk1lc4khmmGb3CWQXG'
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
options = {}
options["probability"] = "true"

sum=0
for i in range(2151,10000):
    for j in range(0,4):
        if os.path.exists('K:\\img_rec\\train\\'+str(i)+'_'+str(j)+'.png'):
            im=Image.open('K:\\img_rec\\train\\'+str(i)+'_'+str(j)+'.png')
            if min(im.size[0],im.size[1])<16:
                f=18/min(im.size[0],im.size[1])
                im=im.resize((round(im.size[0]*f),round(im.size[1]*f)))
                im.save('K:\\img_rec\\train\\'+str(i)+'_'+str(j)+'.png')
            image = get_file_content('K:\\img_rec\\train\\'+str(i)+'_'+str(j)+'.png')
            try:
                data=client.basicGeneral(image,options)
            except:
                time.sleep(60)
                data=client.basicGeneral(image,options)
            print(sum,str(i)+'_'+str(j),data)
            try:
                if data['words_result_num']==1:
                    word=data['words_result']
                    word=word[0]
                    res=word['words']
                    prob=word['probability']
                    if prob['average']>0.85:
                        if len(res)==1:
                            if ord(res)>47 and ord(res)<58:
                             shutil.copyfile('K:\\img_rec\\train\\'+str(i)+'_'+str(j)+'.png','K:\\img_rec\\trainset\\'+res+'\\'+str(i)+'_'+str(j)+'.png')
                             sum=sum+1
                            if ord(res)>64 and ord(res)<91:
                                shutil.copyfile('K:\\img_rec\\train\\'+str(i)+'_'+str(j)+'.png','K:\\img_rec\\trainset\\C'+res+'\\'+str(i)+'_'+str(j)+'.png')    
                                sum=sum+1
                            if ord(res)>96 and ord(res)<123:
                                shutil.copyfile('K:\\img_rec\\train\\'+str(i)+'_'+str(j)+'.png','K:\\img_rec\\trainset\\'+res+'\\'+str(i)+'_'+str(j)+'.png')
                                sum=sum+1
            except:
                print(sum,str(i)+'_'+str(j),'wrong size')