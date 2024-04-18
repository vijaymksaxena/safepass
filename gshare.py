def share(text):
        from PIL import Image, ImageDraw, ImageFont
        def text_to_binary_image(text, image_width, image_height=100, font_size=100):
            # Create a blank image with white background
            image = Image.new('1', (image_width, image_height), color=1)
            draw = ImageDraw.Draw(image)  
            # Load a TrueType font
            font = ImageFont.truetype('arial.ttf', font_size)  
            # Calculate the text position
            text_width, text_height = draw.textsize(text, font=font)
            x = (image_width - text_width) // 2
            y = (image_height - text_height) // 2   
            # Draw the text on the image
            draw.text((x, y), text, fill=0, font=font)  
            return image
        wd=len(text)*72
        binary_image = text_to_binary_image(text,wd)
        new_size = (220, 200)  # Change this to your desired dimensions
        # Resize the image to the new size
        binary_image = binary_image.resize(new_size)
        binary_image.save("1.png")
        import numpy as np
        # Load the original binary image
        image_path = '1.png'
        image = Image.open(image_path)
        image_data = np.array(image)
        # Create random shares
        share1 = np.random.randint(0, 2, size=image_data.shape, dtype=np.uint8)
        share2 = image_data ^ share1
        # Convert the share matrices to images and save them
        share1_image = Image.fromarray(share1 * 255, 'L')
        share2_image = Image.fromarray(share2 * 255, 'L')
        share1_image.save('share1.png')
        share2_image.save('share2.png')