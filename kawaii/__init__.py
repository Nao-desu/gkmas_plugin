from hoshino import Service,aiorequests
from io import BytesIO
import re, html ,os, base64
from PIL import Image,ImageSequence
import numpy as np
import cv2
from ...groupmaster.switch import sdb

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

def process_frame(frame_image):
    x, y = frame_image.size
    if x / y < 1.2:
        image_flame = Image.open(img1)
        if x / y < 589 / 814:
            x1, y1 = x, x / (589 / 814)
        else:
            x1, y1 = y * 589 / 814, y
        d = 43
        x2, y2 = 675, 900
        x3, y3 = 589, 814
    else:
        image_flame = Image.open(img2)
        if x / y < 808 / 414:
            x1, y1 = x, x / (808 / 414)
        else:
            x1, y1 = y * 808 / 414, y
        d = 46
        x2, y2 = 900, 506
        x3, y3 = 808, 414

    frame_image = frame_image.crop((abs(int((x1 - x) / 2)), abs(int((y1 - y) / 2)), int((x1 + x) / 2), int((y1 + y) / 2)))
    frame_image = frame_image.resize((x3, y3))
    bg = Image.new('RGBA', (x2, y2), (255, 255, 255, 255))
    bg.paste(frame_image, (d, d))
    bg.paste(image_flame, (0, 0), image_flame)
    return bg.convert("RGB")


@sv.on_prefix("卡哇伊")
async def kawaii(bot, ev):
    status = sdb.get_status(ev.real_group_id,'卡哇伊')
    if not status:
        return
    image_data = await get_pic(ev)
    if len(image_data.getvalue()) >= 1024 * 1024:
        await bot.send(ev, "传入图片过大，可能无法输出结果")
    image = Image.open(image_data)
    frames = []
    durations = []

    if image.format == 'GIF' and hasattr(image, 'n_frames'):
        for frame in range(image.n_frames):
            image.seek(frame)
            frame_image = image.copy()
            frame_image = process_frame(frame_image)
            frames.append(frame_image)
            durations.append(image.info['duration'] if 'duration' in image.info else 100)
    else:
        processed_image = process_frame(image)
        frames.append(processed_image)

    output_image = BytesIO()
    if len(frames) > 1:
        frames[0].save(output_image, format='GIF', save_all=True, append_images=frames[1:], loop=0, duration=durations)
    else:
        frames[0].save(output_image, format='JPEG')

    base64_str = f'base64://{base64.b64encode(output_image.getvalue()).decode()}'
    msg = f'[CQ:image,file={base64_str}]'
    await bot.send(ev, msg)




