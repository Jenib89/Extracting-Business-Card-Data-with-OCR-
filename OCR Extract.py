import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import easyocr
import mysql.connector as sql
import os
import re


st.title("OCR-Extract")

# CREATING MENU
selected = option_menu(None, ["Extract Data","Modify Details"], )
                       

# INITIALIZING THE EasyOCR READER
reader = easyocr.Reader(['en'])

mydb = sql.connect(host="localhost",
                   user="root",
                   password="Jeni27589$",
                   database= "business_card",
		   auth_plugin ="mysql_native_password"
                  )
mycursor = mydb.cursor(buffered=True)


mycursor.execute('''CREATE TABLE IF NOT EXISTS card_data
                   (id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    company_name TEXT,
                    card_holder TEXT,
                    designation TEXT,
                    mobile_number VARCHAR(50),
                    email TEXT,
                    website TEXT,
                    area TEXT,
                    city TEXT,
                    state TEXT,
                    pin_code VARCHAR(10),
                    image LONGBLOB
                    )''')

        
if selected == "Extract Data":
    st.markdown("##### Upload a Business Card to extract details")
    uploaded_card = st.file_uploader("upload here",label_visibility="collapsed",type=["png","jpeg","jpg"])
        
    if uploaded_card is not None: 
        # card is saved to get the path
        def save_card(uploaded_card):
            with open(os.path.join("uploaded_cards",uploaded_card.name), "wb") as f:
                f.write(uploaded_card.getbuffer())   
        save_card(uploaded_card)
              
 
        #easy OCR
        saved_img = os.getcwd()+ "\\" + "uploaded_cards"+ "\\"+ uploaded_card.name #filename from current directory
        result = reader.readtext(saved_img,detail = 0,paragraph=True) #filenmae or path to be given
        st.image(uploaded_card)
        
               
        s = ' '.join(result)
        url_s = re.findall(r"[www|WWW|wwW]+[\.|\s]+[a-zA-Z0-9]+[\.|\][a-zA-Z]+", s)
        url = re.sub('[WWW|www|wwW]+ ', 'www.', url_s[0]) if url_s else ""
        email_s = re.findall(r"[a-zA-Z0-9\.\-+_]+@[a-zA-Z0-9\.\-+_]+\.[a-z]+", s)
        email = email_s[0] if email_s else ""
        mob_s = re.findall(r"[6-9]\d{9}|[\+9]\d{12}|[\+91]+\-\d{3}\-\d{4}|[\+1-2]\d{3}\-\d{3}\-\d{4}|[1-2]\d{2}\-\d{3}\-\d{4}|[0-9]{10}", s)
        mob = ', '.join(mob_s) if mob_s else ""
        ad_s = re.findall(r"[0-9]{1,4}\s[A-Za-z]+\s[A-Za-z]+[\s|\.|\,]\,\s[A-Za-z]+[\|\,|\;]\s[A-Za-z]+[\,\s|\,\s|\;\s|\s]+[0-6]{5,7}", s)
        ad = re.findall(r"([0-9]{1,4}\s[A-Za-z]+\s[A-Za-z]+)[\s|\.|\,]\,\s([A-Za-z]+)[\|\,|\;]\s([A-Za-z]+)[\,\s|\,\s|\;\s|\s]+([0-6]{5,7})", s)
        area_v = ad[0][0] if ad else ""
        city_v = ad[0][1] if ad else ""
        state_v = ad[0][2] if ad else ""
        pin = ad[0][3] if ad else ""
        l_s = result.copy()
        x = l_s[0] if l_s else ""
        des_s = re.findall(r"[A-Za-z]+[\s|\s\&\s]+[A-Za-z]+$", x)
        des = des_s[0] if des_s else ""
        nam_s = x.replace(des, '')
        nam_l = re.findall(r"[A-Za-z]+\s[A-Za-z]+|[A-Za-z]+", nam_s)
        name = nam_l[0] if nam_l else ""
        companyname = l_s[-1] if l_s else ""
        cmp = len(l_s)-1
        
        


        def img_to_binary(file):
        # Convert image data to binary format to store in db
         with open(file, 'rb') as file:
            binaryData = file.read()
         return binaryData

        extracted_data ={"company_name": companyname,
        "card_holder_name": name,
        "designation": des,
        "mobile_number": mob,
        "email_address": email,
        "website": url,
        "area": area_v,
        "city": city_v,
        "state": state_v,
        "pincode": pin,
        "image" :  img_to_binary(saved_img)
         }

        #st.write(extracted_data)
        df_data = pd.DataFrame([extracted_data])
        st.write(df_data)

       

        if st.button("Insert to DB"):
            for i,row in df_data.iterrows():                
                sql = """INSERT INTO card_data(company_name,card_holder,designation,mobile_number,email,website,area,city,state,pin_code,image)
                         VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                values = (
                       extracted_data["company_name"],
                       extracted_data["card_holder_name"],
                       extracted_data["designation"],
                       extracted_data["mobile_number"],
                       extracted_data["email_address"],
                       extracted_data["website"],
                       extracted_data["area"],
                       extracted_data["city"],
                       extracted_data["state"],
                       extracted_data["pincode"],
                       img_to_binary(saved_img)
                        )

                mycursor.execute(sql, values)                
                mydb.commit()
            st.success("Inserted successfully")
        
# MODIFY MENU    
if selected == "Modify Details":
    tab1, tab2 = st.tabs(["Update", "Delete"])
    with tab1:
            st.header("Update Card Data")
            mycursor.execute("SELECT card_holder FROM card_data")
            result = mycursor.fetchall()
            business_cards = {}
            for row in result:
                business_cards[row[0]] = row[0] # to store the modified data with the same key and values
            selected_card = st.selectbox("Select a card holder name and modify data below to update", list(business_cards.keys()))
            
            mycursor.execute("select company_name,card_holder,designation,mobile_number,email,website,area,city,state,pin_code from card_data WHERE card_holder=%s",
                            (selected_card,))
            result = mycursor.fetchone()
            
            company_name = st.text_input("Company_Name", result[0])
            card_holder = st.text_input("Card_Holder", result[1])
            designation = st.text_input("Designation", result[2])
            mobile_number = st.text_input("Mobile_Number", result[3])
            email = st.text_input("Email", result[4])
            website = st.text_input("Website", result[5])
            area = st.text_input("Area", result[6])
            city = st.text_input("City", result[7])
            state = st.text_input("State", result[8])
            pin_code = st.text_input("Pin_Code", result[9])

            if st.button("Update"):                
                mycursor.execute("""UPDATE card_data SET company_name=%s,card_holder=%s,designation=%s,mobile_number=%s,email=%s,website=%s,area=%s,city=%s,state=%s,pin_code=%s
                                    WHERE card_holder=%s""", (company_name,card_holder,designation,mobile_number,email,website,area,city,state,pin_code,selected_card))
                mydb.commit()
                st.success("Updated successfully.")

    with tab2:
      st.header("Delete Card Data")
      mycursor.execute("SELECT card_holder FROM card_data")
      result = mycursor.fetchall()
      business_cards = {}
      for row in result:
          business_cards[row[0]] = row[0]
      selected_card = st.selectbox("Select a card holder name to Delete", list(business_cards.keys()))
             
      if st.button("Delete"):
         mycursor.execute(f"DELETE FROM card_data WHERE card_holder='{selected_card}'")
         mydb.commit()       
         st.success(f"{selected_card} details deleted.")
   
 
    
    if st.button("View modified data"):
        mycursor.execute("select company_name,card_holder,designation,mobile_number,email,website,area,city,state,pin_code from card_data")
        updated_df = pd.DataFrame(mycursor.fetchall(),columns=["Company_Name","Card_Holder","Designation","Mobile_Number","Email","Website","Area","City","State","Pin_Code"])
        st.write(updated_df)
