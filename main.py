import logging

import configs

from aiogram import executor, types, Bot, Dispatcher
from aiogram.contrib.fsm_storage.mongo import MongoStorage
from aiogram.dispatcher.filters.state import State, StatesGroup


from configs import BOT_TOKEN, MONGO_URL, collusers


class SetReport(StatesGroup):
    report = State()


bot = Bot(BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MongoStorage(uri=MONGO_URL)
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    if await collusers.count_documents({'_id': message.from_user.id}) < 1:
        await collusers.insert_one({"_id": message.from_user.id, "name": message.from_user.full_name})
    await bot.send_message(message.from_user.id, "Salom, <b>{user}</b>! "
                                                 "Ushbu bot @uzwikichat da barcha reklamani o'chirib tashlaydi".
                           format(user=message.from_user.full_name))


@dp.message_handler(content_types=['new_chat_members', 'left_chat_member'])
async def deleting_messages(msg: types.Message):
    if msg.new_chat_members:
        if msg.chat.username == "wikiayollaruz":
            await msg.answer("""Ushbu guruhga xush kelibsiz, <a href="tg://user?id={}">{}</a>\n
Iltimos, WikiStipendiya marafoni haqida <a href="https://youtube.com/playlist?list=PLTiLidqsHkJMY1CSQiUuweKqly5LmYp_L">ushbu havola</a> orqali 
tanishib chiqing.
 
<a href="https://uz.wikipedia.org/wiki/Vikipediya:WikiStipendiya_marafoni/WikiAyollar"> WikiAyollar sahifasi</a>
 
Loyiha doirasida yaratgan maqolalaringizni <a href="https://fountain.toolforge.org/editathons/wikiayollar">ushbu havola</a> orqali kiriting 
            """.
                             format(msg.new_chat_members[0].id, msg.from_user.full_name),
                             parse_mode="HTML")
        else:
            await msg.answer("""Ushbu guruhga xush kelibsiz, <a href="tg://user?id={}">{}</a>\n
Iltimos, WikiStipendiya marafoni HAMDA VIKIPEDIYAGA HISSA QOʻSHISH (tahrirlash, maqola yaratish, fayl yuklash va hokazo) haqida <a href="https://youtube.com/playlist?list=PLTiLidqsHkJMY1CSQiUuweKqly5LmYp_L">ushbu havola</a> orqali 
tanishib chiqing""".
                             format(msg.new_chat_members[0].id, msg.from_user.full_name),
                             parse_mode="HTML")
            await msg.delete()


@dp.errors_handler()
async def some_error(msg, error):
    logging.error("ERROR {} {}".format(error, msg))


@dp.message_handler(content_types=["voice"])
async def ban_sms_content(message: types.Message):
    await message.answer("{} \nIltimos, ovozli xabar yozmang!".format(message.from_user.get_mention()),
                         parse_mode="HTML")
    await message.delete()


@dp.message_handler()
async def some_text(message: types.Message):
    if message.chat.type == 'private':
        await message.answer("Iltimos, qandaydir savolingiz bo'lsa @uzwikichat da yozib qoldirsangiz!")
    else:
        if message.chat.username == "wikiayollaruz":
            return
        if message.forward_from_chat and message.forward_from_chat.username in configs.ignore_links:
            return
        admins_list = [admin.user.id for admin in await bot.get_chat_administrators(chat_id=message.chat.id)]
        if message.from_user.id not in admins_list:
            if message.text.find("wiki") == -1:
                if '@' in message.text:  # Удаление сообщений с тегами (@тег)
                    await message.answer("{} \nIltimos, reklama tarqatmang!".format(message.from_user.get_mention()),
                                         parse_mode="HTML")
                    await message.delete()

                for entity in message.entities:  # Удаление сообщений с ссылками
                    if entity.type in ["url", "text_link"]:
                        await message.answer("{} \nIltimos, reklama tarqatmang!".format(message.from_user.get_mention()),
                                             parse_mode="HTML")
                        await message.delete()


if __name__ == '__main__':
    executor.start_polling(dp,
                           on_startup=configs.on_startup,
                           on_shutdown=configs.on_shutdown, skip_updates=True)
