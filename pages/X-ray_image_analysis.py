import streamlit as st
import numpy as np
from tensorflow import keras
from keras.utils import img_to_array
import cv2
from ultralytics import YOLO
import shutil,base64
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Image



st.set_page_config(page_title="X-ray image analysis",page_icon="❄️")

hide_st_style = """
            <style>
            # MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.title("To analysis X-ray images")

def report_generation(input_path,output_path):
        
    # Create a PDF file
    pdf_file_name = "XRay_Report.pdf"
    c = canvas.Canvas(pdf_file_name, pagesize=letter)

    # Set the font and font size
    c.setFont("Helvetica", 32)

    page_width, page_height = letter

    border_width = 20  
    c.setStrokeColor(colors.black) 
    c.setLineWidth(2)  
    c.rect(border_width, border_width, page_width - 2 * border_width, page_height - 2 * border_width, fill=0)


    report = "REPORT"
    c.setFont("Helvetica", 32)
    c.setFillColor(colors.black)
    c.drawString(250 , 700 , report)


    # Patient ID
    c.setFont("Helvetica", 18)
    patient_name = "Patient Name: John Doe"
    c.setFillColor(colors.black)
    c.drawString(50, 650 ,  patient_name)


    disease = "Disease: Brain Tumor"
    c.setFillColor(colors.black)
    c.drawString(50, 620 ,  disease)


    doc_name = "Doctor Name: Dr. Balaji"
    c.setFillColor(colors.black)
    c.drawString(50, 75 ,  doc_name )

    c.setFont("Helvetica", 12)
    ph_num = "Ph Num: 9345615762"
    c.setFillColor(colors.black)
    c.drawString( 50, 50 ,  ph_num)


    date = "Date : 5.11.2023"
    c.setFillColor(colors.black)
    c.drawString( 400 , 55 ,  date )

    # # sign = "sign.png"
    # patient_image = Image( sign, width= 35, height= 20)
    # patient_image.drawOn(c, 410 , 75 )


    Desc = "Descricption : "
    c.setFont("Helvetica", 16)
    c.drawString( 50 , 315 , Desc )

    desc1 = "1. Abnormal growth within the brain, often benign."
    c.setFont("Helvetica", 14)
    c.drawString( 100 , 275 ,  desc1 )

    desc2 = "2. Can disrupt normal brain functions and cause symptoms."
    c.drawString( 100 , 255 ,  desc2 )

    desc3 = "3. Diagnosed through imaging and biopsy, if necessary."
    c.drawString( 100 , 235 ,  desc3 )

    desc4 = "4. Treatment options include surgery, radiation, and chemotherapy."
    c.drawString( 100 , 215 ,  desc4 )



    desc5 = "Raw Image"
    c.drawString( 100 , 375 ,  desc5 )

    patient_image_path = input_path
    patient_image = Image(patient_image_path, width= 150 , height= 150 )
    patient_image.drawOn(c, 300 , 400)


    desc6 = "Detected Image"
    c.drawString( 300 , 375 ,  desc6 )

    patient_image_path = output_path 
    patient_image = Image(patient_image_path, width= 150 , height= 150 )
    patient_image.drawOn(c, 100 , 400)

    c.save()
    print(f"PDF report '{pdf_file_name}' created successfully.")


def report_generation_fracture(input_path,output_path):
    # Create a PDF file
    pdf_file_name = "XRay_Report.pdf"
    c = canvas.Canvas(pdf_file_name, pagesize=letter)

    # Set the font and font size
    c.setFont("Helvetica", 32)

    page_width, page_height = letter

    border_width = 20  
    c.setStrokeColor(colors.black) 
    c.setLineWidth(2)  
    c.rect(border_width, border_width, page_width - 2 * border_width, page_height - 2 * border_width, fill=0)


    report = "REPORT"
    c.setFont("Helvetica", 32)
    c.setFillColor(colors.black)
    c.drawString(250 , 700 , report)


    # Patient ID
    c.setFont("Helvetica", 18)
    patient_name = "Patient Name: John Doe"
    c.setFillColor(colors.black)
    c.drawString(50, 650 ,  patient_name)


    disease = "Disease: Bone Fracture"
    c.setFillColor(colors.black)
    c.drawString(50, 620 ,  disease)


    doc_name = "Doctor Name: John Doe"
    c.setFillColor(colors.black)
    c.drawString(50, 75 ,  doc_name )

    c.setFont("Helvetica", 12)
    ph_num = "Ph Num: 9345615762"
    c.setFillColor(colors.black)
    c.drawString( 50, 50 ,  ph_num)


    date = "Date : 5.11.2023"
    c.setFillColor(colors.black)
    c.drawString( 400 , 55 ,  date )

    # # sign = "sign.png"
    # patient_image = Image( sign, width= 35, height= 20)
    # patient_image.drawOn(c, 410 , 75 )


    Desc = "Descricption : "
    c.setFont("Helvetica", 16)
    c.drawString( 50 , 315 , Desc )

    desc1 = "Ratio of bone to total mass."
    c.setFont("Helvetica", 14)
    c.drawString( 100 , 275 ,  desc1 )

    desc2 = "Measures bone density and strength."
    c.drawString( 100 , 255 ,  desc2 )

    desc3 = "Important for overall skeletal health."
    c.drawString( 100 , 235 ,  desc3 )

    desc4 = "Often assessed through DEXA scans"
    c.drawString( 100 , 215 ,  desc4 )


    exc = "Exercise :"
    c.setFont("Helvetica", 16)
    c.drawString( 50 , 180 , exc )

    exc1 = "Hand Grip Strengthener"
    c.setFont("Helvetica", 13)
    c.drawString( 100 , 160 ,  exc1 )

    exc2 = "Finger Tapping"
    c.setFont("Helvetica", 13)
    c.drawString( 400 , 160 ,  exc2 )

    exc3 = "Hand Stretching"
    c.setFont("Helvetica", 13)
    c.drawString( 100 , 130 ,  exc3 )

    exc4 = "Hand-Eye Coordination Drills"
    c.setFont("Helvetica", 13)
    c.drawString( 400, 130 ,  exc4 )




    desc5 = "Raw Image"
    c.drawString( 100 , 375 ,  desc5 )

    patient_image_path = input_path
    patient_image = Image(patient_image_path, width= 150 , height= 150 )
    patient_image.drawOn(c, 300 , 400)


    desc6 = "Detected Image"
    c.drawString( 300 , 375 ,  desc6 )

    patient_image_path = output_path
    patient_image = Image(patient_image_path, width= 150 , height= 150 )
    patient_image.drawOn(c, 100 , 400)



    c.save()
    print(f"PDF report '{pdf_file_name}' created successfully.")



def predict_image(path):
    
    read =  Image.open(path)
    resize_image = read.resize((180,180))
    ima_array = img_to_array(resize_image)
    
    resize_image = ima_array / 255

    return resize_image.reshape(1,180,180,3)
        

select_type_of_disease = st.radio("Enter the disease :",["brain_tumour","Tuberculosis","Bone fracture"],horizontal=True)



if select_type_of_disease == "brain_tumour":
    # title of page
    st.title("Brain tumour")
    
    #  image upload 
    uploaded_show_img = st.image([])
    file_uploader_image  = st.file_uploader("Upload a CT scan")
    

    if file_uploader_image is not None: 
        uploaded_show_img.image(file_uploader_image,use_column_width=True)
    
    labels_result = ["glioma_tumor","meningioma_tumor","no_tumor","pituitary_tumor"]
    button_tumour = st.button("Submit",use_container_width=True)
    
    if button_tumour:

        model_segment = YOLO(r"model_files\yolov8_segment_models\yolov8_segment_brain_tumor_model.pt") 
        
        from PIL import Image
        
        file_uploader_image = Image.open(file_uploader_image).save("x-ray.png")

        results = model_segment.predict("x-ray.png",save=True,conf=0.20)
                    
        st.subheader("disease segmented result")
        st.image(cv2.imread(r"runs\segment\predict\x-ray.png"),use_column_width=True)
        cv2.imwrite(r"result_img_x_ray.png",cv2.imread(r"runs\segment\predict\x-ray.png"))
        
        shutil.rmtree(r"runs")
        
        
        
        if len(results[0].boxes) != 0:
            
            st.subheader("Description:")
            st.success("A brain tumor, known as an intracranial tumor, is an abnormal mass of tissue in which cells grow and multiply uncontrollably, seemingly unchecked by the mechanisms that control normal cells.")  
            st.subheader("Causes:")
            st.success(" Brain tumors can be caused by genetic mutations, exposure to radiation, age, gender, family history, immune system disorders, and environmental factors. Genetic mutations, radiation, age, gender, family history, immune system disorders, and environmental factors can all increase the risk of developing brain tumors.   ")
            st.success("Brain tumors can be caused by genetic mutations, exposure to radiation, age, gender, family history, immune system disorders, and environmental factors. Genetic mutations, radiation, age, gender, family history, immune system disorders, and environmental factors can all increase the risk of developing brain tumors.   ")
            st.subheader("Precaution:")
            st.success("  Regular check-ups with a primary care physician or a neurologist are important to monitor brain health and detect potential issues early. To protect your head, wear helmets and seatbelts when biking, skateboarding, or participating in other sports. Eat a healthy diet rich in fruits, vegetables, and whole grains. Exercise regularly to improve overall health and reduce the risk of many diseases. Limit exposure to radiation to reduce the risk of developing brain tumors.")
            
            st.subheader("Symptoms:")
            st.success("Headaches,Seizures,Nausea and Vomiting,Cognitive Changes,Personality and Mood Changes")

            
        else:
            
            st.info("You are safe")
            
            
    
    report_download_button = st.button("Genarate Report")
    
    if report_download_button:
        
        report_generation(input_path= "result_img_x_ray.png",output_path= "x-ray.png")  
        
        with open("XRay_Report.pdf", "rb") as pdf_file:
            PDFbyte = pdf_file.read()

        st.download_button(label="Download Report",
                            data=PDFbyte,
                            file_name="downloaded_report.pdf",
                            mime='application/octet-stream')
        
        def displayPDF(file):
            # Opening file from file path
            with open(file, "rb") as f:
                base64_pdf = base64.b64encode(f.read()).decode('utf-8')

            # Embedding PDF in HTML
            pdf_display = F'<embed src="data:application/pdf;base64,{base64_pdf}" width="800" height="600" type="application/pdf">'

            # Displaying File
            st.markdown(pdf_display, unsafe_allow_html=True)
        displayPDF("XRay_Report.pdf")
        
if select_type_of_disease == "Tuberculosis":
    # title of page
    st.title("Tuberculosis")
    
    #  image upload 
    uploaded_show_img = st.image([])
    image  = st.file_uploader("Upload a CT scan")
    
    
    if image is not None: 
        uploaded_show_img.image(image,use_column_width=True)
    
    labels_result = ["normal","Tuberculosis"]
    button_tumour = st.button("Submit",use_container_width=True)
    
    if button_tumour:

             
            model_segment = YOLO(r"model_files\yolov8_segment_models\tuberculosis_yolov8.pt") 
            
            st.code(model_segment.names)
            from PIL import Image
            
            image = Image.open(image).save("x-ray.png")
            
            results = model_segment.predict("x-ray.png",save=True,conf=0.30)
            

            st.subheader("disease segmented result")
            st.image(cv2.imread(r"runs\detect\predict\x-ray.png"),use_column_width=True)
            
            shutil.rmtree(r"runs")
            
            for i in results:
                results = i.boxes.cls.tolist()
            
            if 4 not in results:
                
                st.subheader("Description:")
                
                st.success("A bone fracture is a break or crack in a bone, commonly caused by trauma or excessive stress. It results in pain, swelling, and reduced functionality in the affected area. Left untreated, fractures can lead to lasting discomfort and impaired movement")
               
                st.subheader("Exercise:")
                
                st.success("""Hand Grip Strengthener
