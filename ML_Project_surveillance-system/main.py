import cv2
import numpy as np
from keras.models import load_model
import os
import queue
import threading
from datetime import datetime, timedelta
import paho.mqtt.client as mqtt
from funktioner import verify, L1Dist, placering, upload_image_to_s3, upload_video_to_s3, send_sms_notification, sendpost


# Indlæser modeller og opsætter kamera
siamese_model = load_model("D:/test3/siamesemodelv2.h5", custom_objects={'L1Dist': L1Dist})
deploy_prototxt_path = r"D:\test3\deploy.prototxt.txt"
caffemodel_path = r"D:\test3\res10_300x300_ssd_iter_140000.caffemodel"
face_net = cv2.dnn.readNetFromCaffe(deploy_prototxt_path, caffemodel_path)
rtsp_url = "rtsp://admin:770603@192.168.2.199:554/live/profile.0/video"

#Variabler
frame_queue = queue.Queue(maxsize=600)
stop_flag = False
positive_threshold = 16
record_duration = timedelta(seconds=10)
video_writer = None
recording_event = threading.Event()
fps = 15

#Broker IP og port
brokerIP = "192.168.2.185"  
port = 1883  

#Alarm topic til at modtage besked om aktivering eller deaktivering
alarmTopic = "alarm"


#Når den får forbindelse til broker
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(alarmTopic)

#Pause variabel
paused = False

#Aktiverer eller deaktiverer alarmen
def on_message(client, userdata, msg):
    global paused  
    print(f"Modtaget advisering: {msg.topic}: {msg.payload}")
    besked = msg.payload
    if "True" in besked:
        if not paused:
            print("Pauserer scriptet..")
            paused = True
    elif "False" in besked:
        if paused:
            print("Genoptager scriptet...")
            paused = False

#MQTT klient og callbacks
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(brokerIP, port)

#MQTT Threading
mqtt_thread = threading.Thread(target=mqtt_client.loop_forever)
mqtt_thread.start()

#Tager billede
def capture_frames(rtsp_url):
    global stop_flag
    while not stop_flag:
        cap = cv2.VideoCapture(rtsp_url)
        frame_queue.queue.clear()  
        while not frame_queue.full():
            ret, frame = cap.read()
            if ret:
                frame_queue.put(frame)
            else:
                print("Fejl i forbindelse med frames")
        cap.release()
        cv2.waitKey(1)


#Machine learning, tjekker om der er ansigt og sammenligner
def process_frames():
    global stop_flag, video_writer, paused 

    while not stop_flag:
        if not frame_queue.empty() and not recording_event.is_set() and not paused: 
            frame = frame_queue.get()
            blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), (104.0, 177.0, 123.0))
            face_net.setInput(blob)
            detections = face_net.forward()

            for i in range(0, detections.shape[2]):
                confidence = detections[0, 0, i, 2]
                if confidence > 0.5:
                    save_image(frame)
                    results, verified = verify(siamese_model, 0.95, 0.95)
                    num_positive_results = np.sum(np.squeeze(results) > 0.95)

                    if num_positive_results < positive_threshold:
                        sendpost()
                        send_sms_notification()
                        upload_image_to_s3(os.path.join(placering, 'input_image', 'input_image.jpg'))
                        video_filename = start_recording(frame)
                        recording_event.set()
                        threading.Thread(target=record_video, args=(video_filename,)).start()

        cv2.waitKey(10)

#Gemmer billede
def save_image(frame):
    input_image_directory = os.path.join(placering, 'input_image')
    os.makedirs(input_image_directory, exist_ok=True)
    image_path = os.path.join(input_image_directory, 'input_image.jpg')
    cv2.imwrite(image_path, frame)


def start_recording(initial_frame):
    global video_writer
    record_start_time = datetime.now()
    video_filename = os.path.join("D:/test3/video", f"recorded_video_{int(record_start_time.timestamp())}.avi")
    video_writer = cv2.VideoWriter(video_filename, cv2.VideoWriter_fourcc(*"XVID"), fps, (initial_frame.shape[1], initial_frame.shape[0]))
    return video_filename


def record_video(video_filename):
    global video_writer
    total_frames = int(fps * record_duration.total_seconds())
    frame_count = 0

    while frame_count < total_frames:
        if not frame_queue.empty():
            frame = frame_queue.get()
            if video_writer is not None:
                video_writer.write(frame)
                frame_count += 1
        else:
            print("Waiting for frames...")
            cv2.waitKey(500)

    video_writer.release()
    video_writer = None
    upload_video_to_s3(video_filename)
    recording_event.clear()

#Starter threads
capture_thread = threading.Thread(target=capture_frames, args=(rtsp_url,))
process_thread = threading.Thread(target=process_frames)
capture_thread.start()
process_thread.start()

#Main loop til at styre, hvornår man lukker
try:
    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            stop_flag = True
            break
finally:
    stop_flag = True
    capture_thread.join()