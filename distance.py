    
    
def calulate_distance_between_camera_and_human_body(frame):
    import cv2
    import mediapipe as mp

    mp_drawing = mp.solutions.drawing_utils
    mp_face = mp.solutions.face_detection.FaceDetection(model_selection=1,min_detection_confidence=0.5)

    width=640
    height=480
    Known_distance = 69.0
    Known_width = 14.0
    a=[]
    def Focal_Length_Finder(Known_distance, real_width, width_in_rf_image):
        focal_length = (width_in_rf_image * Known_distance) / real_width
        return focal_length

    def obj_data(img):
        obj_width=0
        results = mp_face.process(img)
        if not results.detections:
            # print("NO FACE")
            pass
        else: 
            for detection in results.detections:
                bbox = detection.location_data.relative_bounding_box
                x, y, w, h = int(bbox.xmin*width), int(bbox.ymin * height), int(bbox.width*width),int(bbox.height*height)
                # cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
                a.append([x,y])
                obj_width=w
            return obj_width
    def Distance_finder(Focal_Length, Known_width, obj_width_in_frame):
        distance = (Known_width * Focal_Length)/obj_width_in_frame
        return distance

    ref_image = cv2.imread(r"D:\Downloads\ref_ima.png")
    ref_image_obj_width = obj_data(ref_image)
    Focal_length_found = Focal_Length_Finder(Known_distance, Known_width, ref_image_obj_width)


    obj_width_in_frame=obj_data(frame)
    if not obj_width_in_frame:
        final_distance = 0

    else:
        Distance = Distance_finder(Focal_length_found, Known_width, obj_width_in_frame)
        for i in a:
            x1=i[0]
            y1=i[1]
        
        final_distance = round(Distance,2)
        cv2.putText(frame, f"Distance: {round(Distance,2)} CM", (x1, y1),cv2.FONT_HERSHEY_PLAIN, 2, (255,0,0), 2)
    
    return final_distance,frame

    
    