import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import sqlite3
import pandas as pd
import json,base64
import datetime
from pathlib import Path
from streamlit.source_util import _on_pages_changed, get_pages
# from bokeh.models.widgets import Div
from st_clickable_images import clickable_images
# from tensorflow import keras
import tensorflow



st.set_page_config(page_title="Home_Page",page_icon="💫")

hide_st_style = """
            <style>
            MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()
img = get_img_as_base64(r"images\WhatsApp Image 2023-05-09 at 1.48.04 PM.jpeg")

page_bg_img = f"""
<style>
.stApp {{
background-image: url('data:image/jpg;base64,{img}');
background-size: cover;
}} 
</style>
"""
           
# st.markdown(page_bg_img, unsafe_allow_html=True)



DEFAULT_PAGE = "Home_Page.py"


def get_all_pages():
    default_pages = get_pages(DEFAULT_PAGE)

    pages_path = Path("pages.json")
    
    if pages_path.exists():
        saved_default_pages = json.loads(pages_path.read_text())
    
    else:
        saved_default_pages = default_pages.copy()
        pages_path.write_text(json.dumps(default_pages, indent=4))

    return saved_default_pages


def clear_all_but_first_page():
    current_pages = get_pages(DEFAULT_PAGE)

    if len(current_pages.keys()) == 1:
        return

    get_all_pages()

    # Remove all but the first page
    key, val = list(current_pages.items())[0]
    current_pages.clear()
    current_pages[key] = val

    _on_pages_changed.send()


def show_all_pages():
    current_pages = get_pages(DEFAULT_PAGE)

    saved_pages = get_all_pages()

    missing_keys = set(saved_pages.keys()) - set(current_pages.keys())

    # Replace all the missing pages
    for key in missing_keys:
        current_pages[key] = saved_pages[key]
        
        

    _on_pages_changed.send()

clear_all_but_first_page()


#--------------------------------------------------------- medical_database_table ---------------------------------------------#

conn = sqlite3.connect('data.db',check_same_thread=False)
c = conn.cursor()

def view_all_data():
    c.execute('SELECT * FROM medical_database_table')
    data = c.fetchall()
    return data


def get_task(task):
    c.execute('SELECT * FROM medical_database_table WHERE today_date="{}"'.format(task))
    data = c.fetchall()
    return data

# query_1 = "ALTER TABLE medical_database_table ADD user_name int(20);"
# query_2 = "UPDATE medical_database_table SET user_name = 'admin';"

# # execute the queries
# c.execute(query_1)
# c.execute(query_2)
  
# c.execute("select * from medical_database_table;")
# myresult = c.fetchall()
# for row in myresult:
#     print(row)
# conn.commit()

def create_table_authentication():
    c.execute('CREATE TABLE IF NOT EXISTS authentication_table(user_name TEXT, today_date DATE,today_time TEXT  ,gmail_id TEXT,password TEXT,type_of_customer TEXT)')
create_table_authentication()


def add_data_authentication(user_name,today_date,today_time,gmail_id ,password,type_of_customer ):
	c.execute('INSERT INTO authentication_table(user_name,today_date,today_time,gmail_id ,password ,type_of_customer) VALUES (?,?,?,?,?,?)',(user_name,today_date,today_time,gmail_id ,password,type_of_customer ))
	conn.commit()
 
def get_task_authentication(task):
    c.execute('SELECT * FROM authentication_table WHERE user_name="{}"'.format(task))
    data = c.fetchall()
    return data

def view_all_data_authentication():
    c.execute('SELECT * FROM authentication_table')
    data = c.fetchall()
    return data


try:
    if st.session_state.login == "login successfully" :
        show_all_pages()

except:
    pass

selected2 = option_menu(None, ["Home", "Login", "Signup", 'about'], 
    icons=['house', 'cloud-upload', "list-task", 'gear'], 
    menu_icon="cast", default_index=0, orientation="horizontal")

if selected2 == "Home" :
    
    st.markdown("""Medical accessibility and affordability are no laughing matter,
