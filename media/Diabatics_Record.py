# import streamlit as st
# import pandas as pd
# import pickle
# import datetime
# import numpy as np
# import base64
# import sqlite3


# conn = sqlite3.connect('data.db',check_same_thread=False)
# c = conn.cursor()

# def create_table():
#     c.execute('CREATE TABLE IF NOT EXISTS diabatics_db_table(test TEXT, today_date DATE,today_time TEXT  ,Glucose INT,Glucoselevel TEXT, Result TEXT)')


# def add_data(test,today_date,today_time,Glucose,Glucoselevel,Result,user_name):
# 	c.execute('INSERT INTO diabatics_db_table(test,today_date,today_time,Glucose,Glucoselevel,Result,user_name) VALUES (?,?,?,?,?,?,?)',(test,today_date,today_time,Glucose,Glucoselevel,Result,user_name))
# 	conn.commit()
 
# create_table()


# def view_all_data():
#     c.execute('SELECT * FROM diabatics_db_table')
#     data = c.fetchall()
#     return data

# def get_task(task):
#     c.execute('SELECT * FROM diabatics_db_table WHERE user_name="{}"'.format(task))
#     data = c.fetchall()
#     return data

# def delete_data(task):
#     c.execute('DELETE FROM diabatics_db_table WHERE test="{}"'.format(task))
#     conn.commit()
    
# # delete_data("test1")

# st.set_page_config(page_title="diabetes analysis",page_icon="☑️")

# hide_st_style = """
#             <style>
#             # MainMenu {visibility: hidden;}
#             footer {visibility: hidden;}
#             # header {visibility: hidden;}
#             </style>
#             """
# st.markdown(hide_st_style, unsafe_allow_html=True)


# # def get_img_as_base64(file):
# #     with open(file, "rb") as f:
# #         data = f.read()
# #     return base64.b64encode(data).decode()
# # img = get_img_as_base64(r"D:\Downloads\pexels-nataliya-vaitkevich-6941883.jpg")

# # page_bg_img = f"""
# # <style>
# # .stApp {{
# # background-image: url('data:image/jpg;base64,{img}');
# # background-size: cover;
# # }} 
# # </style>
# # """
           
# # st.markdown(page_bg_img, unsafe_allow_html=True)



# st.subheader("Dashboard")
# all_data_db = get_task(task= st.session_state.user_name )

# clean_df = pd.DataFrame(all_data_db,columns=["test","today_date","today_time","Glucose","Glucoselevel","Result","user_name"])

# st.dataframe(clean_df,height=200,use_container_width=True)

# st.subheader("Graph")
# st.line_chart(pd.DataFrame(data={"Glucose":list(clean_df["Glucose"]),"date":list(clean_df["today_date"])}),y="Glucose",x="date")



# df = pd.read_csv(r"csv_files\diabetes.csv")

# columns_list = list(df.columns)

# list_data_user_g = []

# with st.expander("See current diabetes analysis"):


#     for num,i in enumerate(columns_list[:len(columns_list)-1][1:]):
#         i = str(i)
        
#         num = num +1
#         col1, col2 = st.columns(2)
#         col11, col22 = st.columns(2)
        
#         with col1:
#             # if num == 0:
#             #     st.info("Number of times pregnant",icon="🧊")
#             if num == 1:
#                 st.info(i,icon="🧊")
#             if num == 2:
#                 st.info(i,icon="🧊")
#             if num == 3:
#                 st.info(i,icon="🧊")
#             if num == 4:
#                 st.info(i,icon="🧊")

#             if num == 5:
#                 st.info(i,icon="🧊")
#             if num == 6:
#                 st.info(i,icon="🧊")
#             if num == 7:
#                 st.info(i,icon="🧊")
#         with col22: 
            
#             # st.warning(i)
#             val = st.number_input("enter value of " + str(i),-1,500)
#             if int(val) != -1:
#                 list_data_user_g.append(val)
            
#         if len(list_data_user_g) == num -1:
#             break

#     try:
#         st.session_state['diabetes_list_data_user'] = list_data_user_g
#         st.session_state['diabetes_result'] = list_data_user_g
#     except:
#         pass    

#     st.code(list_data_user_g)

#     check_button =  st.button("To check diabetes")
        
#     if check_button:

#         model = pickle.load(open(r"model_files\diabatics_model.pickle","rb"))
#         list_data_user_g.insert(0,0)
#         result = model.predict([list_data_user_g])
        
        
#         model_result_str = ""
        
#         if int(result) == 1:
#             model_result_str = "Yes"
#             st.subheader("result")
#             st.success("Your diabetes levels may have changed")
            
            
#         if int(result) == 0:
#             model_result_str = "No"
#             st.subheader("result")
#             st.success("Your diabetes levels may not have changed")
#             st.success("You are safe")
        
#         try:
#             st.session_state['diabetes_result'] = model_result_str
#         except:
#             pass   
        
#         Glucoselevel = ""
#         if list_data_user_g[1] <= 99:
#             Glucoselevel = "low"
#         if list_data_user_g[1] in [ i for i in range(100,126)]:
#             Glucoselevel = "Medium"
#         if list_data_user_g[1] > 126 :
#             Glucoselevel = "High"
            
#         all_data_db = view_all_data()
        
#         add_data(test="test_" + str(len(all_data_db)),today_date=datetime.datetime.today().date(),today_time= str(datetime.datetime.today().time()),Glucose=list_data_user_g[1],Glucoselevel=Glucoselevel,Result=model_result_str,user_name=st.session_state.user_name)   
#         all_data_db = get_task(task= st.session_state.user_name )
        
        
#         clean_df = pd.DataFrame(all_data_db,columns=["test","today_date","today_time","Glucose","Glucoselevel","Result","User name"])
#         st.subheader("Updated Table")
#         st.dataframe(clean_df)
        
        
#         st.subheader("Graph")

#         st.line_chart(pd.DataFrame(data= list(clean_df["Glucose"]),columns=["Glucose"]))

        
#         if int(result) == 1:
            
#             st.subheader("Description:")
#             st.subheader("Causes:")
#             st.subheader("Precaution:")
#             st.subheader("Symptoms:")
            



            
            
            
