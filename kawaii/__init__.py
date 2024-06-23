from hoshino import Service,aiorequests
from io import BytesIO
import re, html ,os, base64
from PIL import Image,ImageSequence
import numpy as np
import cv2

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
    image_data = await get_pic(ev)
    image = Image.open(image_data)
    
    # 检查并压缩图片或GIF
    max_size = 1 * 1024 * 1024  # 1MB
    image_data = compress_image(image_data, image, max_size)
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

def compress_image(image_data, image, max_size):
    """
    压缩图片，使其大小小于指定的大小（单位：字节）
    """
    if image.format == 'GIF':
        # 对GIF图片进行压缩
        gif_frames = []
        durations = []

        # 读取GIF的每一帧并压缩
        for frame in ImageSequence.Iterator(image):
            frame_data = BytesIO()
            frame.save(frame_data, format="PNG")
            np_frame = np.frombuffer(frame_data.getvalue(), np.uint8)
            frame_img = cv2.imdecode(np_frame, cv2.IMREAD_UNCHANGED)

            quality = 90
            while True:
                encode_param = [int(cv2.IMWRITE_PNG_COMPRESSION), quality]
                result, encimg = cv2.imencode('.png', frame_img, encode_param)
                if not result or encimg.nbytes <= max_size:
                    break
                quality += 1

            compressed_frame = Image.open(BytesIO(encimg.tobytes()))
            gif_frames.append(compressed_frame)
            durations.append(frame.info['duration'] if 'duration' in frame.info else 100)

        # 创建新的GIF
        output_image = BytesIO()
        gif_frames[0].save(output_image, format='GIF', save_all=True, append_images=gif_frames[1:], loop=0, duration=durations)

        return output_image

    else:
        # 对非GIF图片进行压缩
        np_img = np.frombuffer(image_data.getvalue(), np.uint8)
        img = cv2.imdecode(np_img, cv2.IMREAD_UNCHANGED)

        quality = 90
        while image_data.getbuffer().nbytes > max_size:
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
            result, encimg = cv2.imencode('.jpg', img, encode_param)
            if not result:
                raise ValueError("图像编码失败")

            image_data = BytesIO(encimg.tobytes())

            if quality <= 5:
                break
            quality -= 5

        return image_data




