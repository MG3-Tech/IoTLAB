from gpiozero import Button
from picamera import PiCamera
from datetime import datetime
import yagmail
import os
from flask import Flask, render_template

app = Flask(__name__)

button = Button(17)
camera = PiCamera()

def send_email(image_path):
    receiver = "your_email@example.com"
    body = "Someone is at your door!"
    yag = yagmail.SMTP("your_email@gmail.com", "your_password")
    yag.send(
        to=receiver,
        subject="Doorbell Alert",
        contents=body,
        attachments=image_path,
    )

def take_picture():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    image_path = f"/home/pi/smart_doorbell/static/{timestamp}.jpg"
    camera.capture(image_path)
    send_email(image_path)
    return timestamp

@app.route("/")
def index():
    images = os.listdir("/home/pi/smart_doorbell/static")
    images = [f"static/{image}" for image in images]
    return render_template("index.html", images=images)

if __name__ == "__main__":
    button.when_pressed = take_picture
    app.run(host="0.0.0.0", port=5000)
