import streamlit as st
import pickle,keras,random,datetime
import speech_recognition as sr
from gtts import gTTS
import pygame,shutil
from playsound import playsound
from translate import Translator
import pyttsx3,requests
from tensorflow import keras
import numpy as np

hide_st_style = """
            <style>
            # MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            # header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


st.title("Welcome")

 # load all pickle files for mdoel 
data = pickle.load(open(r"model_files\bot files\all_data_medical.pickle",'rb'))

model = keras.models.load_model(r'model_files\bot files\chatbot_model_new.h5')

with open(r'model_files\bot files\tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)
    
with open(r'model_files\bot files\label_encoder.pickle', 'rb') as enc:
    lbl_encoder = pickle.load(enc)
 
 

# Initialize the recognizer
r = sr.Recognizer()
 
# Function to convert text to
# speech
def SpeakText(command):
     
    # Initialize the engine
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()
     
     
def stt():
      
    try:
        
        # use the microphone as source for input.
        with sr.Microphone() as source2:
            
            # wait for a second to let the recognizer
            # adjust the energy threshold based on
            # the surrounding noise level
            r.adjust_for_ambient_noise(source2, duration=0.1)
            
            #listens for the user's input
            audio2 = r.listen(source2,phrase_time_limit=5)
            
            # Using google to recognize audio
            MyText = r.recognize_google(audio2)
            MyText = MyText.lower()
            
            return MyText
     
    except sr.RequestError as e:
        return ("Could not request results; {0}".format(e))
        
    except sr.UnknownValueError:
        return ("Unknown Error Occurred")
 
server_url = "https://b8c9-35-227-179-199.ngrok-free.app" 

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
     
          
# user_list.append(user_input)
                
# bot_list.append(output_data)
        
# add_data(today_date=datetime.datetime.today().date(),today_time= str(datetime.datetime.today().time()),User_messages=user_input,Bot_messages=output_data)   

languages = {
    'None' : 'None',
    'Tamil'  : 'ta',
    'English': 'en',
    'Spanish': 'es',
    'French': 'fr',
    'German': 'de',
    'Italian': 'it',
    'Portuguese': 'pt',
    'Dutch': 'nl',
    'Russian': 'ru',
    'Chinese (Simplified)': 'zh-CN',
    'Japanese': 'ja',
    'Korean': 'ko',
    'Arabic': 'ar',
    'Hindi': 'hi',
    'Bengali': 'bn',
    'Turkish': 'tr'
}


language_tra = st.selectbox("Select the languages",list(languages.keys()))

submit_button = st.button("Submit")

if submit_button:

    pygame.mixer.init()
    c1,c2 = st.columns(2)

    for i in range(10):
        
        col1, col2 = st.columns(2)
        col11, col22 = st.columns(2)
       
    
        SpeakText("Say any thing")
        text = stt()
        
        with col1:st.info(text,icon="🧊")
        
        SpeakText(text)
        
        if text == "stop":
            break
        
        chatbot_results = ask(text)
        chatbot_results = chatbot_results.split("Answer:")[1]
        
        if language_tra != "English":
            
            translator= Translator( from_lang='en', to_lang = languages[language_tra])
            chatbot_results = translator.translate(chatbot_results) 
        
        
        with col22: st.success(chatbot_results)
        tts = gTTS(text=chatbot_results, lang="ta", slow=False)
                    
        tts.save("music_saved\soundvoice" +str(i+1) +".mp3")
        
        playsound("music_saved\soundvoice" +str(i+1) +".mp3")
        
        # pygame.mixer.music.load(r"music_saved\soundvoice" +str(i+1) +".mp3")

        # # Play the audio file
        # pygame.mixer.music.play()

        # # Wait until playback is finished
        # while pygame.mixer.music.get_busy():
        #     continue
 
        
        # result = model.predict(keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([text]),truncating='post', maxlen=20))
        # tag = lbl_encoder.inverse_transform([np.argmax(result)])
        # for i in data['intents']:
        #     if i['tag'] == tag:
        #         output_data =  random.choice(list(i['responses']))
        
        #         with col22: st.success(output_data,icon="🤖")
        #         SpeakText(output_data)  
                
        # SpeakText(chatbot_results)  
                
        
        