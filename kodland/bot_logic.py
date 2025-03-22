import telebot
import random

def gen_pass(length):
    password = ''
    lowercase = 'abcdefghijklmnopqrstuvwxyz'
    uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    digits = '0123456789'
    special_characters = '!@#$%^&*()-_=+[{]}\\|;:\'",<.>/?'
    all_characters = lowercase + uppercase + digits + special_characters


    for i in range(length):
        password += random.choice(all_characters)
    return password

def gen_emodji():

    emodjis = ('\U0001f600', '\U0001F606', '\U0001F923')
    random_ = random.choice(emodjis)
    
    return random_

def flip_coin():
    coin = ('heads', 'tails')
    flip = random.choice(coin)

    return flip
    