Finger Tapping
Hand Stretching 
Hand-Eye Coordination Drills""")
                
            else:
                st.info("You are safe")
  


if select_type_of_disease == "Bone fracture":
    # title of page
    st.title("Bone fracture")
    
    #  image upload 
    uploaded_show_img = st.image([])
    file_uploader_image  = st.file_uploader("Upload a CT scan")
    

    if file_uploader_image is not None: 
        uploaded_show_img.image(file_uploader_image,use_column_width=True)
    
    button_tumour = st.button("Submit",use_container_width=True)
    
    if button_tumour:

        model_segment = YOLO(r"train2\weights\best.pt") 
        
        from PIL import Image
        
        file_uploader_image = Image.open(file_uploader_image).save("x-ray.png")

        results = model_segment.predict("x-ray.png",save=True,conf=0.20)
                    
        st.subheader("Bone fracture result")
        st.image(cv2.imread(r"runs\detect\predict\x-ray.png"),use_column_width=True)
        cv2.imwrite(r"result_img_x_ray.png",cv2.imread(r"runs\detect\predict\x-ray.png"))
        
        shutil.rmtree(r"runs")
        
        
        if len(results[0].boxes) != 0:
            
            st.subheader("Description:")
            # st.success("A brain tumor, known as an intracranial tumor, is an abnormal mass of tissue in which cells grow and multiply uncontrollably, seemingly unchecked by the mechanisms that control normal cells.")  
            st.subheader("Causes:")
            # st.success(" Brain tumors can be caused by genetic mutations, exposure to radiation, age, gender, family history, immune system disorders, and environmental factors. Genetic mutations, radiation, age, gender, family history, immune system disorders, and environmental factors can all increase the risk of developing brain tumors.   ")
            # st.success("Brain tumors can be caused by genetic mutations, exposure to radiation, age, gender, family history, immune system disorders, and environmental factors. Genetic mutations, radiation, age, gender, family history, immune system disorders, and environmental factors can all increase the risk of developing brain tumors.   ")
            st.subheader("Precaution:")
            # st.success("  Regular check-ups with a primary care physician or a neurologist are important to monitor brain health and detect potential issues early. To protect your head, wear helmets and seatbelts when biking, skateboarding, or participating in other sports. Eat a healthy diet rich in fruits, vegetables, and whole grains. Exercise regularly to improve overall health and reduce the risk of many diseases. Limit exposure to radiation to reduce the risk of developing brain tumors.")
            
            st.subheader("Symptoms:")
            # st.success("Headaches,Seizures,Nausea and Vomiting,Cognitive Changes,Personality and Mood Changes")

            
        else:
            
            st.info("You are safe")
            
            
    
    report_download_button = st.button("Genarate Report")
    
    if report_download_button:
        
        report_generation_fracture(input_path= "result_img_x_ray.png",output_path= "x-ray.png")
        
        with open("XRay_Report.pdf", "rb") as pdf_file:
            PDFbyte = pdf_file.read()

        st.download_button(label="Download Report",
                            data=PDFbyte,
                            file_name="downloaded_report.pdf",
                            mime='application/octet-stream')
        
        def displayPDF(file):
            # Opening file from file path
            with open(file, "rb") as f:
                base64_pdf = base64.b64encode(f.read()).decode('utf-8')

            # Embedding PDF in HTML
            pdf_display = F'<embed src="data:application/pdf;base64,{base64_pdf}" width="800" height="600" type="application/pdf">'

            # Displaying File
            st.markdown(pdf_display, unsafe_allow_html=True)
        displayPDF("XRay_Report.pdf")  


st.title("Generating X-ray images")

generate_button = st.button("Generate")
# Saves
if generate_button:
    
    from PIL import Image
    
    c1,c2= st.columns(2)
    img = Image.open(file_uploader_image)
    img = img.save("img.jpg")
    # OpenCv Read
    img = cv2.imread("img.jpg")
    im1 = cv2.applyColorMap(img, cv2.COLORMAP_AUTUMN)
    im2 = cv2.applyColorMap(img, cv2.COLORMAP_BONE)
    im3 = cv2.applyColorMap(img, cv2.COLORMAP_JET)
    im4 = cv2.applyColorMap(img, cv2.COLORMAP_WINTER)
    im5 = cv2.applyColorMap(img, cv2.COLORMAP_RAINBOW)
    im6 = cv2.applyColorMap(img, cv2.COLORMAP_OCEAN)
    im7 = cv2.applyColorMap(img, cv2.COLORMAP_SUMMER)
    im8 = cv2.applyColorMap(img, cv2.COLORMAP_SPRING)
    im9 = cv2.applyColorMap(img, cv2.COLORMAP_COOL)
    im10 = cv2.applyColorMap(img, cv2.COLORMAP_HSV)
    im11 = cv2.applyColorMap(img, cv2.COLORMAP_PINK)
    im12 = cv2.applyColorMap(img, cv2.COLORMAP_HOT)

    with c1:
        st.image(im1,use_column_width=True)
        st.image(im2,use_column_width=True)
        st.image(im3,use_column_width=True)
        st.image(im4,use_column_width=True)
        st.image(im5,use_column_width=True)
        st.image(im6,use_column_width=True)
        
    with c2:
        st.image(im7,use_column_width=True)
        st.image(im8,use_column_width=True)
        st.image(im9,use_column_width=True)
        st.image(im10,use_column_width=True)
        st.image(im11,use_column_width=True)
        st.image(im12,use_column_width=True)
        

        
        

        
        
        
        