from aiogram import Bot, Dispatcher, types, executor
from aiogram.types.web_app_info import WebAppInfo


bot = Bot('6300179096:AAFbN2WcT4GvzsVZ7olo5jv9-qDWOyHyGQg')
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    murkup = types.ReplyKeyboardMarkup()
    web_app_info = WebAppInfo(url='http://127.0.0.1:8000/')
    murkup.add(types.KeyboardButton('Открыть веб страницу',
                                    web_app=web_app_info))
    await message.answer('Привет', reply_markup=murkup)


if __name__ == '__main__':
    executor.start_polling(dp)
