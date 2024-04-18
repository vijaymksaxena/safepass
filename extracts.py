def extract(hidden_color_image_path):
    import cv2
    import pywt
    #import matplotlib.pyplot as plt
    # Function to extract the hidden grayscale image from a color image
    def extract_grayscale_from_color(hidden_color_image_path, extracted_grayscale_image_path):
        # Load the hidden color image
        hidden_color_image = cv2.imread(hidden_color_image_path)
        #titles = ['Approximation', ' Horizontal detail',
        #          'Vertical detail', 'Diagonal detail']
        b, g, r = cv2.split(hidden_color_image)
        coeffs_b = pywt.dwt2(b, 'haar')
        coeffs_g = pywt.dwt2(g, 'haar')
        coeffs_r = pywt.dwt2(r, 'haar')
        (LL_b, (LH_b, HL_b, HH_b)) = coeffs_b
        (LL_g, (LH_g, HL_g, HH_g)) = coeffs_g
        (LL_r, (LH_r, HL_r, HH_r)) = coeffs_r
        #LL=cv2.merge((LL_b, LL_g, LL_r))
        #LH=cv2.merge((LH_b, LH_g, LH_r))
        #HL=cv2.merge((HL_b, HL_g, HL_r))
        #HH=cv2.merge((HH_b, HH_g, HH_r))
        #fig = plt.figure(figsize=(12, 3))
        #for i, a in enumerate([LL, LH, HL, HH]):
        #    ax = fig.add_subplot(1, 4, i + 1)
        #    ax.imshow(a)
        #    ax.set_title(titles[i], fontsize=10)
        #plt.show()
        # Extract the blue channel, which contains the hidden grayscale image
        extracted_grayscale_image = hidden_color_image[:, :, 0]
        # Save the extracted grayscale image
        cv2.imwrite(extracted_grayscale_image_path, extracted_grayscale_image)
        #plt.subplot(1,2,1)
        #plt.imshow(cv2.cvtColor(hidden_color_image, cv2.COLOR_BGR2RGB))
        #plt.title("Watermark Image")
        #plt.subplot(1,2,2)
        #plt.imshow(extracted_grayscale_image,cmap='gray')
        #plt.title("Share2 Image")
    extracted_grayscale_image_path = 'extracted_grayscale_image.png'
    # Extract the hidden grayscale image from the color image
    extract_grayscale_from_color(hidden_color_image_path, extracted_grayscale_image_path)
    from PIL import Image
    import numpy as np
    # Load the share images
    share1_path = 'share1.png'
    share2_path = 'extracted_grayscale_image.png'
    share1_image = Image.open(share1_path)
    share2_image = Image.open(share2_path)
    # Convert share images to numpy arrays
    share1 = np.array(share1_image) / 255
    share2 = np.array(share2_image) / 255
    # Ensure both shares have the same data type and dimensions
    share1 = share1.astype(np.uint8)
    share2 = share2.astype(np.uint8)
    # Reconstruct the original image using XOR
    reconstructed_image = share1 ^ share2
    # Convert the numpy array back to an image and save it
    reconstructed_image = Image.fromarray((reconstructed_image * 255).astype(np.uint8), 'L')
    reconstructed_image.save('reconstructed_image.png')
    #plt.figure()
    #plt.subplot(1,3,1)
    #plt.imshow(share1_image,cmap='gray')
    #plt.title("Share1 Image")
    #plt.subplot(1,3,2)
    #plt.imshow(share2_image,cmap='gray')
    #plt.title("Share2 Image")
    #plt.subplot(1,3,3)
    #plt.imshow(reconstructed_image,cmap='gray')
    #plt.title("Combine Image")
    
