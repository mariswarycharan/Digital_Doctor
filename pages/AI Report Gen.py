import streamlit as st
from gtts import gTTS
import pickle,pygame
import pandas as pd
from  PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import datetime
from googletrans import Translator
import base64
from st_clickable_images import clickable_images
from bs4 import BeautifulSoup
import requests
import sqlite3
import webbrowser 
import people_also_ask as paa
from ultralytics import YOLO
from playsound import playsound
import numpy as np 
from tensorflow import keras


st.set_page_config(page_title="Medical Report Generator",page_icon="🎭")

hide_st_style = """
            <style>
            # MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            # header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# def get_img_as_base64(file):
#     with open(file, "rb") as f:
#         data = f.read()
#     return base64.b64encode(data).decode()
# img = get_img_as_base64(r"D:\Downloads\chat-bot-messages-smart-chatbot-assistant-conversation-online-customer-support-robot-talking-to-machine-bots-message-answering-134553809.jpg")

# page_bg_img = f"""
# <style>
# .stApp {{
# background-image: url('data:image/jpg;base64,{img}');
# background-size: cover;
# }} 
# </style>
# """
           
# st.markdown(page_bg_img, unsafe_allow_html=True)



server_url = "https://09c3-34-173-168-26.ngrok-free.app"

df = pd.read_csv(r"csv_files\Training.csv")
# df.drop("Unnamed: 133",axis=1,inplace=True)

#--------------------------------------------------------- medical_database_table ---------------------------------------------#

conn = sqlite3.connect('data.db',check_same_thread=False)
c = conn.cursor()

def create_table():
    	c.execute('CREATE TABLE IF NOT EXISTS medical_database_table(today_date DATE,today_time TEXT ,User_messages TEXT, Bot_messages TEXT)')
create_table()
    

def add_data(today_date,today_time,User_messages,Bot_messages):
	c.execute('INSERT INTO medical_database_table(today_date,today_time,User_messages,Bot_messages) VALUES (?,?,?,?)',(today_date,today_time,User_messages,Bot_messages))
	conn.commit()
 
create_table()

def view_all_data():
    c.execute('SELECT * FROM medical_database_table')
    data = c.fetchall()
    return data

def get_task(task):
    c.execute('SELECT * FROM medical_database_table WHERE test="{}"'.format(task))
    data = c.fetchall()
    return data

def delete_data(task):
    c.execute('DELETE FROM medical_database_table WHERE test="{}"'.format(task))
    conn.commit()
    
def ask(question):
    global server_url
    
    query = {'question': question}
    response = requests.get(server_url, params=query)
    if response.status_code == 200:
        # Handle exception
        try:
            # Get response as text
            response = response.text
            # Print response
            return response
        except:
            return "Error"
    else:
        return "Error"
    
 

def get_doc(location, disease):
    container = {
        "name": [],
        "degree": [],
        "speciality": [],
        "clinic": [],
        "rating": [],
        "experience": [],
        "price": [],
        "available": [],
        "time": []
    }
    
    url = "https://www.lybrate.com/" + location + "/treatment-for-" + disease
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    search_results = soup.find_all(
        "div", {"class": "ly-doctor"})
    

    for result in search_results:
        doc_rating, doc_experience, doc_price, doc_available, doc_time = "null", "null", "null", "null", "null"
        doc_name = result.find("h2", {"class": "ly-doctor__name"})
        doc_degree = doc_speciality = result.find("div", {"class": "ly-doctor__degree"})
        doc_speciality = result.find_all("div", {"class": "lybText--dark lybText--ellipsis"})[0]
        doc_clinic = result.find_all("div", {"class": "lybText--dark lybText--ellipsis"})[1]
        doc_side = result.find_all("div", {"class": "grid__col-xs-10 grid--direction-row"})
        for i in doc_side:
            if "ratings" in i.text:
                doc_rating = i.find_all("span")[0].text.strip() + " " + i.find_all("span")[1].text.strip()
            elif "experience" in i.text:
                doc_experience = i.find_all("span")[0].text.strip() + " " + i.find_all("span")[1].text.strip()
            elif "at clinic" in i.text:
                doc_price = i.find_all("span")[0].text.strip() + " " + i.find_all("span")[1].text.strip()

        doc_available = result.find("div", {"class": "grid__col-20 grid--direction-row grid--align-center grid--justify-start"})
        if doc_available:
            doc_available = doc_available.text.strip()
        doc_time = result.find("div", {"class": "today-time"})

        container["name"].append(doc_name.text.strip())
        container["degree"].append(doc_degree.text.strip() if doc_degree else "null")
        container["speciality"].append(doc_speciality.text.strip())
        container["clinic"].append(doc_clinic.text.strip())
        container["rating"].append(doc_rating)
        container["experience"].append(doc_experience)
        container["price"].append(doc_price)
        container["available"].append(doc_available)
        container["time"].append(doc_time.text.strip() if doc_time else "null")

    return container

