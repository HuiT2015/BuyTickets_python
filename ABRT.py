from PIL import Image 
import urllib.request

#自动抢票系统

pic_url = "https://kyfw.12306.cn/otn/passcodeNew/getPassCodeNew?module=login&rand=sjrand&0.21191171556711197"
headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}

#获取验证码图片
def get_img(url, headers):
    req=urllib.request.Request(url, headers=headers)
    resp=urllib.request.urlopen(req, timeout=60)
    raw = resp.read()
    with open("./tmp.jpg", 'wb') as fp:
        fp.write(raw)
    return Image.open("./tmp.jpg")
    
#裁剪子图,获取子图相应的img
def get_sub_img(img,x, y):  
     assert 0 <= x <= 3  
     assert 0 <= y <= 2  
     left = 5 + (67 + 5) * x  
     top = 41 + (67 + 5) * y  
     right = left + 67  
     bottom = top + 67  
     subImg=img.crop((left, top, right, bottom))  
     return subImg

#百度识图搜索，返回搜索页面内容
def bdst_LookUp(img):
    img.save("./sub_Img.jpg")
    raw = open("./sub_Img.jpg", 'rb').read()
    url = "http://image.baidu.com/n/image?fr=html5&needRawImageUrl=true&id=WU_FILE_0&name=233.png&type=image%2Fpng&lastModifiedDate=Mon+Mar+16+2015+20%3A49%3A11+GMT%2B0800+(CST)&size="    
    url = url + str(len(raw))  
    req = urllib.request.Request(url, raw, {'Content-Type': 'image/jpg', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'})  
    resp_url = urllib.request.urlopen(req).read()  
    url = "http://image.baidu.com/n/pc_search?queryImageUrl=" + urllib.request.quote(resp_url)  
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'})  
    resp = urllib.request.urlopen(req)  
    html = resp.read().decode("utf-8");
    return html
    
def autoBuyRailwayTicket(rtUrl, ):
    
    pass
    
