# By Julien H. Girard with the help of chatGPT - 2025
# Requires package
#   pip install qrcode[pil] Pillow
# To run
#   python supa_qrcode_prompt.py
# Change inputs at prompt. On a Mac you can drag and drop the logo file from finder, it will cope with the addtional space

import qrcode
from PIL import Image, ImageDraw

# Function to generate QR code with square or round dots
def generate_qr_code(url, logo_path=None, color='black', background_color='transparent', output_path='qr_code.png', dot_style='square'):
    # Step 1: Generate the QR code
    qr = qrcode.QRCode(
        version=1,  # Size of the QR code (1 is the smallest)
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction to allow a logo
        box_size=10,  # Size of each individual box in the QR code
        border=4,  # Thickness of the border
    )
    
    qr.add_data(url)
    qr.make(fit=True)
    
    # Get the matrix for the QR code (list of lists)
    matrix = qr.get_matrix()
    qr_width = len(matrix[0]) * qr.box_size  # Calculate width
    qr_height = len(matrix) * qr.box_size  # Calculate height

    # Create the QR code image
    if dot_style == 'round':
        # Custom round dot style using PIL
        qr_image = Image.new('RGBA', (qr_width, qr_height), (255, 255, 255, 0))  # Transparent background
        draw = ImageDraw.Draw(qr_image)

        # Create a round dot effect by drawing circles instead of squares
        for row in range(len(matrix)):
            for col in range(len(matrix[row])):
                if matrix[row][col]:  # If this cell is filled
                    # Calculate the position for the circle (dot)
                    x = col * qr.box_size
                    y = row * qr.box_size
                    draw.ellipse([x, y, x + qr.box_size, y + qr.box_size], fill=color)

        qr_image = qr_image.convert("RGBA")  # Ensure transparency if needed
    else:
        # Default square dot style
        qr_image = Image.new('RGBA', (qr_width, qr_height), (255, 255, 255, 0))  # Transparent background
        draw = ImageDraw.Draw(qr_image)

        # Draw the square QR code using the color provided
        for row in range(len(matrix)):
            for col in range(len(matrix[row])):
                if matrix[row][col]:  # If this cell is filled
                    # Calculate the position for the square (dot)
                    x = col * qr.box_size
                    y = row * qr.box_size
                    draw.rectangle([x, y, x + qr.box_size, y + qr.box_size], fill=color)

    # Step 2: Add a logo (if provided)
    if logo_path:
        logo_path = logo_path.strip()  # Strip any leading/trailing spaces from the logo path
        logo = Image.open(logo_path)
        
        # Resize logo to fit in the center of the QR code (30% of the QR code size)
        qr_width, qr_height = qr_image.size
        logo_size = int(qr_width * 0.3), int(qr_height * 0.3)  # Logo takes up 30% of the QR code size
        logo = logo.resize(logo_size, Image.ANTIALIAS)
        
        # Calculate position to center the logo
        logo_position = ((qr_width - logo_size[0]) // 2, (qr_height - logo_size[1]) // 2)
        
        # Ensure the area around the logo is void of QR code dots (transparent)
        logo_box = (logo_position[0], logo_position[1], logo_position[0] + logo_size[0], logo_position[1] + logo_size[1])
        qr_image.paste((255, 255, 255, 0), logo_box)  # Clear the area around the logo (transparent)

        # Paste the logo into the QR code (with transparency)
        qr_image.paste(logo, logo_position, logo.convert("RGBA"))

    # Step 3: Save the final QR code image
    qr_image.save(output_path)

    print(f"QR code generated and saved as {output_path}")


# Prompt the user for input
name = input("Enter the name for the output QR code file (e.g., my_qr_code, no need for extension): ")

# Prompt for URL
url = input("Enter the URL to encode in the QR code: ")

# Prompt for HEX color code (with default as black if not provided)
color = input("Enter the HEX color code for the QR code (e.g., #FF5733 or FF5733) [default: #000000]: ")
if not color:
    color = "#000000"  # Default to black if no color is provided
elif color[0] != '#':
    color = '#' + color  # Add the '#' if not already present

# Prompt for background color (optional, default is transparent)
background_color = input("Enter the background color for the QR code (e.g., white, transparent) [default: transparent]: ")
if not background_color:
    background_color = "transparent"  # Default to transparent

# Prompt for the logo path (optional)
logo_path = input("Enter the path to the logo image (include full path with image name, optional, press Enter to skip): ")
if not logo_path:
    logo_path = None  # If no logo path is provided, no logo will be added

# Prompt for dot style (square or round)
dot_style = input("Enter dot style for QR code (square or round) [default: square]: ")
if dot_style not in ['square', 'round']:
    dot_style = 'square'  # Default to square if invalid input

# Define output file path
output_path = f"{name}.png"

# Generate the QR code
generate_qr_code(url, logo_path, color, background_color, output_path, dot_style)
