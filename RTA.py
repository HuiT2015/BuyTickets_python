import ssl  
import json  
from PIL import Image  
import re  
import urllib.request as urllib2  
import os;
import time;

if hasattr(ssl, '_create_unverified_context'):  
     ssl.create_default_context = ssl._create_unverified_context  
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36"  
pic_url = "https://kyfw.12306.cn/otn/passcodeNew/getPassCodeNew?module=login&rand=sjrand&0.21191171556711197"  
localDir="D:\\12306Imgs";

if not os.path.exists(localDir):
    os.mkdir(localDir);

#获取验证码图片
def get_img():  
    resp = urllib2.urlopen(pic_url)  
    raw = resp.read()  
    global localDir;
    timeStr= time.strftime("%y%m%d%H%M%S");
    localPath=("%s\\%-src.jpg"%(localDir, timeStr));
    with open(localPath, 'wb') as fp:  
        fp.write(raw)  
    return Image.open(localPath)  
    
#裁剪子图
def get_sub_img(im, x, y):  
    assert 0 <= x <= 3  
    assert 0 <= y <= 2  
    left = 5 + (67 + 5) * x  
    top = 41 + (67 + 5) * y  
    right = left + 67  
    bottom = top + 67  
    return im.crop((left, top, right, bottom))  
    
def baidu_stu_lookup(im, row, col):  
    #url = "http://stu.baidu.com/n/image?fr=html5&needRawImageUrl=true&id=WU_FILE_0&name=233.png&type=image%2Fpng&lastModifiedDate=Mon+Mar+16+2015+20%3A49%3A11+GMT%2B0800+(CST)&size="  
    url = "http://image.baidu.com/n/image?fr=html5&needRawImageUrl=true&id=WU_FILE_0&name=233.png&type=image%2Fpng&lastModifiedDate=Mon+Mar+16+2015+20%3A49%3A11+GMT%2B0800+(CST)&size="  
    timeStr= time.strftime("%y%m%d%H%M%S");
    localPath=("%s\\%s-sub-%d%d.jpg"%(localDir, timeStr, row, col));
    im.save(localPath); 
    raw = open(localPath, 'rb').read()  
    url = url + str(len(raw))  
    req = urllib2.Request(url, raw, {'Content-Type': 'image/jpg', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'})  
    resp_url = urllib2.urlopen(req).read()  
    url = "http://image.baidu.com/n/pc_search?queryImageUrl=" + urllib2.quote(resp_url)  
    print('url=%s'%(url));
    req = urllib2.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'})  
    resp = urllib2.urlopen(req)  
    html = resp.read().decode("utf-8");
    #print("html=%s"%html); 
   # saveHtml(localPath[:localPath.rfind(".")], html);
    return baidu_stu_html_extract(html)  

def saveHtml(namePrefix, content):
     f=open(namePrefix+'.html', 'w', encoding='UTF-8');
     f.write(content);
     f.close();    

def baidu_stu_html_extract(html):  
    pattern = re.compile(r"keywords:'(.*?)'")  
    matches = pattern.findall(html)  
    if not matches:  
        return '[UNKOWN]'  
    json_str = matches[0]  
    json_str = json_str.replace('\\x22', '"').replace('\\\\', '\\')  
    result = [item['keyword'] for item in json.loads(json_str)]  
    return '|'.join(result) if result else '[UNKOWN]'  
    
if __name__ == '__main__':  
    im = get_img()  
    for y in range(2):  
        for x in range(4):  
            im2 = get_sub_img(im, x, y)  
            result = baidu_stu_lookup(im2, y, x)  
            print((y, x), result)  
