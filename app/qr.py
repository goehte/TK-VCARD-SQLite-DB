# -*- coding: utf-8 -*-
# app/qr.py
# https://pypi.org/project/qrcode/

#import Image, ImageDraw
from PIL.Image import core as image
import qrcode

from .vcard import vcard_string_generator

def qr_vcard_generator(f_name, l_name, company, email, url, cell_w, phone_w, cell_h, phone_h, title, role, categories, notes):

  vcard_str = vcard_string_generator(f_name, l_name, company, email, url, cell_w, phone_w, cell_h, phone_h, title, role, categories, notes)
  #print(vcard_str)
   
  qr = qrcode.QRCode(
      version=1,
      error_correction=qrcode.constants.ERROR_CORRECT_L,
      box_size=4,
      border=4,
  )
  qr.add_data(vcard_str)
  qr.make(fit=True)
  
  img = qr.make_image(fill_color="black", back_color="white")
  type(img)  # qrcode.image.pil.PilImage
  img.save("./app/qr.png")

  return