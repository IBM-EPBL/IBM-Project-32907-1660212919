import numpy as np
import os
import cv2
from keras.models import load_model
from keras.preprocessing import image
from keras.utils import load_img,img_to_array
from flask import Flask,render_template,request
from twilio.rest import Client

app=Flask(__name__)

model = load_model(r"D:\IBM\forestfire.h5")
def send_message():
  account_sid = 'ACfa7f886e40951c77c313595754d8b7f9'
  auth_token = 'fc3642a703e36857bed517368e9c4e2a' 
  client = Client(account_sid, auth_token) 
 
  message = client.messages \
    .create(
    body="Fire detected in the location",
    from_='+19705002427',
    to='+919585030451')
 
  print(message.sid)
   
  print("Fire Detected")
  print("SMS Sent") 
@app.route('/')
def index():
    return render_template('index.html')
text=''
#@app.route('/predict',methods=['GET','POST'])
def upload():
    msg_sent=False
    text=""
    if request.method=='POST':
        f=request.files['image']
        basepath=os.path.dirname(__file__)
        filepath=os.path.join(basepath,'uploads',f.filename)
        f.save(filepath)
        v = 0
        vid= cv2.VideoCapture(filepath)
        if vid.isOpened():
          while True:
            success,frame = vid.read()
            if success:
                 
                 cv2.imwrite('output.jpg',frame)
                 s='D:\IBM\output.jpg'
                 img = image.load_img(s,target_size=(150,150))
                 x = image.img_to_array(img)
                 x = np.expand_dims(x,axis=0)
                 predict = model.predict(x)
                 y = int(predict[0][0])
            
                 if y==0:
                      if not msg_sent:
                           print("fire")
                           text="Fire detected"
                           send_message()
                           msg_sent=True
                 else:
                    print("No Forest Fire Detected")
                    text="no fire"
   
            else:
               break
            cv2.imshow('frame',frame)
            print("frame")
            print(v)
            v+=1
         
            
               
        vid.release()
    cv2.destroyAllWindows()
    return text 
if __name__=='__main__':
    app.run(debug=True)