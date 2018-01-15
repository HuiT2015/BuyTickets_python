from pytesser import *
from PIL import Image
import os;

localSrcDir="D:\\12306Imgs\\test"

def rImgText():
    global localSrcDir
    for parentDir, dirnames, filenames in os.walk(localSrcDir):
             for filename in filenames:
                 filePathName=os.path.join(parentDir,filename)
                 img=Image.open(filePathName)
                 print("正在识别图片%s..."%filename)
                 text = image_to_string(img, language = 'rt')
                 print("图片%s中的文字为->>>%s\n"%(filename, text))


if __name__=="__main__":
     rImgText();
     
