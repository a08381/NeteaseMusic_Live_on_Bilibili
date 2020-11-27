from PIL import Image
import qrcode

def make_qrcode(url: str, img: Image=None) -> Image:
    qr = qrcode.QRCode(version=5, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=8, border=4)
    qr.add_data(url)
    qr.make()

    image = qr.make_image()
    image.convert("RGBA")

    if img:
        img_w, img_h = image.size
        factor = 4
        size_w = int(img_w / factor)
        size_h = int(img_h / factor)

        icon_w, icon_h = img.size
        if icon_w > size_w:
            icon_w = size_w
        if icon_h > size_h:
            icon_h = size_h
        img = img.resize((icon_w, icon_h), Image.ANTIALIAS)

        w = int((img_w - icon_w) / 2)
        h = int((img_h - icon_h) / 2)
        img = img.convert("RGBA")
        image.paste(img, (w, h), img)

    return image

