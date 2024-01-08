# import modules
import qrcode
from PIL import Image, ImageDraw
 
# taking image which user wants 
# in the QR code center
Logo_link = 'favicon.png'
 
logo = Image.open(Logo_link)
 
# taking base width
basewidth = 100
 
# adjust image size
wpercent = (basewidth/float(logo.size[0]))
hsize = int((float(logo.size[1])*float(wpercent)))
logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)

# Create a function to generate QR code with concentric circles and image
def generate_concentric_qr(url, logo, basewidth, QRcolor, output_path='output.png'):
    # Create a QR code
    QRcode = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H
    )
    QRcode.add_data(url)
    QRcode.make()
    
    # Create a blank image for the QR code
    QRimg = QRcode.make_image(fill_color=QRcolor, back_color="white").convert('RGB')

    # Draw concentric circles around the QR code
    draw = ImageDraw.Draw(QRimg)
    for radius in range(20, 100, 20):  # Adjust the range based on your preference
        draw.ellipse(
            (pos[0] - radius, pos[1] - radius, pos[0] + radius, pos[1] + radius),
            outline='black', width=2
        )

    # Set the size and position of the image to be pasted
    pos = ((QRimg.size[0] - logo.size[0]) // 2, (QRimg.size[1] - logo.size[1]) // 2)
    
    # Paste the logo onto the QR code
    QRimg.paste(logo, pos)
    
    # Save the QR code with concentric circles and image
    QRimg.save(output_path)
    print(f'QR code with concentric circles and image saved to {output_path}')

# Example usage
url = 'https://www.geeksforgeeks.org/'
QRcolor = 'Green'
generate_concentric_qr(url, logo, basewidth, QRcolor, output_path='gfg_QR.png')
