import telebot
import numpy as np
import keras
import requests
import tensorflow as tf
from bot_logic import gen_pass, gen_emodji, flip_coin
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext
from imageai.Detection import ObjectDetection
from PIL import Image, ImageOps


bot = telebot.TeleBot("7564141840:AAG3vZdxtSWWiDsqzQxNPqDkZ6We6Y6_2dg")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я твой Telegram бот. Напиши команду /hello, /bye, /pass, /emodji или /coin  ")

@bot.message_handler(commands=['hello'])
def send_hello(message):
    bot.reply_to(message, "Привет! Как дела?")

@bot.message_handler(commands=['bye'])
def send_bye(message):
    bot.reply_to(message, "Пока! Удачи!")

@bot.message_handler(commands=['pass'])
def send_password(message):
    password = gen_pass(10)  
    bot.reply_to(message, f"Вот твой сгенерированный пароль: {password}")

@bot.message_handler(commands=['emodji'])
def send_emodji(message):
    emodji = gen_emodji()
    bot.reply_to(message, f"Вот эмоджи': {emodji}")

@bot.message_handler(commands=['coin'])
def send_coin(message):
    coin = flip_coin()
    bot.reply_to(message, f"Монетка выпала так: {coin}")

detector = ObjectDetection()
MODEL_PATH = "yolov3.pt"  
detector.setModelTypeAsYOLOv3()
detector.setModelPath(MODEL_PATH)
detector.loadModel()


@bot.message_handler(commands=['start2'])
def send_welcome(message):
    bot.reply_to(message, "Send me an image, and I'll detect objects in it!")


@bot.message_handler(content_types=['photo'])
def detect_objects(message):
    chat_id = message.chat.id

    
    file_info = bot.get_file(message.photo[-1].file_id)
    file_path = file_info.file_path
    image_url = f"https://api.telegram.org/file/bot{'7564141840:AAG3vZdxtSWWiDsqzQxNPqDkZ6We6Y6_2dg'}/{file_path}"

    
    input_path = "input.jpg"
    output_path = "output.jpg"
    
    image_data = requests.get(image_url).content
    with open(input_path, "wb") as f:
        f.write(image_data)

    
    detections = detector.detectObjectsFromImage(input_image=input_path, output_image_path=output_path)

    
    detected_objects = "\n".join([f"{obj['name']} ({obj['percentage_probability']:.2f}%)" for obj in detections])

    
    with open(output_path, "rb") as img_file:
        bot.send_photo(chat_id, img_file, caption=f"Detected Objects:\n{detected_objects}")


@bot.message_handler(func=lambda message: True)
def handle_other_messages(message):
    bot.reply_to(message, "❌ Please send an image.")

#classification
model = tf.keras.models.load_model("keras_model.h5", compile=False)
model.save('new_model.h5')
class_names = open("labels.txt", "r").readlines()

def classify_image(image_path):
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    image = Image.open(image_path).convert("RGB")
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
    data[0] = normalized_image_array
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index].strip()
    confidence_score = prediction[0][index]
    return class_name, confidence_score

@bot.message_handler(commands=['classification'])
def ask_for_image(message):
    bot.reply_to(message, "Please send an image for classification.")

@bot.message_handler(content_types=['photo'])
def classify_received_image(message):
    chat_id = message.chat.id
    file_info = bot.get_file(message.photo[-1].file_id)
    file_path = file_info.file_path
    image_url = f"https://api.telegram.org/file/botYOUR_BOT_TOKEN/{file_path}"
    image_data = requests.get(image_url).content
    input_path = "input_classification.jpg"
    with open(input_path, "wb") as f:
        f.write(image_data)
    class_name, confidence = classify_image(input_path)
    bot.reply_to(message, f"Class: {class_name}\nConfidence Score: {confidence:.2f}")


bot.polling()
