import streamlit as st
import pandas as pd
import webbrowser  
import pyautogui
import time


st.set_page_config(page_title="symptom and disease",page_icon="⭐")
hide_st_style = """
            <style>
            # MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            # header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# --------------------------------------"disease ==> Description"------------------------------------------------------------#
st.subheader("Disease - Description")
df_des1 = pd.read_csv(r"csv_files\symptom_Description.csv")
disease_pre = st.selectbox("Enter the disease :",list(df_des1["Disease"]))
predicted_description = df_des1[ df_des1["Disease"]  == disease_pre ]
st.info(list(predicted_description["Description"])[0])


#---------------------------------------Disease ==> precaution-----------------------------------------------------------------# 
st.subheader("Disease - Precautions")
df_pre = pd.read_csv(r"csv_files\symptom_precaution.csv")
disease_pre = st.selectbox("Enter the disease :",list(df_pre["Disease"]))
predicted_Precaution = df_pre[ df_pre["Disease"]  == disease_pre ]
Precaution_list = []

for i in predicted_Precaution:
    
    Precaution_list.append(list(predicted_Precaution.iloc[0:1,:][i]))
    
dataframe_pre = pd.DataFrame(data= Precaution_list[1:],columns=["Precaution"])
st.dataframe(dataframe_pre)

#---------------------------------------Disease ==> symptom-----------------------------------------------------------------# 
st.subheader("Disease - Symptoms")
df_symptom = pd.read_csv(r"csv_files\disease_symptom.csv")
list_disease = list(set(list(df_symptom["Disease"])))
list_disease.sort()
disease_pre = st.selectbox("Enter the disease :",list_disease)
predicted_symptom = df_symptom[ df_symptom["Disease"]  == disease_pre ]
predicted_symptom.drop_duplicates(inplace=True)
symptom_list = []
for i in predicted_symptom.iloc[:,1:]:
    val = list(predicted_symptom[i])
    for j in val:
        symptom_list.append(j)
symptom_list = list(set(symptom_list))
dataframe_symp = pd.DataFrame(data= symptom_list,columns=["Symptom"])
st.dataframe(dataframe_symp)


st.subheader("To visit the nearest places")
st.warning("Make sure your device location is turn on")
st.subheader("To see nearby places")
select_near_place = st.selectbox("Choose the nearby place :",["None","hospital","government hospital","private hospital","medical"])
location = st.button("Click here")
if location == True:
    # opening an URL in new browser window using the open_new() method  
    url = "https://www.google.com/maps/search/near+by+{}".format(select_near_place)
    webbrowser.open_new(url)
    

st.subheader("Direction to nearby place")
select_near_place_dir = st.selectbox("Choose the nearby places :",["None","hospital","government hospital","private hospital","medical"])
button_dir = st.button("Click here!!!")
if button_dir == True:
    # opening an URL in new browser window using the open_new() method  
    url = "https://www.google.com/maps/search/near+by+{}".format(select_near_place_dir)
    webbrowser.open_new(url)
    if select_near_place_dir == "government hospital":
        time.sleep(4)
        pyautogui.click(446 ,264)
        time.sleep(4)
        pyautogui.click(223 ,377)
        
    if select_near_place_dir == "medical":
        time.sleep(4)
        pyautogui.click(369, 278)
        time.sleep(4)
        pyautogui.click(607, 674)
        time.sleep(4)
        pyautogui.click(223 ,377)
    else:
        time.sleep(4)
        pyautogui.click(446, 318)
        time.sleep(4)
        pyautogui.click(223 ,377)
        
