
import cv2
import streamlit as st
import yolov5
from PIL import Image
from ultralytics import YOLO
from keras.utils import img_to_array
import numpy as np


st.set_page_config(page_title="Dermotologist",page_icon="🥼")

hide_st_style = """
            <style>
            # MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# def get_img_as_base64(file):
#     with open(file, "rb") as f:
#         data = f.read()
#     return base64.b64encode(data).decode()
# img = get_img_as_base64(r"D:\app\dermatologist-vector-30803268.jpg")

# page_bg_img = f"""
# <style>
# .stApp {{
# background-image: url('data:image/jpg;base64,{img}');
# background-size: cover;
# }} 
# </style>
# """
           
# st.markdown(page_bg_img, unsafe_allow_html=True)



st.title("Get your Acnes and Scars Detected")
button_pim = st.button("Detect",use_container_width=True)
detected_object_name_list = []


model = model = YOLO(r"train13/weights/best.pt") 
classes_list = model.names

stop = st.button("Terminate",use_container_width=True)



if button_pim:
    
    st.subheader("You may have:")
    image = st.image([])
    stop = st.button("Terminate",use_container_width=True)
    
    detected_classes = st.success([])
    video = cv2.VideoCapture(0)
    
    while True:
        
        ret,frame = video.read()
        results = model(frame)
        
        results =   cv2.cvtColor(results[0].plot(),cv2.COLOR_BGR2RGB)
        
        # get_array = results.xyxy[0]
        # get_array = get_array.tolist()
        
        # if len(get_array) == 0:
        #     pass
        # else:
        #     for i in get_array:
        #         last = classes_list[round(i[-1])]
        #         detected_object_name_list.append(last)
        
        # detected_classes.success(",".join(list(set(detected_object_name_list))))
        
        
        # detected_object_name_list = []
        
        
        image.image(results)
        
    
        
        


# # title of page
# st.title("Predict the skin diseases")

# #  image upload 
# uploaded_show_img = st.image([])
# image  = st.file_uploader("Upload the image")

# def predict_image(path):
    
#     read =  Image.open(path)
    
#     resize_image = read.resize((180,180))
#     ima_array = img_to_array(resize_image)
    
#     resize_image = ima_array / 255
#     return resize_image.reshape(1, 180,180,3)
        

# if image is not None: 
#     uploaded_show_img.image(image)

# labels_result = ['Vasculitis Photos', 'Actinic Keratosis Basal Cell Carcinoma and other Malignant Lesions', 'Acne and Rosacea Photos', 'Exanthems and Drug Eruptions', 'Poison Ivy Photos and other Contact Dermatitis', 'Atopic Dermatitis Photos', 'Melanoma Skin Cancer Nevi and Moles', 'Nail Fungus and other Nail Disease', 'Vascular Tumors', 'Psoriasis pictures Lichen Planus and related diseases', 'Cellulitis Impetigo and other Bacterial Infections', 'Systemic Disease', 'Herpes HPV and other STDs Photos', 'Hair Loss Photos Alopecia and other Hair Diseases', 'Warts Molluscum and other Viral Infections', 'Light Diseases and Disorders of Pigmentation', 'Lupus and other Connective Tissue diseases', 'Seborrheic Keratoses and other Benign Tumors', 'Scabies Lyme Disease and other Infestations and Bites', 'Bullous Disease Photos', 'Tinea Ringworm Candidiasis and other Fungal Infections', 'Urticaria Hives', 'Eczema Photos']
# button_tumour = st.button("Submit",use_container_width=True)


# if button_tumour:

#     model = keras.models.load_model(r'model_files\all models files\all_skin_Disease_model.h5')
#     result = model.predict([predict_image(image)])
#     result = str(labels_result[np.argmax(result)])

#     st.success("Result : " + result ,icon="✅")
    