import os
import cv2
import numpy as np
import tensorflow as tf
from keras.models import load_model
import boto3
from botocore.exceptions import NoCredentialsError
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


placering = 'D:/test3/application_data'

# Siamese L1 Distance class
class L1Dist(tf.keras.layers.Layer):
    # init metode til nedarvning
    def __init__(self, **kwargs):
        super().__init__()

    # Udregning af ensartethed
    def call(self, input_embedding, validation_embedding):
        return tf.math.abs(input_embedding - validation_embedding)

# Custom objekt til den siamesiske model
custom_objects = {'L1Dist': L1Dist}
siamese_model = load_model("D:/test3/siamesemodelv2.h5", custom_objects=custom_objects, compile=False)

# Funktion til at håndtere billeder
def preprocess(image_path, target_size=(100, 100)):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, target_size)
    img = img / 255.0  # Pixels bliver normaliseret til [0, 1]
    img = np.expand_dims(img, axis=0)  # Der bliver tilføjet en batch dimension
    return img


def verify(model, detection_threshold, verification_threshold):
    # Laver en liste til resultater
    results = []
    
    verification_base_folder = os.path.join(placering, 'verification_images')
    
    for person_folder in os.listdir(verification_base_folder):
        person_folder_path = os.path.join(verification_base_folder, person_folder)
        
        # Tjekker om det er en mappe
        if os.path.isdir(person_folder_path):
            # Resetter resultater for hver person
            results = []
            
            for image in os.listdir(person_folder_path):
                input_img = preprocess(os.path.join(placering, 'input_image', 'input_image.jpg'))
                validation_img = preprocess(os.path.join(person_folder_path, image))
                
                # Laver forudsigelse
                result = model.predict([input_img, validation_img])
                results.append(result)
    
            # Angiver om der er en positiv forudsigelse
            detection = np.sum(np.array(results) > detection_threshold)

    
            # Verificerings logik
            verification = detection / len(os.listdir(person_folder_path)) 
            verified = verification > verification_threshold
    
            print(f"Number of positive results for {person_folder}: {detection}")
            
    return results, verified


def upload_image_to_s3(image_path):
    s3_bucket = "semesterprojekt3"
    s3_key = "images/input_image.jpg"
    try:
        s3_client = boto3.client('s3')
        s3_client.upload_file(image_path, s3_bucket, s3_key)
        print(f"Billede uploaded til S3: s3://{s3_bucket}/{s3_key}")
    except Exception as e:
        print(f"Error ved upload af billede til S3: {e}")

def upload_video_to_s3(video_path):
    s3_bucket = "semesterprojekt3"
    s3_key = f"vids/{os.path.basename(video_path)}"
    try:
        s3_client = boto3.client('s3')
        s3_client.upload_file(video_path, s3_bucket, s3_key)
        print(f"Video uploaded til S3: s3://{s3_bucket}/{s3_key}")
    except Exception as e:
        print(f"Error ved upload af video til S3: {e}")

def sms_notifikation(telefonnummer, message):
    sns = boto3.client('sns')
    
    try:
        sns.publish(PhoneNumber=telefonnummer, Message=message)
        print("SMS sendt:")
    except Exception as e:
        print(f"Error ved sms afsendelse: {e}")


def generate_presigned_url(bucket_name, object_name, expiration=3600):
    s3 = boto3.client('s3')
    
    try:
        url = s3.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': bucket_name,
                'Key': object_name,
                'ResponseContentDisposition': 'inline',  # Viser billedet i browseren
                'ResponseContentType': 'image/jpeg',  
            },
            ExpiresIn=expiration
        )
        return url
    except NoCredentialsError:
        print("Credentials ikke tilgængelige")
        return None

def send_sms_notification():
    bucket_name = "semesterprojekt3"
    object_name = "images/input_image.jpg"
    telefonnummer = "+4522481330"

    presigned_url = generate_presigned_url(bucket_name, object_name, expiration=86400)
    if presigned_url is not None:
        sms_message = f"Overvågnings billede: {presigned_url}"
    else:
        sms_message = "Der er registreret en aktivitet, men billedet kunne ikke tilgås."

    sms_notifikation(telefonnummer, sms_message)


def sendpost():
    try:
        content = "Der er registreret aktivitet"

        # Forbinder til SMTP server
        mail = smtplib.SMTP('smtp.gmail.com', 587)
        mail.ehlo()

        # Opgraderer forbindelsen til en sikker forbindelse ved brug af TLS (Transport Layer Security)
        context = ssl.create_default_context()

        # Aktiverer server certifikat validering
        context.check_hostname = True
        context.verify_mode = ssl.CERT_REQUIRED
        mail.starttls(context=context)

        # Bruger Gmail email og app password til login
        sender_email = 'kimolesen345@gmail.com'
        app_password = 'gynt wagr tljj fbqn'
        mail.login(sender_email, app_password)

        # Angiver modtager email adresser
        recipient = 'kimolesen345@gmail.com'

        # Opretter et MIMEMultipart objekt
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient
        msg['Subject'] = 'Test Mail'

        # Vedhæfter indhold til emailen
        msg.attach(MIMEText(content, 'plain'))

        # Vedhæfter billedet
        attachment_path = 'D:/test3/application_data/input_image/input_image.jpg'
        attachment = open(attachment_path, 'rb')
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={attachment_path}')
        msg.attach(part)

        # Sender emailen
        mail.sendmail(sender_email, recipient, msg.as_string())

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Lukker forbindelsen
        mail.quit()
