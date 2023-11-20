# Extracting-Business-Card-Data-with-OCR-

## Project Overview
 
   BizCardX is a user-friendly tool for extracting information from business cards. The tool uses OCR technology to recognize text on business cards and extracts the data into a SQL database after classification using regular expressions. Users can access the extracted information using a GUI built using streamlit.
   The BizCardX application is a simple and intuitive user interface that guides users through the process of uploading the business card image and extracting its information. The extracted information would be displayed in a clean and organized manner, and users would be able to easily add it to the database with the click of a button. Further the data stored in database can be easily Read, updated and deleted by user as per the requirement.


## Libraries/Modules used for the project!

   - Pandas - (To Create a DataFrame with the scraped data)
   - mysql.connector - (To store and retrieve the data)
   - Streamlit - (To Create Graphical user Interface)
   - EasyOCR - (To extract text from images)
     

   
## Steps

   
- Install the required libraries using the pip install command. Streamlit, mysql.connector, pandas, easyocr.
   
- Once user uploads a business card, the text present in the card is extracted by easyocr library.

- The extracted text is processed using regular expressions to get values for respective text classification as company name, card holder name, designation, mobile number, email address, website URL, area, city, state, and pin code using loops and some regular expression.

- The classified data is displayed on screen which can be further edited by user based on requirement.

- On Clicking Insert to DB the data gets stored in the MySQL Database. 

- Further with the help of Modify Details menu the uploaded data’s in SQL Database can be accessed for  Update ,Delete and view the modified data.

