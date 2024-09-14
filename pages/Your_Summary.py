import streamlit as st
# from deepface import DeepFace
from PIL import Image
import sqlite3
import pandas as pd

st.set_page_config(page_title="Your_Summary",page_icon="🥼")

hide_st_style = """
            <style>
            # MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            # header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


# picture = st.camera_input("Take a photo")


# if picture is not None:
#     read_img = Image.open(picture)
#     read_img.save("save_image_to_analyze.jpg")

#     val = DeepFace.analyze("save_image_to_analyze.jpg",actions=['emotion', 'age', 'gender', 'race'])

# button = st.button("SUBMIT")

# if button:
    
#     st.subheader("Emotion analysis")
#     st.success("Your emotion is " + val["dominant_emotion"])
#     st.subheader("Age analysis")
#     st.success("Your age is around " + str(int(val["age"]) - 8) + "-" + str(int(val["age"])-3))
#     st.subheader("gender analysis")
#     st.success("Your gender is " + val["gender"])
    
#     st.code(val)
 
 

conn = sqlite3.connect('data.db',check_same_thread=False)
c = conn.cursor()              


def get_task_diabetes(task):
    c.execute('SELECT * FROM diabatics_db_table WHERE user_name="{}"'.format(task))
    data = c.fetchall()
    return data

def get_task_chatbot(task):
    c.execute('SELECT * FROM medical_database_table WHERE user_name="{}"'.format(task))
    data = c.fetchall()
    return data

# import os
# os.remove(r"E:\vs code projects\Digital Docter\music_saved\soundvoice0.mp3")

st.title("Diabetes Analysis History")

clean_df_diabetes = pd.DataFrame(get_task_diabetes(task= st.session_state.user_name),columns=["test","today_date","today_time","Glucose","Glucoselevel","Result","user_name"])
st.dataframe(clean_df_diabetes,height=200,use_container_width=True)



st.title("Chatbot History")

clean_df_chatbot = pd.DataFrame(get_task_chatbot(task= st.session_state.user_name),columns=["today_date","today_time","User_messages","Bot_messages","user_name"])
st.dataframe(clean_df_chatbot,height=200,use_container_width=True)

