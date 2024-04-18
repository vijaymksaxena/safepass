def stego(color_image_path):
    import cv2
    #import matplotlib.pyplot as plt
    import pywt
    # Function to hide a grayscale image within a color image
    def hide_grayscale_in_color(color_image_path, grayscale_image_path, output_image_path):
        # Load the color image and grayscale image
        color_image = cv2.imread(color_image_path)
        # titles = ['Approximation', ' Horizontal detail',
        #           'Vertical detail', 'Diagonal detail']
        b, g, r = cv2.split(color_image)
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
            #ax = fig.add_subplot(1, 4, i + 1)
            #ax.imshow(a)
            #ax.set_title(titles[i], fontsize=10)
        #plt.show()
        grayscale_image = cv2.imread(grayscale_image_path, cv2.IMREAD_GRAYSCALE)
        # Check if images have the same dimensions
        if color_image.shape[:2] != grayscale_image.shape:
            raise ValueError("Color image and grayscale image must have the same dimensions.")
        # Split the color image into its color channels (B, G, R)
        b, g, r = cv2.split(color_image)
        # Replace the blue channel with the grayscale image
        b = grayscale_image
        # Merge the modified channels to create the new color image
        modified_color_image = cv2.merge((b, g, r))
        # Save the modified color image with the hidden grayscale image
        cv2.imwrite(output_image_path, modified_color_image)
        #plt.subplot(1,3,1)
        #plt.imshow(cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB))
        #plt.title("Color Image")
        #plt.subplot(1,3,2)
        #plt.imshow(grayscale_image,cmap='gray')
        #plt.title("Share2 Image")
        #plt.subplot(1,3,3)
        #plt.imshow(cv2.cvtColor(modified_color_image, cv2.COLOR_BGR2RGB))
        #plt.title("Watermark Image")
    # Paths to the input color image, grayscale image, and output image
    grayscale_image_path = 'share2.png'
    output_image_path = 'stegoimg.png'
    # Hide the grayscale image within the color image
    hide_grayscale_in_color(color_image_path, grayscale_image_path, output_image_path)
