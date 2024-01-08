import qrcode
from PIL import Image, ImageDraw
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import CircleModuleDrawer, SquareModuleDrawer

def show_qr(img):
    img.show()

# Generate a regular square QR code
qr = qrcode.QRCode(
    version=10,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=18,
    mask_pattern=4,
)
qr.add_data('https://stackoverflow.com/')
qr.make(fit=True)

img = qr.make_image(
    fill_color="white",
    back_color=None,
    image_factory=StyledPilImage,
    module_drawer=CircleModuleDrawer(resample_method=None),
    eye_drawer=SquareModuleDrawer(),
)

# Add a circular ring around the QR code
img_copy = img.copy()
draw = ImageDraw.Draw(img_copy)
draw.ellipse(
    (30, 30, img_copy.size[1] - 30, img_copy.size[1] - 30),
    fill=None,
    outline='black',
    width=30
)

# Fill the negative space with a pattern
width, height = img.size
left = 0
top = height // 3
right = width
bottom = 2 * height // 3

img_copy = img.copy()
draw_rec = ImageDraw.Draw(img_copy)
draw_rec.rectangle(
    (left, top, right, bottom),
    fill=None,
    outline='red',
    width=5
)

cropped_section = img.crop((left, top, right, bottom))
rotated_crop = cropped_section.copy()
rotated_crop = rotated_crop.rotate(90, expand=True)

# Fill top, bottom, left, and right
img.paste(cropped_section, (0, -cropped_section.size[1] // 2 + 20))
img.paste(cropped_section, (0, img.size[1] - cropped_section.size[1] // 2 - 20))
img.paste(rotated_crop, (-rotated_crop.size[0] // 2 + 20, 0))
img.paste(rotated_crop, (img.size[0] - rotated_crop.size[0] // 2 - 20, 0))

# Add the circular ring back in
draw = ImageDraw.Draw(img)
draw.ellipse(
    (30, 30, img.size[1] - 30, img.size[1] - 30),
    fill=None,
    outline='black',
    width=30
)

# Draw a mask ring to remove the pattern outside the circular ring
draw.ellipse(
    (-rotated_crop.size[0],
     -cropped_section.size[1],
     img.size[1] + rotated_crop.size[0],
     img.size[1] + cropped_section.size[1]
     ),
    fill=None,
    outline='white',
    width=340
)

# Convert the image to RGBA and set a transparent background
img = img.convert("RGBA")
opaque_pixel = (0, 0, 0, 255)
transparent_pixel = (255, 255, 255, 0)

img_data = img.getdata()
new_pixels = []
for item in img_data:
    if item[0] == 255 and item[1] == 255 and item[2] == 255:
        new_pixels.append(transparent_pixel)
    else:
        new_pixels.append(opaque_pixel)
img.putdata(new_pixels)

# Create a background image and paste the QR code on top
background_img = Image.new("RGBA", img.size)
background_draw = ImageDraw.Draw(background_img)
background_draw.rectangle(
    (0, 0, background_img.size[0], background_img.size[1]),
    fill="grey",
    outline=None
)
background_img.paste(img, (0, 0), img)

# Show the final result
show_qr(background_img)

# taking image which user wants 
# in the QR code center
Logo_link = 'favicon.png'
 
logo = Image.open(Logo_link)

basewidth = 100

# adjust image size
wpercent = (basewidth/float(logo.size[0]))
hsize = int((float(logo.size[1])*float(wpercent)))
logo = logo.resize((basewidth, hsize), Image.LANCZOS)
QRcode = qrcode.QRCode(
    error_correction=qrcode.constants.ERROR_CORRECT_H
)

# set size of QR code
pos = ((img.size[0] - logo.size[0]) // 2,
       (img.size[1] - logo.size[1]) // 2)
img.paste(logo, pos)

# Save the QR code with a transparent background
img.save('circl_qr_code.png', "PNG", quality=100)
