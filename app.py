import streamlit as st
from streamlit_image_select import image_select
import re
import pandas as pd
import math
import random
import smtplib
import pickle
import os


st.title('Safe Pass')
st.subheader("One Place to Secure Your Passwords")
st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 370px !important; # Set the width to your desired value
        }
    </style>
    """,
    unsafe_allow_html=True,
)
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

def stego(color_image_path):
    import cv2
    #import matplotlib.pyplot as plt
    import pywt
    # Function to hide a grayscale image within a color image
    def hide_grayscale_in_color(color_image_path, grayscale_image_path, output_image_path):
        # Load the color image and grayscale image
        color_image = cv2.imread(color_image_path)
        b, g, r = cv2.split(color_image)
        coeffs_b = pywt.dwt2(b, 'haar')
        coeffs_g = pywt.dwt2(g, 'haar')
        coeffs_r = pywt.dwt2(r, 'haar')
        (LL_b, (LH_b, HL_b, HH_b)) = coeffs_b
        (LL_g, (LH_g, HL_g, HH_g)) = coeffs_g
        (LL_r, (LH_r, HL_r, HH_r)) = coeffs_r
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
    # Paths to the input color image, grayscale image, and output image
    grayscale_image_path = 'share2.png'
    output_image_path = 'stegoimg.png'
    # Hide the grayscale image within the color image
    hide_grayscale_in_color(color_image_path, grayscale_image_path, output_image_path)
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
        # Extract the blue channel, which contains the hidden grayscale image
        extracted_grayscale_image = hidden_color_image[:, :, 0]
        # Save the extracted grayscale image
        cv2.imwrite(extracted_grayscale_image_path, extracted_grayscale_image)
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

import sqlite3
conn = sqlite3.connect('data.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(FirstName TEXT,LastName TEXT,Email TEXT,Mobile TEXT,password TEXT)')
def add_userdata(FirstName,LastName,Email,Mobile,password):
    c.execute('INSERT INTO userstable(FirstName,LastName,Email,Mobile,password) VALUES (?,?,?,?,?)',(FirstName,LastName,Email,Mobile,password))
    conn.commit()
def login_user(Email,password):
    c.execute('SELECT * FROM userstable WHERE Email =? AND password = ?',(Email,password))
    data = c.fetchall()
    return data
def create_site():
    c.execute('CREATE TABLE IF NOT EXISTS userstable1(emil TEXT,site TEXT,user TEXT,pss TEXT)')
def add_site(emil,site,user,pss):
    c.execute('INSERT INTO userstable1(emil,site,user,pss) VALUES (?,?,?,?)',(emil,site,user,pss))
    conn.commit()
def view_site(emil):
	c.execute("SELECT * FROM userstable1 WHERE emil=?", (emil,))
	data = c.fetchall()
	return data
def delete_site(site):
    c.execute("DELETE FROM userstable1 WHERE site="+"'"+site+"'")
    conn.commit()


menu = ["Home","Signup","Login"]
choice = st.sidebar.selectbox("Menu",menu)
if choice=="Home":
    testp="<p style='font-size:20px'>SafePass is the easier, safer way to unlock your digital world. It’s an application you can download on all your PC to remove the hassle of passwords. Get started by logging in to the Master password app using unique factors image. From there, the app works quietly in the background to make your current passwords stronger, remembers them and instantly logs you in so you don’t have to. </p>"
    st.markdown(testp, unsafe_allow_html=True)
    st.image("main.gif")
    # if os.path.isfile("reconstructed_image.png"):
    #     os.remove("reconstructed_image.png")
    #     os.remove("extracted_grayscale_image.png")
    #     os.remove("stegoimg.png")
    #     os.remove("share1.png")
    #     os.remove("share2.png")
    #     os.remove("1.png")
    #     os.remove("otp.pkl")
    
if choice=="Signup":
    st.text("Welcome Signup")
    Fname=st.text_input("First Name")
    Lname=st.text_input("Last Name")
    Email=st.text_input("Email")
    Mobile=st.text_input("Mobile")
    Password=st.text_input("Passwod",type="password")
    st.text_input("Confirm Password",type="password")
    rn = [1,2,4,6]
    img = image_select(
        label="Select Hide Image",
        images=[
            "images/"+str(rn[0])+".jpg",
            "images/"+str(rn[1])+".jpg",
            "images/"+str(rn[2])+".jpg",
            "images/"+str(rn[3])+".jpg",
        ],
    )
    b=st.button("Submit")
    if b:
        pattern=re.compile("(0|91)?[7-9][0-9]{9}")
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if (pattern.match(Mobile)):
            if re.fullmatch(regex, Email):
                create_usertable()
                share(Password)
                stego(img)
                add_userdata(Fname,Lname,Email,Mobile,str(img))
                st.success("Success")
            else:
                st.warning("Not Valid Email")         
        else:
            st.warning("Not Valid Mobile Number")

if choice=="Login":    
    Email=st.sidebar.text_input("Email")
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if re.fullmatch(regex, Email):
        if st.sidebar.button("Generate OTP"):
            digits="0123456789"
            OTP=""
            for i in range(6):
                OTP+=digits[math.floor(random.random()*10)]
            otp = OTP + " is your OTP"
            msg= otp
            #s = smtplib.SMTP('smtp.gmail.com', 587)
            #s.starttls()
            #s.login("Emil", "hhj")
            #emailid = Email
            #s.sendmail('&&&&&&&&&&&',emailid,msg)
            st.write(OTP)
            pickle.dump(OTP, open("otp.pkl","wb"))
        ss=st.sidebar.text_input("OTP",type="password")
        rn = [2,1,6,4]
        with st.sidebar:     
            img1 = image_select(
                label="Select Password Image",
                images=[
                    "images/"+str(rn[0])+".jpg",
                    "images/"+str(rn[1])+".jpg",
                    "images/"+str(rn[2])+".jpg",
                    "images/"+str(rn[3])+".jpg",
                ],
            )
        if st.sidebar.checkbox("Login"):
            result = login_user(Email,str(img1))
            OTP=pickle.load(open("otp.pkl","rb"))
            if result and ss==OTP:
                    img1="stegoimg.png"
                    extract(img1)       
                    st.success("Login Sucess")
                    sts=st.text_input("Enter Delete Site")
                    if st.button("Delete"):
                        delete_site(sts)
                        st.success("Deleted Sucess")
                    site=st.text_input("Site")
                    user=st.text_input("Email/Password")
                    pss=st.text_input("Password",type="password")
                    if st.button("Add to database"):
                        create_site()
                        add_site(Email,site,user,pss)
                        st.success("database update Sucess")
                    user_result = view_site(Email)
                    clean_db = pd.DataFrame(user_result,columns=["Email","Site","User","Password"])
                    st.dataframe(clean_db)
            else:
                st.error("Wrong OTP/Image")
    else:
        st.warning("Not Valid Email")
        
        


        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
