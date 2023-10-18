import logging
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, WebAppInfo
import os
import openai
from dotenv import load_dotenv

load_dotenv()

bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
bot = Bot(token=bot_token)
dp = Dispatcher(bot)

openai.api_key = os.getenv('OPENAI_API_KEY')

selected_personality = "Elon Musk"


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    personality_prompt = "Я Илон Маск."
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Начать общение", callback_data="start_chat"))
    keyboard.add(InlineKeyboardButton("Твиттер Илона Маска", url="https://twitter.com/elonmusk?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor"))
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('Открыть веб страницу', web_app=WebAppInfo(url='https://ru.wikipedia.org/wiki/%D0%9C%D0%B0%D1%81%D0%BA,_%D0%98%D0%BB%D0%BE%D0%BD')))
    message_text = (
        "Привет! " + personality_prompt + " Вы можете начать общение, выбрав опцию:"
    )

    await message.answer(message_text, reply_markup=keyboard)
    await message.answer("🤝", reply_markup=markup)

    global selected_personality
    selected_personality = personality_prompt


@dp.message_handler(lambda message: not message.text.startswith('/'))
async def chat(message: types.Message):
    user_input = message.text
    response = chat_with_gpt3(user_input, selected_personality)
    await message.answer(response, parse_mode=ParseMode.MARKDOWN)


@dp.callback_query_handler(lambda query: query.data == "start_chat")
async def start_chat(query: types.CallbackQuery):
    await bot.answer_callback_query(query.id)
    await bot.send_message(query.from_user.id,
                           "Вы можете начать общение, задав вопрос.")


def chat_with_gpt3(prompt, personality=""):
    instruction = f"Chat with a {personality}:\n{prompt}\n"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=instruction,
        max_tokens=300,
        temperature=0.5,
        n=1,
        stop=None
    )
    return response.choices[0].text.strip()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
