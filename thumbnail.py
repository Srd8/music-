import os

import aiofiles
import aiohttp
from PIL import Image, ImageDraw, ImageFont


def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage


async def gen_thumb(thumbnail, title, userid, ctitle):
    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail) as resp:
            if resp.status == 200:
                f = await aiofiles.open(f"search/thumb{userid}.png", mode="wb")
                await f.write(await resp.read())
                await f.close()
    image1 = Image.open(f"search/thumb{userid}.png")
    image2 = Image.open(f"MusicAndVideo/helpers/other/choose/rrc.png")
    image3 = changeImageSize(1280, 720, image1)
    image4 = changeImageSize(1280, 720, image2)
    image5 = image3.convert("RGBA")
    image6 = image4.convert("RGBA")
    Image.alpha_composite(image5, image6).save(f"search/temp{userid}.png")
    img = Image.open(f"search/temp{userid}.png")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("MusicAndVideo/helpers/other/choose/Roboto-Light.ttf", 55)
    font2 = ImageFont.truetype("MusicAndVideo/helpers/other/choose/finalfont.ttf", 65)
    draw.text(
        (20, 630),
        f"{title[:25]}...",
        fill="White",
        stroke_width=1,
        stroke_fill="black",
        font=font2,
    )
    draw.text(
        (20, 550),
        f"Playing on: {ctitle[:15]}...",
        fill="White",
        stroke_width=1,
        stroke_fill="black",
        font=font,
    )
    img.save(f"search/final{userid}.png")
    os.remove(f"search/temp{userid}.png")
    os.remove(f"search/thumb{userid}.png")
    final = f"search/final{userid}.png"
    return final
