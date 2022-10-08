import os
from vkbottle import Bot, Keyboard, Text
from vkbottle import BaseStateGroup, DocMessagesUploader
from vkbottle.bot import Message

bot = Bot(os.environ['token'])

class Branch(BaseStateGroup):
    HELLO = 0



@bot.on.message(text='Начать')
async def start(m: Message) -> None:
    keyboard = Keyboard(one_time=True)
    keyboard.add(Text('Регистрация'))
    await m.answer('Привет, это бот для набора', keyboard=keyboard)


@bot.on.message()
async def registration(m: Message) -> None:
    keyboard = Keyboard(one_time=True)
    keyboard.add(Text("Отдел разработки")).add(Text("Отдел дизайна"))
    keyboard.row()
    keyboard.add(Text("Отдел системной администрации"))
    keyboard.row()
    keyboard.add(Text("Секретарь"))
    await m.answer('Выбери отдел', keyboard=keyboard)


@bot.on.message()
async def development(m: Message) -> None:
    keyboard = Keyboard(one_time=True)
    keyboard.add(Text("Front-end")).add(Text("Back-end")).add(Text('Mentor'))
    keyboard.row()
    keyboard.add(Text("Project manager"))
    await m.answer('Выбери должность', keyboard=keyboard)


@bot.on.message()
async def development(m: Message) -> None:
    keyboard = Keyboard(one_time=True)
    keyboard.add(Text("Дизайнер"))
    await m.answer('Выбери должность', keyboard=keyboard)


@bot.on.message()
async def development(m: Message) -> None:
    keyboard = Keyboard(one_time=True)
    keyboard.add(Text("DevOps"))
    await m.answer('Выбери должность', keyboard=keyboard)

if __name__ == "__main__":
    bot.run_forever()
