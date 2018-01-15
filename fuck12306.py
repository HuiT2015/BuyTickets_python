#!/usr/bin/python
# #  FileName    : fuck12306.py
# #  Author      : MaoMao Wang <andelf@gmail.com>
# #  Created     : Mon Mar 16 22:08:41 2015 by ShuYu Wang
# #  Copyright   : Feather (c) 2015
# #  Description : fuck fuck 12306
# #  Time-stamp: <2016-04-10 16:28:41 andelf>

from PIL import Image
from PIL import ImageFilter
import urllib.request as urllib2  
import urllib.parse
import re


# hack CERTIFICATE_VERIFY_FAILED
# https://github.com/mtschirs/quizduellapi/issues/2
import ssl
if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context


UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36"

pic_url = "https://kyfw.12306.cn/otn/passcodeNew/getPassCodeNew?module=login&rand=sjrand&0.21191171556711197"


def get_img():
    resp = urllib2.urlopen(pic_url)
    raw = resp.read()
    with open("./tmp.jpg", 'wb') as fp:
        fp.write(raw)

    return Image.open("./tmp.jpg")


def get_sub_img(im, x, y):
    assert 0 <= x <= 3
    assert 0 <= y <= 2
    left = 5 + (67 + 5) * x
    top = 41 + (67 + 5) * y
    right = left + 67
    bottom = top + 67
    return im.crop((left, top, right, bottom))



def baidu_image_upload(im):
    url = "http://image.baidu.com/pictureup/uploadshitu?fr=flash&fm=index&pos=upload"
    im.save("./query_temp_img.png")
    raw = open("./query_temp_img.png", 'rb').read()

    files = {
        'fileheight'   : "0",
        'newfilesize'  : str(len(raw)),
        'compresstime' : "0",
        'Filename'     : "query_temp_img.png",
        'filewidth'    : "0",
        'filesize'     : str(len(raw)),
        'filetype'     : 'image/png',
        'Upload'       : "Submit Query",
        'filedata'     : ("query_temp_img.png", raw)
    }
    
    #files=urllib.parse.urlencode(files).encode(encoding='utf8')
    req = urllib2.Request(url, data=files, headers={'User-Agent':UA})
    resp = urllib2.urlopen(req).read()
    print('resp=%s'%resp.decode())
    #  resp.url
    redirect_url = "http://image.baidu.com" + urllib2.quote(resp)
    print('redirect_url=%s'%redirect_url)  
    return redirect_url



def baidu_stu_lookup(im):
    redirect_url = baidu_image_upload(im)

    #print redirect_url
    req = urllib2.Request(redirect_url)

    resp = urllib2.urlopen(req)  
    html = resp.read().decode("utf-8");

    return baidu_stu_html_extract(html)


def baidu_stu_html_extract(html):
    pattern = re.compile(r"'multitags':\s*'(.*?)'")
    matches = pattern.findall(html)
    if not matches:
        return '[ERROR?]'

    tags_str = matches[0]

    result =  list(filter(None, tags_str.replace('\t', ' ').split()))

    return '|'.join(result) if result else '[UNKOWN]'


def ocr_question_extract(im):
    # git@github.com:madmaze/pytesseract.git
    global pytesser
    try:
        import pytesser
    except:
        print("[ERROR] pytesseract not installed")
        return
    im = im.crop((117, 0, 180, 30))
    im = pre_ocr_processing(im)
    im.show()
    return pytesser.image_to_string(im, language='chi_sim').strip()


def pre_ocr_processing(im):
    im = im.convert("RGB")
    width, height = im.size
    white = im.filter(ImageFilter.BLUR).filter(ImageFilter.MaxFilter(23))
    grey = im.convert('L')
    impix = im.load()
    whitepix = white.load()
    greypix = grey.load()

    for y in range(height):
        for x in range(width):
            greypix[x,y] = min(255, max(255 + impix[x,y][0] - whitepix[x,y][0],
                                        255 + impix[x,y][1] - whitepix[x,y][1],
                                        255 + impix[x,y][2] - whitepix[x,y][2]))

    new_im = grey.copy()
    binarize(new_im, 150)
    return new_im


def binarize(im, thresh=120):
    assert 0 < thresh < 255
    assert im.mode == 'L'
    w, h = im.size
    for y in range(0, h):
        for x in range(0, w):
            if im.getpixel((x,y)) < thresh:
                im.putpixel((x,y), 0)
            else:
                im.putpixel((x,y), 255)


if __name__ == '__main__':
    im = get_img()
    #im = Image.open("./tmp.jpg")
    try:
        print('OCR Question:%s'%ocr_question_extract(im))
    except Exception as e:
        print("<OCR failed>:%s"%e)
    for y in range(2):
        for x in range(4):
            im2 = get_sub_img(im, x, y)
            result = baidu_stu_lookup(im2)
            print (y,x), result
            pass