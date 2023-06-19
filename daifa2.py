
import os

import logging

import telebot

from dotenv import load_dotenv

import requests

import openai

import re

# Set up logging

logger = telebot.logger

telebot.logger.setLevel(logging.DEBUG)

# Load environment variables from .env file

load_dotenv()

BOT_API_KEY = os.getenv("BOT_API_KEY")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize Telegram bot

bot = telebot.TeleBot(BOT_API_KEY)

# Define bot's details

bot_name = "Daifa Bot or Alfayo Leonard"

bot_location = "Dar es Salaam or Arusha"

bot_contact = "+255755381962"

bot_email = "alfayokingwele@gmail.com"

bot_forex_broker = "I'm Daifa and I do forex. If interested, I can be your mentor. Just contact me. My recommended broker is EXNESS. You can sign up with my referral link: https://one.exness-track.com/a/havsosicn8"

# Set up OpenAI API client

openai.api_key = OPENAI_API_KEY

# Define a dictionary to store user conversations

user_conversations = {}

# Handler function for incoming messages

@bot.message_handler(func=lambda message: True)

def handle_message(message):

    try:

        # Determine the user's question

        user_question = message.text.lower()

        # Check if the user greets the bot

        if user_question == "hi":

            bot.reply_to(message, "Hi there! How can I assist you?")

        # Check if the user asked for the bot's name

        elif re.search(r'\bname\b', user_question):

            bot.reply_to(message, f"My name is {bot_name}.....Aikatai chaliangu!")

        # Check if the user asked about forex

        elif re.search(r'\bforex_broker\b', user_question):

            bot.send_message(message.chat.id, bot_forex_broker)

        # Otherwise, generate a response using OpenAI

        else:

            # Check if the bot has conversed with the user before

            if message.chat.id in user_conversations:

                conversation = user_conversations[message.chat.id]

                prompt = f"Following is a conversation with a user. The user has previously said: {conversation}\n\nUser: {message.text}\nBot:"

            else:

                prompt = f"Following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nUser: Hello, who are you?\nBot am an Daifabot created by Daifa's company. How can I help you today?\nUser: {message.text}\nBot:"

            response = openai.Completion.create(

                model="text-davinci-003",

                prompt=prompt,

                temperature=0.9,

                max_tokens=100,  

                top_p=1,

                frequency_penalty=0,

                presence_penalty=0.6,

                stop=["User:", "Bot:"]

            )

            generated_text = response.choices[0].text.strip()

            bot.reply_to(message, generated_text)

            # Update the user's conversation

            if message.chat.id in user_conversations:

                user_conversations[message.chat.id] += f"\nUser: {message.text}\nBot: {generated_text}"

            else:

                user_conversations[message.chat.id] = f"User: {message.text}\nBot: {generated_text}"

 

    except Exception as e:

        logger.error("Error generating response: %s", e)

        bot.reply_to(message, "Sorry, Sijakuelewaa apoo Chaliangu.")

# Start the bot and keep it running continuously

while True:

    try:

        bot.polling(none_stop=True)

    except Exception as e:

        logger.error("Error polling for new messages:%s", e)

    # Sleep for a few seconds before attempting to reconnect

    time.sleep()

