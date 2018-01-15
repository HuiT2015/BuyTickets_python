import urllib.request as urllib2  
import os
import time
from PIL import Image  
import _thread;

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36"  
pic_url = "https://kyfw.12306.cn/otn/passcodeNew/getPassCodeNew?module=login&rand=sjrand&0.21191171556711197"  
localSrcDir="D:\\12306Imgs\\SrcN"
localSubDir="D:\\12306Imgs\\SubN"
localTextDir="D:\\12306Imgs\\TextN"

if not os.path.exists(localSrcDir):
    os.mkdir(localSrcDir)

if not os.path.exists(localSubDir):
    os.mkdir(localSubDir)

if not os.path.exists(localTextDir):
    os.mkdir(localTextDir)
    
    
#获取验证码图片
def save_img():  
    resp = urllib2.urlopen(pic_url)  
    raw = resp.read()  
    global localSrcDir
    timeStr= time.strftime("%y%m%d%H%M%S")
    filenamePrefix=("%s-src"%timeStr)
    localPath=("%s\\%s.jpg"%(localSrcDir, filenamePrefix))
    with open(localPath, 'wb') as fp:  
         fp.write(raw)  
         print("<<<下载验证码图片%s成功!"%localPath)
    img=Image.open(localPath) 
    return [img, filenamePrefix]
    
         
#裁剪子图
def save_sub_img(img,filenamePrefix, x, y):  
     assert 0 <= x <= 3  
     assert 0 <= y <= 2  
     left = 5 + (67 + 5) * x  
     top = 41 + (67 + 5) * y  
     right = left + 67  
     bottom = top + 67  
     subImg=img.crop((left, top, right, bottom))  
     localSubImgPath=("%s\\%s-sub-%d%d.jpg"%(localSubDir, filenamePrefix, y, x))
     print(">>>>>>提取图片%s.jpg的子图(%d,%d)成功!"%(filenamePrefix,y, x ))
     subImg.save(localSubImgPath,quality = 95)

def save_text_img1():
     for parentDir, dirnames, filenames in os.walk(localSrcDir):
         for filename in filenames:
             filePathName=os.path.join(parentDir,filename)
             img=Image.open(filePathName)
             textImg=img.crop((117, 0, 180, 30))
             localTextImgPath=localTextDir+"\\"+filename[:filename.rfind(".jpg")]+"-text.jpg";
             textImg.save(localTextImgPath)
             print(">>>>>>提取验证码图片%s的文字部分图片成功"%(filename))
         
def save_text_img(img, filenamePrefix):
     textImg=img.crop((117, 0, 180, 30))
     localTextImgPath=localTextDir+"\\"+filenamePrefix+"-text.jpg";
     textImg.save(localTextImgPath, quality = 95)
     print(">>>>>>提取验证码图片%s.jpg的文字部分图片成功！"%(filenamePrefix))
     

def multThread(threadName, sleepTime):
     while(True):
         print("****线程%s正在抓取验证码图片****\n"%threadName)
         img, filenamePrefix=save_img()
         save_text_img(img,filenamePrefix)
         for y in range(2):  
             for x in range(4):  
                 save_sub_img(img,filenamePrefix, x, y)
         time.sleep(sleepTime)

#主函数
if __name__ == '__main__':  
     n=1
     while n<=5:
         _thread.start_new_thread(multThread, (('thread%d'%n),n*2));
         n+=1
      
