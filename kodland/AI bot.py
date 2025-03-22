import telebot
import numpy
import keras
import requests
import tensorflow 
from bot_logic import gen_pass, gen_emodji, flip_coin
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext
from imageai.Detection import ObjectDetection


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


@bot.message_handler(commands=['start'])
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


bot.polling()