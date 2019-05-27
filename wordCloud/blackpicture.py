from PIL import Image
im = Image.open('./5.jpg')
Img = im.convert('L')
threshold = 200
table = []
for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)
# 图片二值化
photo = Img.point(table, '1')
photo.save("./day.jpg")
