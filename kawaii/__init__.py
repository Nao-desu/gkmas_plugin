from hoshino import Service,aiorequests
from io import BytesIO
import re, html ,os, base64
from PIL import Image
from ...groupmaster.switch import check_status

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

#(长,宽,边距)
size = {
    'kawaii':{
        1: (675, 900, 43),
        2: (900, 506, 46)
    },
    'amai':{
        1: (506, 900, 16),
        2: (900, 506, 16)
    },
    'shuki':{
        1: (540, 960, 21),
        2: (960, 540, 21)
    }
}


def process_frame(frame_image,tag):
    x, y = frame_image.size
    if x / y < 1.2:
        image_flame = Image.open(os.path.join(path, f"{tag}1.png"))
        a,b,c = size[tag][1]
        d = a - c*2
        e = b - c*2
        if x / y < d / e:
            x1, y1 = x, x / (d / e)
        else:
            x1, y1 = y * d / e, y
        _d = c
        x2, y2 = a, b
        x3, y3 = d, e
    else:
        image_flame = Image.open(os.path.join(path, f"{tag}2.png"))
        a,b,c = size[tag][2]
        d = a - c*2
        e = b - c*2
        if x / y < d / e:
            x1, y1 = x, x / (d / e)
        else:
            x1, y1 = y * d / e, y
        _d = c
        x2, y2 = a, b
        x3, y3 = d, e

    frame_image = frame_image.crop((abs(int((x1 - x) / 2)), abs(int((y1 - y) / 2)), int((x1 + x) / 2), int((y1 + y) / 2)))
    frame_image = frame_image.resize((x3, y3))
    bg = Image.new('RGBA', (x2, y2), (255, 255, 255, 255))
    bg.paste(frame_image, (_d, _d))
    bg.paste(image_flame, (0, 0), image_flame)
    return bg.convert("RGB")

async def send_msg(bot, ev, tag):
    image_data = await get_pic(ev)
    image = Image.open(image_data)
    frames = []
    durations = []

    if image.format == 'GIF' and hasattr(image, 'n_frames'):
        for frame in range(image.n_frames):
            image.seek(frame)
            frame_image = image.copy()
            frame_image = process_frame(frame_image,tag)
            frames.append(frame_image)
            durations.append(image.info['duration'] if 'duration' in image.info else 100)
    else:
        processed_image = process_frame(image,tag)
        frames.append(processed_image)

    output_image = BytesIO()
    if len(frames) > 1:
        frames[0].save(output_image, format='GIF', save_all=True, append_images=frames[1:], loop=0, duration=durations)
    else:
        frames[0].save(output_image, format='JPEG')

    base64_str = f'base64://{base64.b64encode(output_image.getvalue()).decode()}'
    msg = f'[CQ:image,file={base64_str}]'
    await bot.send(ev, msg)

@sv.on_prefix("卡哇伊")
@check_status('卡哇伊')
async def kawaii(bot, ev):
    await send_msg(bot, ev, 'kawaii')

@sv.on_prefix("喜欢甜食?","喜欢甜食？")
@check_status('卡哇伊')
async def amai(bot, ev):
    await send_msg(bot, ev, 'amai')
    
@sv.on_prefix("shuki")
@check_status('卡哇伊')
async def shuki(bot, ev):
    await send_msg(bot, ev, 'kawaii')
