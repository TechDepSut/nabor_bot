import os
from vkbottle import Bot, Keyboard, Text
from vkbottle import BaseStateGroup
from vkbottle.bot import Message
from utils.user import User


bot = Bot(os.environ["token"])


class Branch(BaseStateGroup):
    NAME = 0
    GROUP = 1
    UNITS = 2
    CHOOSE = 100


#  https://vk.com/id{m.from_id}


@bot.on.message(text="Начать")
async def start(m: Message) -> None:
    keyboard = Keyboard(one_time=True)
    keyboard.add(Text("Регистрация"))
    await m.answer(f"Привет, это бот для набора", keyboard=keyboard)
    await bot.state_dispenser.set(m.peer_id, Branch.NAME)


@bot.on.message(state=Branch.NAME)
async def name(m: Message) -> None:
    await m.answer("Введите свое имя")
    await bot.state_dispenser.set(m.peer_id, Branch.GROUP)


@bot.on.message(state=Branch.GROUP)
async def group(m: Message) -> None:
    await m.answer("Введите группу")
    user = User()
    user.name = m.text
    await bot.state_dispenser.set(m.peer_id, Branch.UNITS, payload=user)


@bot.on.message(state=Branch.UNITS)
async def units(m: Message) -> None:
    await m.answer(m.state_peer.payload['payload'])


@bot.on.message()
async def registration(m: Message) -> None:
    keyboard = Keyboard(one_time=True)
    keyboard.add(Text("Отдел разработки")).add(Text("Отдел дизайна"))
    keyboard.row()
    keyboard.add(Text("Отдел системной администрации"))
    keyboard.row()
    keyboard.add(Text("Секретарь"))
    await m.answer("Выбери отдел", keyboard=keyboard)
    await bot.state_dispenser.set(m.peer_id, Branch.CHOOSE)


@bot.on.message(state=Branch.CHOOSE, text="Отдел разработки")
async def development(m: Message) -> None:
    keyboard = Keyboard(one_time=True)
    keyboard.add(Text("Front-end")).add(Text("Back-end")).add(Text("Mentor"))
    keyboard.row()
    keyboard.add(Text("Project manager"))
    await m.answer("Выбери должность", keyboard=keyboard)


@bot.on.message(state=Branch.CHOOSE, text="Отдел дизайна")
async def design(m: Message) -> None:
    keyboard = Keyboard(one_time=True)
    keyboard.add(Text("Дизайнер"))
    await m.answer("Выбери должность", keyboard=keyboard)


@bot.on.message(state=Branch.CHOOSE, text="Отдел системной администрации")
async def devops(m: Message) -> None:
    keyboard = Keyboard(one_time=True)
    keyboard.add(Text("DevOps"))
    await m.answer("Выбери должность", keyboard=keyboard)


# @bot.on.message(state=Branch.CHOOSE, text='')
# async def


if __name__ == "__main__":
    bot.run_forever()
