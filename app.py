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


menu = ["Home","Singup","Login"]
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
    
if choice=="Singup":
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
                #sh
                from gshare import share
                share(Password)
                #wtermrking
                from stegos import stego
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
                    #Extraction
                    from extracts import extract
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
        
        


        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