As we realize your workload keeps you too busy to address it further,
So we've taken it upon ourselves to tackle this issue head-on,
Working diligently to ensure everyone can receive the care they need, won't be undone""")
    # st.markdown("This text is :red[colored red], and this is **:blue[colored]** and bold.")
    # st.markdown(":green[$\sqrt{x^2+y^2}=1$] is a Pythagorean identity. :pencil:")
    # st.markdown("Digital Doctor is the application of digital technologies in healthcare, enabling remote consultations and personalized care. It leverages AI, telemedicine, and IoT to revolutionize healthcare. Patients can access virtual consultations, reducing the need for in-person visits. Remote monitoring using wearable devices helps track health conditions. AI and machine learning assist in diagnostics, while data security and privacy are prioritized. Digital Doctor improves accessibility, efficiency, and patient empowerment in healthcare.")
    
    st.image(Image.open(r"images\WhatsApp Image 2023-05-09 at 1.48.04 PM.jpeg"),use_column_width=True)

    # clicked = clickable_images(
    #     [
    #         "https://images.unsplash.com/photo-1565130838609-c3a86655db61?w=700",
    #         "https://images.unsplash.com/photo-1565372195458-9de0b320ef04?w=700",
    #         "https://images.unsplash.com/photo-1582550945154-66ea8fff25e1?w=700",
    #         "https://images.unsplash.com/photo-1591797442444-039f23ddcc14?w=700",
    #         ],
    #     titles=[f"Image #{str(i)}" for i in range(5)],
        
    #     # div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
    #     img_style={"margin": "5px"},
    # )

    st.subheader("Retrain the model")

    retrain_image = clickable_images(["https://mma.prnewswire.com/media/1780099/image2_Logo.jpg?w=200",],img_style={"margin": "50px",})

  
    
    if retrain_image == 0:
        
        view_db = st.button("View medical data",use_container_width=True)

        if view_db:

            st.subheader("Medical chat database")
            all_data_db = view_all_data()
            clean_df = pd.DataFrame(all_data_db,columns=["today_date","today_time","User_messages","Bot_messages","user_name"])
            st.dataframe(clean_df)


    # if st.button('Go to Dermotologist'):
    #     js = "window.open('http://localhost:8501/Dermotologist')"  # New tab or window
    #     js = "window.location.href = 'http://localhost:8501/Dermotologist'"  # Current tab
    #     html = '<img src onerror="{}">'.format(js)
    #     div = Div(text=html)
    #     st.bokeh_chart(div)
        
    
if selected2 == "Signup":

    username = st.text_input("Enter the Username :")
    gmail = st.text_input("Enter the gmail id :")
    password = st.text_input("Enter the password :", type="password")
    type_of_customer = st.radio("Enter your role :",["Patient","Doctor"],horizontal=True)
    Signup_button = st.button("Signup",use_container_width=True)
    
    
    
    if Signup_button:
        
        if get_task_authentication(username) == []:
            add_data_authentication(user_name=username,today_date=datetime.datetime.today().date(),today_time=str(datetime.datetime.today().time()),gmail_id=gmail,password=password,type_of_customer=type_of_customer)
            st.success("Signup successfully")

        else:
            st.warning("User name is already exists")
        
        
if selected2 == "Login" :
    
    username = st.text_input("Enter the Username :",  key="username")
    password = st.text_input("Enter the password :", type="password")
    login_button = st.button("login",use_container_width=True)
    
    # to see user database
    # st.code(view_all_data_authentication())
  
    if login_button:
        
        if get_task_authentication(username) != []:
            if username == get_task_authentication(username)[0][0] and password == get_task_authentication(username)[0][4] :
                st.success("login successfully")
                st.session_state["login"] = "login successfully"
                st.session_state["user_name"] = username
                
                show_all_pages()
                
            else:
                st.warning("Incorrect username or password")
                st.session_state["login"] = "login not"
                
                clear_all_but_first_page()
                
            
        if get_task_authentication(username) == []:
            st.warning("Incorrect username or password")
            st.session_state["login"] = "login not"
            
            clear_all_but_first_page()


    