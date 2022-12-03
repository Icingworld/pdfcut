from PIL import Image
import os
import io
import img2pdf
from pdf2image import convert_from_path
#https://blog.csdn.net/zhuoqingjoking97298/article/details/110222668 (img2pdf)
#https://blog.csdn.net/zbj18314469395/article/details/98329442 (pdf2image)

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False

def pdf_to_img():
    print("输入pdf路径：")
    filepath = input()
    print("正在加载pdf···")
    global name
    global Path
    for i in range(1,999):
        pathcheck = filepath[-i:-i+1]
        if pathcheck == "/":
            name = filepath[-i+1:-4]
            break
    dirs = filepath[:-4] + "/"
    if not os.path.exists(dirs):
        os.makedirs(dirs)
    imgs = convert_from_path(filepath)
    for i, image in enumerate(imgs):
        #这里规定分离的图片命名位数
        t = str(i).zfill(3)
        image.save(dirs + t + ".png", "PNG")
        print(t + ".png已分离")
        Path = dirs
    print("pdf文件切割完毕\n")

def open_(path):
    im = Image.open(path)
    global height_half
    global height
    global width
    height_half = im.size[1]/2
    height = im.size[1]
    width = im.size[0]

def cut(filepath,height,i):
    j = str(2 * i + 1)
    l = str(2 * i +2)
    convertpath = path + "convert/"
    if not os.path.exists(convertpath):
        os.makedirs(convertpath)
    img = Image.open(filepath)
    imup = img.crop((300, 280, width - 1 - 300, height_half-100))
    #https://blog.csdn.net/weixin_39777626/article/details/82774270
    #如果输出为png无法写入pdf，因为无法处理alpha通道
    imup.convert("RGB").save(convertpath + j + ".jpg")
    print("已输出" + j + ".jpg")
    imdown = img.crop((300, height_half + 90, width - 1 -300, height-289))
    imdown.convert("RGB").save(convertpath + l + ".jpg")
    print("已输出" + l + ".jpg")

def run():
    global path
    if Path[-1:] == "/":
        path = Path
    else:
        path = Path + "/"
    filenames = os.listdir(path)
    for i in range(0, 999):
        n = str(i).zfill(3)
        for file in filenames:
            filenum = str(file)[-7:-4]
            if filenum == n:
                filepath = path + file
                open_(filepath)
                cut(filepath,height,i)
    print("素材分割完毕\n")

def img_to_pdf(path):
    with open(path + "convert/" + name + ".pdf", "wb") as f:
        filelist = os.listdir(path + "convert/")
        pnglist = []
        for m in range(1,999):
            u = str(m)
            for filename in filelist:
                check00 = filename[-6:-5]
                check000 = filename[-7:-6]
                if not is_number(check00):
                    if u == filename[-5:-4]:
                        pnglist.append(path + "convert/" +filename)
                elif not is_number(check000):
                    if u == filename[-6:-4]:
                        pnglist.append(path + "convert/" +filename)
                else:
                    if u == filename[-7:-4]:
                        pnglist.append(path + "convert/" +filename)
        tran = img2pdf.convert(pnglist)
        f.write(tran)
    print("pdf文件组合完毕")

if __name__ == "__main__":
    global path
    pdf_to_img()
    run()
    img_to_pdf(path)
    #by Jzw 2021-3-11