st.title("Artificial Intelligence Electronic Report Generator")

c1_i,c2_i = st.columns(2)

with c1_i: st.subheader(":blue[_ERG Gen_]")
with c2_i: st.subheader(":blue[_Care_ _Bot_]")

clicked = clickable_images(
    [
        "https://media.istockphoto.com/id/1188335495/vector/medical-friendly-android-robot-with-stethoscope-robot-doctor-concept.jpg?s=612x612&w=0&k=20&c=yZFUUGPDsXeySqMZSkp0AN1vMK8_yG01tAdK9CKIWP0=",
        "https://media.istockphoto.com/id/1385658219/vector/healthcare-doctor-chatbot-and-using-ai-technology-concept-vector-flat-people-illustration.jpg?s=612x612&w=0&k=20&c=-ziWDu2E_pZegqL5C3v7ydth9FxBQs7DuSQ-elEN26c="
        
        ],
    titles=[f"Image #{str(i)}" for i in range(5)],
    
    div_style={"display": "flex","flex": "33.33%","padding": "5px"},
    img_style={"margin": "5px", "max-width":"50%","height":"300px","width": "50%"},
)

if clicked == 0:


    #--------------------------------------------------------- medical_database_table ---------------------------------------------#
    st.title("CareBot")


    column_1_1,column_1_2 = st.columns(2)
    column_2_1,column_2_2 = st.columns(2)
    column_3_1,column_3_2 = st.columns(2)
    column_4_1,column_4_2 = st.columns(2)
    column_5_1,column_5_2 = st.columns(2)
    column_6_1,column_6_2 = st.columns(2)
    column_7_1,column_7_2 = st.columns(2)
    column_8_1,column_8_2 = st.columns(2)
    column_9_1,column_9_2 = st.columns(2)
    column_10_1,column_10_2 = st.columns(2)
    column_11_1,column_11_2 = st.columns(2)
    column_12_1,column_12_2 = st.columns(2)
    column_13_1,column_13_2 = st.columns(2)
    column_14_1,column_14_2 = st.columns(2)
    column_15_1,column_15_2 = st.columns(2)
    column_16_1,column_16_2 = st.columns(2)
    column_17_1,column_17_2 = st.columns(2)
    column_18_1,column_18_2 = st.columns(2)
    column_19_1,column_19_2 = st.columns(2)
    column_20_1,column_20_2 = st.columns(2)
    column_21_1,column_21_2 = st.columns(2)
    column_22_1,column_22_2 = st.columns(2)
    column_23_1,column_23_2 = st.columns(2)
    column_24_1,column_24_2 = st.columns(2)
    column_25_1,column_25_2 = st.columns(2)
    column_26_1,column_26_2 = st.columns(2)

    try:
        # ----------------------------------------- columns 1 ---------------------------------------------------------#
        # bot
        with column_1_1:
            q1_c1 = "Welcome to CareBot "
            st.info("Hi, I'm an artificial intelligence based bot. How can I help you?",icon="🤖")
            # st.info("Do you have any problem?",icon="🤖")

        # ----------------------------------------- columns 2 ---------------------------------------------------------#
        # user   
        with column_2_2:
            # problem_result = ""
            
            s1,s2 = st.columns(2)
            with s1:problem = st.button("I have a problem")
            with s2:not_problem = st.button("No, I don't have a problem")
            
            if problem:
                problem_result = "problem"
                st.success("I have a problem")
                # if 'problem_result' not in st.session_state:
                st.session_state['problem_result'] = problem_result
            if not_problem:
                problem_result = "not_problem"
                st.success("No, I don't have a problem")
                
                # if 'problem_result' not in st.session_state:
                st.session_state['problem_result'] = problem_result

        # ----------------------------------------- columns 3 ---------------------------------------------------------#
        # bot  
        problem_result = str(st.session_state.problem_result)

        if problem_result == "problem":
            with column_3_1:
                st.info("Please give me some general information about your health")
                st.info("Upload your photo")
                
            # user columns 4
            with column_4_2:
                your_photo = st.file_uploader("upload your photo")
                if your_photo != None:
                    if 'your_photo' not in st.session_state:
                        st.session_state['your_photo'] = "your_photo_uploaded"
                    
                    
            your_photo_ = str(st.session_state.your_photo)
                
            
            # bot columns 5
            if your_photo_ == "your_photo_uploaded":
                with column_5_1:
                    st.info("What is your name?")

                # user columns 6
                with column_6_2:
                    my_name = st.text_input("Enter your name:")
                    if my_name != "":
                        if 'my_name' not in st.session_state:
                            st.session_state['my_name'] = my_name
                    
                my_name = str(st.session_state.my_name)
                
            # bot columns 7
            if my_name != "":
                with column_7_1:
                    st.info("What is your age and date of birth?")
                
                # user columns 8
                with column_8_2:
                    my_age = st.number_input("enter your age",0,100)
                    my_dob = st.date_input("Date of birth")
                    if my_age != 0:
                        if 'my_age' not in st.session_state:
                                st.session_state['my_age'] = my_age
                    
                my_age = int(st.session_state.my_age)

            
            # bot columns 9
            if int(my_age) != 0:
                with column_9_1:
                    st.info("What is your sex?")
                
                # user columns 10
                with column_10_2:
                    g5,g6 = st.columns(2)
                    
                    with g5: male = st.button("male")
                    with g6: female = st.button("female")
                    
                    if male:
                        result_sex = "male"
                        st.success("male")
                        if 'result_sex' not in st.session_state:
                                st.session_state['result_sex'] = result_sex
                    if female:
                        result_sex = "female"
                        st.success("female")
                        if 'result_sex' not in st.session_state:
                                st.session_state['result_sex'] = result_sex
                        
                        
                my_gender = str(st.session_state.result_sex)
            
            # bot columns 11
            if my_gender != "":
                with column_11_1:
                    st.info("What is your blood group?")

                # user columns 12
                with column_12_2:
                    my_blood_group = st.selectbox("enter your blood group:",["None","A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
                    if my_blood_group != "None":
                        if 'my_blood_group' not in st.session_state:
                                st.session_state['my_blood_group'] = my_blood_group
                                
                my_blood_group = str(st.session_state.my_blood_group)
            
            
            # bot columns 13
            if my_blood_group != "None":
                with column_13_1:
                    st.info("What are the symptoms that you are facing?")
                
                # user columns 14
                with column_14_2:
                    my_symptoms = st.multiselect("select your symptoms",list(df.columns))
                    if len(my_symptoms) != 0:
                        if 'my_symptoms' not in st.session_state:
                                st.session_state['my_symptoms'] = my_symptoms
                            
                my_symptoms_for_condition = st.session_state.my_symptoms
                
                
            # bot columns 15
            if len(my_symptoms_for_condition) != 0:
                with column_15_1:
                    st.info("For how long have you been experiencing these symptoms?")
                    
                # user columns 16
                with column_16_2:
                    symptoms_days = st.text_input("")
                    if symptoms_days != "":
                        if 'symptoms_days' not in st.session_state:
                                st.session_state['symptoms_days'] = symptoms_days
                                
                symptoms_days =  str(st.session_state.symptoms_days)
                
            # bot columns 17
            if symptoms_days != "":
                with column_17_1:
                    st.info("Rate how severe these symptoms are.")
                
                # user columns 18
                with column_18_2:
                    severe_list = []
                    for i in my_symptoms:
                        severe_st =  st.select_slider(i,[1,2,3,4,5])
                        severe_list.append(severe_st)
                
            if symptoms_days != "":
                with column_19_1:
                    st.info("Do you have others problems or symptoms?")
                    

                # user columns 18
                with column_20_2:
                    s3,s4 = st.columns(2)
                    with s3: condi_yes = st.button("YES")
                    with s4: condi_no = st.button("NO")
                    if condi_no:
                        st.success("Generating report...")
                        condi_resu = "no"   
                        # if 'condi_resu' not in st.session_state:
                        st.session_state['condi_resu'] = condi_resu
                        
                    if condi_yes:
                        condi_resu = "yes"
                        st.success("Please add your others symptom in previous symptom container")
                        
                        # if 'condi_resu' not in st.session_state:
                        st.session_state['condi_resu'] = condi_resu
                    
                condi_resu = str(st.session_state.condi_resu)
                
                    

            if condi_resu == "no":
                
                with column_22_2:

                    # generate_report_ = st.button("GENERATE REPORT")
                    generate_report_ = True
                    if generate_report_:
                        
                        # to take all rows relatrd to symptom
                        all_dataframe = pd.DataFrame()
                        for i in my_symptoms:
                            predicted_symptom = df[ (df[i] == 1)]
                            all_dataframe =  pd.concat([all_dataframe,predicted_symptom])
                        
                        # to filter main content in full dataframe
                        find_list = []
                        for i in all_dataframe.to_numpy():
                            i = list(i)
                            find_list.append([i[:len(my_symptoms)], i[-1], i[3:].count(0)])

                        # to sort the data 
                        h = find_list
                        def sor(e):
                            return sum(e[0]),e[2]
                        h.sort(key=sor,reverse=True)
                        
                        # to append diesease from sorted dataframe
                        z = []
                        for i in h:
                            z.append(i[1]) 
                        
                        # to remove reduntanancy
                        res = []
                        for x in z:
                            if x not in res:
                                res.append(x)
                        
                        st.subheader("There are predicted disease in priority order for your symptoms") 
                        disease_in_order_df = pd.DataFrame(data=res,columns=["Disease"])   
                        st.dataframe(disease_in_order_df,width=600) 
                    
                    
                        report_result = "You may have " + res[0]
                        st.success(report_result)
                        if report_result != "":
                            if 'report_result' not in st.session_state:
                                    st.session_state['report_result'] = report_result
                        
            report_result = str(st.session_state.report_result)
            
            if report_result != "":
                        
                with column_23_1:
                    
                    st.info("Do you want us to refer you to near by specialist near by you?")
                    st.info("Enter the name of your district")
                    
                    
                # user columns 18
                with column_24_2:
                    
                    ques1_near_specialist = st.selectbox("*",["None","Ariyalur", "Chengalpattu", "Chennai", "Coimbatore", "Cuddalore", "Dharmapuri", "Dindigul", "Erode", "Kallakurichi", "Kanchipuram", "Kanyakumari", "Karur", "Krishnagiri", "Madurai", "Nagapattinam", "Namakkal", "Nilgiris", "Perambalur", "Pudukkottai", "Ramanathapuram", "Ranipet", "Salem", "Sivaganga", "Tenkasi", "Thanjavur", "Theni", "Thoothukudi", "Tiruchirappalli", "Tirunelveli", "Tirupathur", "Tiruppur", "Tiruvallur", "Tiruvannamalai", "Tiruvarur", "Vellore", "Viluppuram", "Virudhunagar"])
                    if ques1_near_specialist != "None":
        
                       
                        # st.dataframe( pd.DataFrame(get_doc(ques1_near_specialist,disease_in_order_df["Disease"][0])))
    
                        if ques1_near_specialist != "":
                            if 'ques1_near_specialist' not in st.session_state:
                                    st.session_state['ques1_near_specialist'] = ques1_near_specialist
                                    
                        
                ques1_near_specialist_ = str(st.session_state.ques1_near_specialist)
                
                    
            if ques1_near_specialist_ != "None":
                
                with column_25_1:
                    
                    st.info("Do you want to book an appointment at the nearest hospital?")
                
                        
                with column_26_2:
                
                        
                    st.success("Are you in need to book an appointment in a hospital?")
                    s5,s6,s7 = st.columns(3)
                    with s5: book_yes = st.button("YES!!!")
                    with s6: book_no = st.button("NO!!!")
                    with s7: report_button = st.button("Download report")
                    
            
                    
                    if book_no:
                        st.success("okay thank you")
                        final_con = "yes"
                        if 'final_con' not in st.session_state:
                                st.session_state['final_con'] = final_con
                        
                    if book_yes:
                        
                        url = "https://www.lybrate.com/"+ ques1_near_specialist  +"/treatment-for-" + report_result.replace("you may have change of ","").replace("disease","").replace(" ","")
                        webbrowser.open_new(url)
                        
                        final_con = "yes"
                        if 'final_con' not in st.session_state:
                                st.session_state['final_con'] = final_con
                                
                                        
                    if report_button:
                        
                        try:
                            diabatics_list_data_user = st.session_state.diabatics_list_data_user
                            diabatics_list_data_user = [197,110,120,543,30.5,64,53]
                            
                        except:
                            diabatics_list_data_user = [197,110,120,543,30.5,64,53]
                        
                            
                        bg_image = Image.open(r"media\report_template.jpeg")
            
                        my_pho_ima = Image.open(your_photo)
                        my_pho_ima = my_pho_ima.resize((270,270))
                        Image.Image.paste(bg_image,my_pho_ima,(1100,230))
                        
                        title_font = ImageFont.truetype(r"media\Poppins-Medium.otf",35)
                        d1 = ImageDraw.Draw(bg_image)
                        
                        d1.text((450,160),my_name,font = title_font,fill= (0,0,0))
                        d1.text((450,216),str(my_age),font = title_font,fill= (0,0,0))
                        d1.text((450,267),my_gender,font = title_font,fill= (0,0,0))
                        d1.text((830,328),str(my_dob),font = title_font,fill= (0,0,0))
                        d1.text((830,275),ques1_near_specialist_,font = title_font,fill= (0,0,0))
                        d1.text((450,330),my_blood_group,font = title_font,fill= (0,0,0))
                        
                        x1 = 580
                        for i in my_symptoms:
                            d1.text((50,x1),i,font = title_font,fill= (0,0,0))
                            x1 += 60
                        
                        x2 = 580
                        for i in severe_list:
                            d1.text((600,x2)," * "*i+"  " + str(i),font = title_font,fill= (0,0,0))
                            x2 += 60   
                        
                        x3 = 1030
                        for i,j in enumerate(disease_in_order_df["Disease"][:5]):
                            d1.text((50,x3),str(i+1) + ")  " + j ,font = title_font,fill= (0,0,0))
                            x3 += 60 
                        
                        d1.text((500,1150),"you may have change of " +disease_in_order_df["Disease"][0]+ " disease" ,font = title_font,fill= (0,0,0))
                        
                        # BMI
                        d1.text((830,170),str(diabatics_list_data_user[5]),font = title_font,fill= (0,0,0))
                        # Insulin
                        d1.text((200,1630),str(diabatics_list_data_user[4]),font = title_font,fill= (0,0,0))
                        # Glucose
                        d1.text((200,1710),str(diabatics_list_data_user[1]),font = title_font,fill= (0,0,0))
                        # BloodPressure
                        d1.text((200,1780),str(diabatics_list_data_user[2]),font = title_font,fill= (0,0,0))
                        # diabatics_ result
                        d1.text((1170,1620),"No",font = title_font,fill= (0,0,0))
                        
                        bg_image.show()
                        
                        bg_image.save("report.png")
                        
                        with open("report.png", "rb") as file:

                            btn = st.download_button(

                                    label="Download image",

                                    data=file,

                                    file_name="report.png",

                                    mime="image/png"

                                )
                            
                            if btn:
                                st.balloons()
                        
                        
                final_con = str(st.session_state.final_con)
    
    except:
        pass
        
#-----------------------------------------chat bot--------------------------------------------------------------------------#        
        
if clicked == 1:
    
    googletrans_translator = Translator()
    
  
    with open('user_list.pickle', 'rb') as handle:
        user_list = pickle.load(handle)

    with open('bot_list.pickle', 'rb') as handle:
            bot_list = pickle.load(handle)

    # load all pickle files for mdoel 
    data = pickle.load(open(r"model_files\bot files\all_data_medical.pickle",'rb'))

    model = keras.models.load_model(r'model_files\bot files\chatbot_model_new.h5')

    with open(r'model_files\bot files\tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)
        
    with open(r'model_files\bot files\label_encoder.pickle', 'rb') as enc:
        lbl_encoder = pickle.load(enc)


    language = {'afrikaans': 'af', 'albanian': 'sq', 'amharic': 'am', 'arabic': 'ar', 'armenian': 'hy', 'azerbaijani': 'az', 'basque': 'eu', 'belarusian': 'be', 'bengali': 'bn', 'bosnian': 'bs', 'bulgarian': 'bg', 'catalan': 'ca', 'cebuano': 'ceb', 'chichewa': 'ny', 'chinese (simplified)': 'zh-cn', 'chinese (traditional)': 'zh-tw', 'corsican': 'co', 'croatian': 'hr', 'czech': 'cs', 'danish': 'da', 'dutch': 'nl', 'english': 'en', 'esperanto': 'eo', 'estonian': 'et', 'filipino': 'tl', 'finnish': 'fi', 'french': 'fr', 'frisian': 'fy', 'galician': 'gl', 'georgian': 'ka', 'german': 'de', 'greek': 'el', 'gujarati': 'gu', 'haitian creole': 'ht', 'hausa': 'ha', 'hawaiian': 'haw', 'hebrew': 'he', 'hindi': 'hi', 'hmong': 'hmn', 'hungarian': 'hu', 'icelandic': 'is', 'igbo': 'ig', 'indonesian': 'id', 'irish': 'ga', 'italian': 'it', 'japanese': 'ja', 'javanese': 'jw', 'kannada': 'kn', 'kazakh': 'kk', 'khmer': 'km', 'korean': 'ko', 'kurdish (kurmanji)': 'ku', 'kyrgyz': 'ky', 'lao': 'lo', 'latin': 'la', 'latvian': 'lv', 'lithuanian': 'lt', 'luxembourgish': 'lb', 'macedonian': 'mk', 'malagasy': 'mg', 'malay': 'ms', 'malayalam': 'ml', 'maltese': 'mt', 'maori': 'mi', 'marathi': 'mr', 'mongolian': 'mn', 'myanmar (burmese)': 'my', 'nepali': 'ne', 'norwegian': 'no', 'odia': 'or', 'pashto': 'ps', 'persian': 'fa', 'polish': 'pl', 'portuguese': 'pt', 'punjabi': 'pa', 'romanian': 'ro', 'russian': 'ru', 'samoan': 'sm', 'scots gaelic': 'gd', 'serbian': 'sr', 'sesotho': 'st', 'shona': 'sn', 'sindhi': 'sd', 'sinhala': 'si', 'slovak': 'sk', 'slovenian': 'sl', 'somali': 'so', 'spanish': 'es', 'sundanese': 'su', 'swahili': 'sw', 'swedish': 'sv', 'tajik': 'tg', 'tamil': 'ta', 'telugu': 'te', 'thai': 'th', 'turkish': 'tr', 'ukrainian': 'uk', 'urdu': 'ur', 'uyghur': 'ug', 'uzbek': 'uz', 'vietnamese': 'vi', 'welsh': 'cy', 'xhosa': 'xh', 'yiddish': 'yi', 'yoruba': 'yo', 'zulu': 'zu'}
    # source_lan = st.selectbox("Select the source language",list(language.keys()))
    destination_lan  = st.selectbox("Select the language",list(language.keys()),index=21)

    

    input_ques_columns1,input_ques_columns2 = st.columns(2)
    with input_ques_columns1:
        user_input_initial =  st.text_input("Query :")
        user_input = googletrans_translator.translate(user_input_initial,src = language[destination_lan], dest= "en")
        user_input = user_input.text
        
        image_upload_for_bot = st.file_uploader("image")
    with input_ques_columns2:
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("") 
        submit_button_bot = st.button("Submit")

        if image_upload_for_bot is not None:
            model_segment = YOLO(r"train13\weights\best.pt") 
        
            image = Image.open(image_upload_for_bot).save("pimple_result_image.png")

            results = model_segment.predict("pimple_result_image.png",conf=0.20)
            
            st.image(results[0].plot())


    if submit_button_bot == True:
        
        user_list.append(user_input_initial)
        
        chatbot_results = ask(user_input)
        
        # result = model.predict(keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([user_input]),truncating='post', maxlen=20))
        # tag = lbl_encoder.inverse_transform([np.argmax(result)])
        # for i in data['intents']:
        #     if i['tag'] == tag:
        #         output_data =  random.choice(list(i['responses']))

        bot_list.append(chatbot_results.split("Answer:")[1])
                
        add_data(today_date=datetime.datetime.today().date(),today_time= str(datetime.datetime.today().time()),User_messages=user_input,Bot_messages=chatbot_results.split("Answer:")[1])   
        
            
                
    with open('user_list.pickle', 'wb') as handle:
        pickle.dump(user_list, handle, protocol=pickle.HIGHEST_PROTOCOL)

    with open('bot_list.pickle', 'wb') as handle:
        pickle.dump(bot_list, handle, protocol=pickle.HIGHEST_PROTOCOL)  

    pygame.mixer.init()
    for i,j in enumerate(zip(user_list,bot_list)):
        col1, col2 = st.columns(2)
        col11, col22 = st.columns(2)
        
        with col1:
            
            selected_col1 = st.info(j[0],icon="🧊")
        with col22:
            googletrans_result = googletrans_translator.translate( j[1],src= "en", dest= language[destination_lan])
            
            selected_col2 = st.success(googletrans_result.text ,icon="🤖")
            
            c1,c2 = st.columns(2)
            
            with c1:
                say = st.button("Say"+str(i)+"🔊",use_container_width=True)
            with c2:
                pass
                # translate_button = st.button("Translate"+str(i),use_container_width=True)
            # with c3:
            #     extra_information_button = st.button("See extra"+str(i),use_container_width=True)
                
            
            if say:
                
                tts = gTTS(text=j[1], lang=language[destination_lan], slow=False)
                
                tts.save("sound.mp3")
                
                # Load the audio file
                # from playsound import playsound

                playsound("sound.mp3")

 
        
    if len(bot_list) > 1:
        end_button_conservation = st.button("End Conversation")
        if end_button_conservation:
            user_list = []
            bot_list = []
            with open('user_list.pickle', 'wb') as handle:
                pickle.dump(user_list, handle, protocol=pickle.HIGHEST_PROTOCOL)

            with open('bot_list.pickle', 'wb') as handle:
                pickle.dump(bot_list, handle, protocol=pickle.HIGHEST_PROTOCOL) 

    




