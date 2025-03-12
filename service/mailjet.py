from mailjet_rest import Client
import os
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv('API_KEY')
secret_key = os.getenv('SECRET_KEY')
mailjet = Client(auth=(api_key, secret_key), version='v3.1')

def send_mail(sender:str ='muhammadibragimov439@gmail.com',sander_name:str=None,to=any,to_name:str=None, subject=any, body=any):
    # Rasmni yuklash
    with open('images/image.png', 'rb') as f:
        data = {
            'File': f,
            'Name': 'image.png'
        }
        image_result = mailjet.files.create(data=data)
        print(image_result.status_code)
        print(image_result.json())

    data = {
      'Messages': [
                    {
                            "From": {
                                    "Email": sender,
                                    "Name": sander_name,
                            },
                            "To": [
                                    {
                                            "Email": to,
                                            "Name": to_name
                                    }
                            ],
                            "Subject": subject,
                            "TextPart": body,
                            "HTMLPart": '<h3>Bu python da qilingan REST-API service:</h3> <br> <img src="https://rest-apis-flask-python-project-cpts.onrender.com/" alt="Rasm">'

                    }
            ]
    }
    result = mailjet.send.create(data=data)
    print(result.status_code)
    print(vars(result))
    return result.status_code