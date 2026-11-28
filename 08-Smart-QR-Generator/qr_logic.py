import re
from urllib.parse import quote, urlsplit
import qrcode

def payload(kind, value, password='', security='WPA'):
    value = value.strip()
    if not value: raise ValueError('Enter a value first.')
    if kind == 'Website':
        if urlsplit(value).scheme not in ('http','https') or not urlsplit(value).netloc: raise ValueError('Enter a valid http or https URL.')
    elif kind == 'Email':
        if not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+',value): raise ValueError('Enter a valid email address.')
        return 'mailto:'+quote(value,safe='@')
    elif kind == 'Phone':
        if not re.fullmatch(r'\+?[0-9 ()-]{5,25}',value): raise ValueError('Enter a valid phone number.')
        return 'tel:'+re.sub(r'[ ()-]','',value)
    elif kind == 'Wi-Fi':
        def esc(s): return re.sub(r'([\\;,:\"])',r'\\\1',s)
        if security != 'nopass' and not password: raise ValueError('Enter the Wi-Fi password.')
        return f'WIFI:T:{security};S:{esc(value)};P:{esc(password) if security != "nopass" else ""};;'
    return value

def generate(data, size=512, color='#172B4D', level='M'):
    if not re.fullmatch(r'#[0-9a-fA-F]{6}',color): raise ValueError('Use a hex color such as #172B4D.')
    rgb=[int(color[i:i+2],16) for i in (1,3,5)]
    if sum(a*b for a,b in zip(rgb,(.2126,.7152,.0722)))>120: raise ValueError('Choose a darker color for readability.')
    qr=qrcode.QRCode(error_correction=getattr(qrcode.constants,'ERROR_CORRECT_'+level),box_size=1,border=4)
    qr.add_data(data); qr.make(fit=True)
    img=qr.make_image(fill_color=color,back_color='white').convert('RGB')
    from PIL import Image
    scale=size//img.width
    if scale<1: raise ValueError('Choose a larger image size.')
    img=img.resize((img.width*scale,img.height*scale),Image.Resampling.NEAREST)
    canvas=Image.new('RGB',(size,size),'white'); canvas.paste(img,((size-img.width)//2,(size-img.height)//2)); return canvas
