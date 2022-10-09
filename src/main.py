import os
from vkbottle import Bot, Keyboard, Text
from vkbottle import BaseStateGroup, KeyboardButtonColor
from vkbottle.bot import Message
from utils.user import User


bot = Bot(os.environ["token"])


class Branch(BaseStateGroup):
    NAME = 0
    GROUP = 1
    UNITS = 2
    REG = 3
    EXTRA = 4
    VOCATION = 5
    CHOOSE = 100


# @bot.on.message(text="Начать")
# async def start(m: Message) -> None:
#     await bot.state_dispenser.set(m.peer_id, Branch.NAME)


@bot.on.message(text="Начать")
async def name(m: Message) -> None:
    await m.answer("Введи полностью свои имя и фамилию. (Пример: Мария Сергеева)")
    await bot.state_dispenser.set(m.peer_id, Branch.GROUP)


@bot.on.message(state=Branch.GROUP)
async def group(m: Message) -> None:
    await m.answer(
        "Приятно познакомиться! Теперь напиши номер своей академической группы.(Пример: ИКБ-02)"
    )
    user = User()
    user.name = m.text
    user.url = f"https://vk.com/id{m.from_id}"
    await bot.state_dispenser.set(m.peer_id, Branch.UNITS, payload=user)


@bot.on.message(state=Branch.UNITS)
async def units(m: Message) -> None:
    user = m.state_peer.payload["payload"]
    user.group = m.text
    await m.answer(
        "В каких подразделениях и отделах Студенческого совета ты состоишь? (Пример: проект 1NFORM, отдел консультации)"
    )
    await bot.state_dispenser.set(m.peer_id, Branch.REG, payload=user)


@bot.on.message(state=Branch.REG)
async def registration(m: Message) -> None:
    user = m.state_peer.payload["payload"]
    user.units = m.text
    keyboard = Keyboard(one_time=True)
    keyboard.add(Text("Отдел разработки")).add(Text("Отдел дизайна"))
    keyboard.row()
    keyboard.add(Text("Отдел системной администрации"))
    keyboard.row()
    keyboard.add(Text("Секретарь"))
    await m.answer("В какой отдел ты хочешь подать заявку?", keyboard=keyboard)
    await bot.state_dispenser.set(m.peer_id, Branch.CHOOSE, payload=user)


@bot.on.message(state=Branch.CHOOSE, text="Отдел разработки")
async def development(m: Message) -> None:
    user = m.state_peer.payload["payload"]
    keyboard = Keyboard(one_time=True)
    keyboard.add(Text("Front-end")).add(Text("Back-end")).add(Text("Mentor"))
    keyboard.row()
    keyboard.add(Text("Project manager"))
    await m.answer("Выбери должность", keyboard=keyboard)
    await bot.state_dispenser.set(m.peer_id, Branch.VOCATION, payload=user)


@bot.on.message(state=Branch.CHOOSE, text="Отдел дизайна")
async def design(m: Message) -> None:
    user = m.state_peer.payload["payload"]
    keyboard = Keyboard(one_time=True)
    keyboard.add(Text("Дизайнер"))
    await m.answer("Выбери должность", keyboard=keyboard)
    await bot.state_dispenser.set(m.peer_id, Branch.VOCATION, payload=user)


@bot.on.message(state=Branch.CHOOSE, text="Отдел системной администрации")
async def devops(m: Message) -> None:
    user = m.state_peer.payload["payload"]
    keyboard = Keyboard(one_time=True)
    keyboard.add(Text("DevOps"))
    await m.answer("Выбери должность", keyboard=keyboard)
    await bot.state_dispenser.set(m.peer_id, Branch.VOCATION, payload=user)


@bot.on.message(state=Branch.VOCATION)
async def secretary(m: Message):
    user = m.state_peer.payload["payload"]
    user.vocation = m.text
    await m.answer(
        "Расскажи о своем опыте работы в этой сфере. Если он отсутствует напиши «далее»."
    )
    await bot.state_dispenser.set(m.peer_id, Branch.EXTRA, payload=user)


@bot.on.message(state=Branch.CHOOSE, text="Секретарь")
async def secretary(m: Message):
    user = m.state_peer.payload["payload"]
    user.vocation = m.text
    await m.answer(
        "Расскажи о своем опыте работы в этой сфере. Если он отсутствует напиши «далее»."
    )
    await bot.state_dispenser.set(m.peer_id, Branch.EXTRA, payload=user)


@bot.on.message(state=Branch.EXTRA)
async def final(m: Message):
    user = m.state_peer.payload["payload"]
    user.extra = m.text
    await m.answer(
        "Спасибо за регистрацию! В ближайшее время с тобой свяжется руководитель Технического департамента и отправит тестовое задание. Если хочешь подать заявку еще в другой отдел, напиши «начать»."
    )
    await user.save()
    await bot.state_dispenser.delete(m.peer_id)


if __name__ == "__main__":
    bot.run_forever()
