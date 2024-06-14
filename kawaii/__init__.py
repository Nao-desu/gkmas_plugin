from hoshino import Service,aiorequests
from io import BytesIO
import re, html ,os, base64
from PIL import Image

sv = Service("gkmas_kawaii")

async def get_pic(ev):
    pic = None
    match = re.findall(r'(\[CQ:image,file=.*?,url=.*?\])', html.unescape(str(ev.message)))
    if not match:
        url = ev.avatar
    else:
        url = re.search(r"\[CQ:image,file=(.*),url=(.*)\]", match[0]).group(2)
    resp = await aiorequests.get(url)
    pic = await resp.content
    pic = BytesIO(pic)
    return pic

path = os.path.dirname(__file__)
img1 = os.path.join(path, "kwy1.png")
img2 = os.path.join(path, "kwy2.png")

@sv.on_prefix("卡哇伊")
async def kawaii(bot, ev):
    image = await get_pic(ev)
    image = Image.open(image)
    x,y = image.size
    if x/y < 1.2:
        image_flame = Image.open(img1)
        if x/y < 589/814:x1,y1 = x,x/(589/814)
        else:x1,y1 = y*589/814,y
        d = 43
        x2,y2 = 675,900
        x3,y3 = 589,814
    else:
        image_flame = Image.open(img2)
        if x/y < 808/414:x1,y1 = x,x/(808/414)
        else:x1,y1 = y*808/414,y
        d = 46
        x2,y2 = 900,506
        x3,y3 = 808,414
    image = image.crop((abs(int((x1-x)/2)),abs(int((y1-y)/2)),int((x1+x)/2),int((y1+y)/2)))
    image = image.resize((x3,y3),Image.ANTIALIAS)
    bg = Image.new('RGBA',(x2,y2),(255,255,255,255))
    bg.paste(image,(d,d))
    bg.paste(image_flame,(0,0),image_flame)
    bg = bg.convert("RGB")
    image_bytes = BytesIO()
    bg.save(image_bytes, format='JPEG')
    base64_str = f'base64://{base64.b64encode(image_bytes.getvalue()).decode()}'
    msg = f'[CQ:image,file={base64_str}]'
    await bot.send(ev, msg)
