import asyncio
import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

TOKEN = os.getenv("TOKEN")
CHANNEL = "https://t.me/natalyavassileva"

bot = Bot(TOKEN)
dp = Dispatcher()

users = {}

scenarios = [
    "Потеря", "Предательство", "Служение", "Борьба", "Изгнание",
    "Поиск дома", "Контроль", "Запрет на счастье", "Дефицит", "Одиночество"
]

stories = {
    "Потеря": """🌿 <b>Ваш сценарий — Потеря</b>

Возможно...

внутри вас живет не страх бедности.

А страх однажды снова потерять всё.

Человек долгие годы создавал свое дело.
Работал. Строил. Мечтал.

Появился дом. Достаток.
Будущее перестало казаться страшным.

Но однажды — всё исчезло.

И тогда внутри появилось решение:
<i>Лучше не иметь слишком много.</i>

Сегодня это проявляется так:
- страшно поднимать цену
- деньги быстро уходят
- сложно позволить себе больше

И где-то глубоко звучит мысль:
<b>«Если у меня будет много — я снова всё потеряю.»</b>""",

    "Предательство": """🤍 <b>Ваш сценарий — Предательство</b>

Возможно...

когда-то доверие закончилось сильной болью.

Два человека любили друг друга.
Строили планы.
Но однажды один сделал выбор.

После этого появилась мысль:
<i>Лучше не открываться полностью.</i>

Сегодня вы можете замечать,
что хотите любви,
но бессознательно держите дистанцию.""",

    "Служение": """🌸 <b>Ваш сценарий — Жизнь ради других</b>

Представьте женщину,
которая много лет жила чужими желаниями.

Она привыкла помогать.
Поддерживать. Спасать.

И постепенно перестала понимать,
чего хочет сама.

Сегодня это проявляется
через чувство вины,
если вы выбираете себя.""",

    "Борьба": """⚔️ <b>Ваш сценарий — Борьба</b>

Каждый день был похож на предыдущий.
Работать. Выживать. Бороться.

Даже когда опасность исчезла,
организм продолжил жить
словно война всё ещё продолжается.

Поэтому отдых становится непривычным,
а спокойствие вызывает тревогу.""",

    "Изгнание": """🕊 <b>Ваш сценарий — Изгнание</b>

Возможно,
когда-то быть собой было небезопасно.

Поэтому сегодня страшно проявляться,
говорить о себе,
быть заметной.

Хотя внутри давно живёт желание
показать миру настоящую себя.""",

    "Поиск дома": """🏡 <b>Ваш сценарий — Поиск своего места</b>

Вы постоянно ищете.
Новую работу. Новое дело. Новый город.

Но ощущение «я ещё не дома» — остаётся.

Иногда поиск происходит не снаружи,
а внутри.""",

    "Контроль": """👑 <b>Ваш сценарий — Контроль</b>

Однажды хаос оказался слишком болезненным.

И тогда родилось решение:
<i>Лучше всё контролировать.</i>

Сегодня сложно доверять.
Расслабляться. Передавать ответственность.

Кажется, что если отпустить — всё разрушится.""",

    "Запрет на счастье": """💔 <b>Ваш сценарий — Запрет на счастье</b>

Возможно,
после счастливого периода
произошло что-то тяжёлое.

Подсознание могло связать эти события.

И теперь появляется ощущение,
что радоваться опасно.

Будто за счастьем обязательно придёт расплата.""",

    "Дефицит": """🌾 <b>Ваш сценарий — Дефицит</b>

Когда-то всего было мало.
Времени. Любви. Денег.

Даже если сегодня жизнь изменилась,
ощущение, что чего-то не хватает,
может оставаться внутри.""",

    "Одиночество": """🤍 <b>Ваш сценарий — Одиночество</b>

Когда-то рядом действительно никого не оказалось.

И тогда родилось решение:
<i>Я справлюсь сама.</i>

Оно помогло выстоять.
Но сегодня может мешать принимать помощь,
доверять и позволять людям быть рядом."""
}


# ---------------------------
# СТАРТ
# ---------------------------

@dp.message(CommandStart())
async def start(message: Message):
    users[message.from_user.id] = {
        "scores": {name: 0 for name in scenarios}
    }

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✨ Начать тест", callback_data="start_test")]
    ])

    await message.answer("""🌙 <b>Добро пожаловать!</b>

<b>Кем вы могли быть в прошлой жизни?</b>

Или, точнее...

<b>Какой опыт до сих пор влияет на вашу жизнь?</b>

Вы замечали, что одни и те же ситуации повторяются снова и снова?

Кто-то никак не может выйти на новый доход.
Кто-то снова выбирает похожих партнёров.
Кто-то боится проявляться.

Этот тест поможет определить сценарий,
который влияет на вашу жизнь сегодня.

❗ Не думайте долго.
Выбирайте первый отклик — он самый честный.""",
        parse_mode="HTML", reply_markup=keyboard)


# ---------------------------
# ВОПРОС 1
# ---------------------------

@dp.callback_query(F.data == "start_test")
async def question1(callback: CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💰 Деньги", callback_data="q1_money")],
        [InlineKeyboardButton(text="❤️ Отношения", callback_data="q1_love")],
        [InlineKeyboardButton(text="😰 Постоянная тревога", callback_data="q1_fear")],
        [InlineKeyboardButton(text="😴 Нет сил", callback_data="q1_energy")],
        [InlineKeyboardButton(text="🎤 Боюсь проявляться", callback_data="q1_voice")],
        [InlineKeyboardButton(text="🧭 Не знаю чего хочу", callback_data="q1_search")],
        [InlineKeyboardButton(text="🤍 Всегда выбираю других", callback_data="q1_service")]
    ])
    await callback.message.edit_text(
        "<b>Вопрос 1 из 10</b>\n\nЧто сейчас беспокоит вас больше всего?",
        parse_mode="HTML", reply_markup=keyboard)


@dp.callback_query(F.data.startswith("q1_"))
async def answer1(callback: CallbackQuery):
    score = users[callback.from_user.id]["scores"]
    d = callback.data
    if d == "q1_money":
        score["Потеря"] += 3; score["Дефицит"] += 2
    elif d == "q1_love":
        score["Предательство"] += 3; score["Одиночество"] += 2
    elif d == "q1_fear":
        score["Борьба"] += 3
    elif d == "q1_energy":
        score["Служение"] += 3
    elif d == "q1_voice":
        score["Изгнание"] += 3
    elif d == "q1_search":
        score["Поиск дома"] += 3
    elif d == "q1_service":
        score["Служение"] += 4
    await callback.message.edit_text("Спасибо ❤️\n\nПереходим дальше...")
    await asyncio.sleep(1)
    await send_question2(callback.message)


# ---------------------------
# ВОПРОС 2
# ---------------------------

async def send_question2(message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Просить помощи", callback_data="q2_help")],
        [InlineKeyboardButton(text="Отказывать людям", callback_data="q2_no")],
        [InlineKeyboardButton(text="Доверять", callback_data="q2_trust")],
        [InlineKeyboardButton(text="Отдыхать", callback_data="q2_rest")],
        [InlineKeyboardButton(text="Говорить о себе", callback_data="q2_show")]
    ])
    await message.answer("<b>Вопрос 2 из 10</b>\n\nЧто для вас сложнее всего?",
        parse_mode="HTML", reply_markup=keyboard)


@dp.callback_query(F.data.startswith("q2_"))
async def answer2(callback: CallbackQuery):
    score = users[callback.from_user.id]["scores"]
    d = callback.data
    if d == "q2_help":
        score["Одиночество"] += 2; score["Служение"] += 2
    elif d == "q2_no":
        score["Служение"] += 3
    elif d == "q2_trust":
        score["Предательство"] += 3
    elif d == "q2_rest":
        score["Борьба"] += 3
    elif d == "q2_show":
        score["Изгнание"] += 3
    await callback.message.edit_text("✨ Хорошо... Идём дальше.")
    await asyncio.sleep(1)
    await send_question3(callback.message)


# ---------------------------
# ВОПРОС 3
# ---------------------------

async def send_question3(message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Мне много не надо", callback_data="q3_little")],
        [InlineKeyboardButton(text="Лучше промолчать", callback_data="q3_silent")],
        [InlineKeyboardButton(text="Я справлюсь сама", callback_data="q3_alone")],
        [InlineKeyboardButton(text="Главное — чтобы всем было хорошо", callback_data="q3_allgood")],
        [InlineKeyboardButton(text="Лучше не рисковать", callback_data="q3_risk")]
    ])
    await message.answer("<b>Вопрос 3 из 10</b>\n\nКакая мысль откликается сильнее всего?",
        parse_mode="HTML", reply_markup=keyboard)


@dp.callback_query(F.data.startswith("q3_"))
async def answer3(callback: CallbackQuery):
    score = users[callback.from_user.id]["scores"]
    d = callback.data
    if d == "q3_little":
        score["Дефицит"] += 2; score["Потеря"] += 2
    elif d == "q3_silent":
        score["Изгнание"] += 3
    elif d == "q3_alone":
        score["Одиночество"] += 3
    elif d == "q3_allgood":
        score["Служение"] += 3
    elif d == "q3_risk":
        score["Контроль"] += 2; score["Потеря"] += 2
    await callback.message.edit_text("🌿 Уже вырисовывается картина...")
    await asyncio.sleep(1)
    await send_question4(callback.message)


# ---------------------------
# ВОПРОС 4
# ---------------------------

async def send_question4(message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Потерять деньги", callback_data="q4_money")],
        [InlineKeyboardButton(text="Быть отвергнутой", callback_data="q4_reject")],
        [InlineKeyboardButton(text="Предательство", callback_data="q4_betray")],
        [InlineKeyboardButton(text="Ошибиться", callback_data="q4_mistake")],
        [InlineKeyboardButton(text="Остаться одной", callback_data="q4_single")]
    ])
    await message.answer("<b>Вопрос 4 из 10</b>\n\nЧто пугает вас сильнее всего?",
        parse_mode="HTML", reply_markup=keyboard)


@dp.callback_query(F.data.startswith("q4_"))
async def answer4(callback: CallbackQuery):
    score = users[callback.from_user.id]["scores"]
    d = callback.data
    if d == "q4_money":
        score["Потеря"] += 3; score["Дефицит"] += 2
    elif d == "q4_reject":
        score["Изгнание"] += 3
    elif d == "q4_betray":
        score["Предательство"] += 3
    elif d == "q4_mistake":
        score["Контроль"] += 3
    elif d == "q4_single":
        score["Одиночество"] += 3
    await callback.message.edit_text("💫 Продолжаем...")
    await asyncio.sleep(1)
    await send_question5(callback.message)


# ---------------------------
# ВОПРОС 5
# ---------------------------

async def send_question5(message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Очень добрая", callback_data="q5_kind")],
        [InlineKeyboardButton(text="Сильная", callback_data="q5_strong")],
        [InlineKeyboardButton(text="Терпеливая", callback_data="q5_patient")],
        [InlineKeyboardButton(text="Ответственная", callback_data="q5_resp")],
        [InlineKeyboardButton(text="Скромная", callback_data="q5_modest")]
    ])
    await message.answer("<b>Вопрос 5 из 10</b>\n\nЧто говорят о вас чаще всего?",
        parse_mode="HTML", reply_markup=keyboard)


@dp.callback_query(F.data.startswith("q5_"))
async def answer5(callback: CallbackQuery):
    score = users[callback.from_user.id]["scores"]
    d = callback.data
    if d == "q5_kind":
        score["Служение"] += 3
    elif d == "q5_strong":
        score["Борьба"] += 2; score["Одиночество"] += 2
    elif d == "q5_patient":
        score["Служение"] += 2; score["Предательство"] += 2
    elif d == "q5_resp":
        score["Контроль"] += 3
    elif d == "q5_modest":
        score["Изгнание"] += 3
    await callback.message.edit_text("🌸 Интересно... Идём дальше.")
    await asyncio.sleep(1)
    await send_question6(callback.message)


# ---------------------------
# ВОПРОС 6
# ---------------------------

async def send_question6(message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Начала блог", callback_data="q6_blog")],
        [InlineKeyboardButton(text="Сменила работу", callback_data="q6_work")],
        [InlineKeyboardButton(text="Открыла бизнес", callback_data="q6_biz")],
        [InlineKeyboardButton(text="Переехала", callback_data="q6_move")],
        [InlineKeyboardButton(text="Начала жить для себя", callback_data="q6_self")]
    ])
    await message.answer(
        "<b>Вопрос 6 из 10</b>\n\nЕсли бы страха не существовало — что бы вы сделали завтра?",
        parse_mode="HTML", reply_markup=keyboard)


@dp.callback_query(F.data.startswith("q6_"))
async def answer6(callback: CallbackQuery):
    score = users[callback.from_user.id]["scores"]
    d = callback.data
    if d == "q6_blog":
        score["Изгнание"] += 3
    elif d == "q6_work":
        score["Борьба"] += 2; score["Поиск дома"] += 2
    elif d == "q6_biz":
        score["Потеря"] += 2; score["Контроль"] += 2
    elif d == "q6_move":
        score["Поиск дома"] += 3
    elif d == "q6_self":
        score["Служение"] += 3
    await callback.message.edit_text("✨ Хорошо...")
    await asyncio.sleep(1)
    await send_question7(callback.message)


# ---------------------------
# ВОПРОС 7
# ---------------------------

async def send_question7(message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Одни и те же отношения", callback_data="q7_rel")],
        [InlineKeyboardButton(text="Денег постоянно не хватает", callback_data="q7_money")],
        [InlineKeyboardButton(text="Не умею отдыхать", callback_data="q7_rest")],
        [InlineKeyboardButton(text="Всё приходится делать самой", callback_data="q7_alone")],
        [InlineKeyboardButton(text="Боюсь проявляться", callback_data="q7_show")]
    ])
    await message.answer(
        "<b>Вопрос 7 из 10</b>\n\nЧто повторяется в вашей жизни чаще всего?",
        parse_mode="HTML", reply_markup=keyboard)


@dp.callback_query(F.data.startswith("q7_"))
async def answer7(callback: CallbackQuery):
    score = users[callback.from_user.id]["scores"]
    d = callback.data
    if d == "q7_rel":
        score["Предательство"] += 2; score["Одиночество"] += 2
    elif d == "q7_money":
        score["Дефицит"] += 3; score["Потеря"] += 2
    elif d == "q7_rest":
        score["Борьба"] += 3
    elif d == "q7_alone":
        score["Одиночество"] += 3
    elif d == "q7_show":
        score["Изгнание"] += 3
    await callback.message.edit_text("🌿 Картина становится яснее...")
    await asyncio.sleep(1)
    await send_question8(callback.message)


# ---------------------------
# ВОПРОС 8
# ---------------------------

async def send_question8(message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Помощь", callback_data="q8_help")],
        [InlineKeyboardButton(text="Деньги", callback_data="q8_money")],
        [InlineKeyboardButton(text="Любовь", callback_data="q8_love")],
        [InlineKeyboardButton(text="Отдых", callback_data="q8_rest")],
        [InlineKeyboardButton(text="Комплименты", callback_data="q8_comp")]
    ])
    await message.answer(
        "<b>Вопрос 8 из 10</b>\n\nЧто вам сложнее всего принять?",
        parse_mode="HTML", reply_markup=keyboard)


@dp.callback_query(F.data.startswith("q8_"))
async def answer8(callback: CallbackQuery):
    score = users[callback.from_user.id]["scores"]
    d = callback.data
    if d == "q8_help":
        score["Одиночество"] += 3
    elif d == "q8_money":
        score["Дефицит"] += 2; score["Потеря"] += 2
    elif d == "q8_love":
        score["Предательство"] += 3
    elif d == "q8_rest":
        score["Борьба"] += 3
    elif d == "q8_comp":
        score["Изгнание"] += 2; score["Запрет на счастье"] += 2
    await callback.message.edit_text("💫 Почти закончили...")
    await asyncio.sleep(1)
    await send_question9(callback.message)


# ---------------------------
# ВОПРОС 9
# ---------------------------

async def send_question9(message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Вина", callback_data="q9_guilt")],
        [InlineKeyboardButton(text="Тревога", callback_data="q9_anxiety")],
        [InlineKeyboardButton(text="Одиночество", callback_data="q9_lone")],
        [InlineKeyboardButton(text="Страх", callback_data="q9_fear")],
        [InlineKeyboardButton(text="Напряжение", callback_data="q9_stress")]
    ])
    await message.answer(
        "<b>Вопрос 9 из 10</b>\n\nКакое чувство сопровождает вас чаще всего?",
        parse_mode="HTML", reply_markup=keyboard)


@dp.callback_query(F.data.startswith("q9_"))
async def answer9(callback: CallbackQuery):
    score = users[callback.from_user.id]["scores"]
    d = callback.data
    if d == "q9_guilt":
        score["Служение"] += 3
    elif d == "q9_anxiety":
        score["Борьба"] += 2; score["Контроль"] += 2
    elif d == "q9_lone":
        score["Одиночество"] += 3
    elif d == "q9_fear":
        score["Потеря"] += 2; score["Предательство"] += 2
    elif d == "q9_stress":
        score["Контроль"] += 3
    await callback.message.edit_text("🌙 Последний вопрос...")
    await asyncio.sleep(1)
    await send_question10(callback.message)


# ---------------------------
# ВОПРОС 10
# ---------------------------

async def send_question10(message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Спокойствия", callback_data="q10_calm")],
        [InlineKeyboardButton(text="Любви", callback_data="q10_love")],
        [InlineKeyboardButton(text="Денег", callback_data="q10_money")],
        [InlineKeyboardButton(text="Свободы", callback_data="q10_free")],
        [InlineKeyboardButton(text="Понять себя", callback_data="q10_self")]
    ])
    await message.answer(
        "<b>Вопрос 10 из 10</b>\n\nЧего вам сейчас хочется больше всего?",
        parse_mode="HTML", reply_markup=keyboard)


@dp.callback_query(F.data.startswith("q10_"))
async def answer10(callback: CallbackQuery):
    score = users[callback.from_user.id]["scores"]
    d = callback.data
    if d == "q10_calm":
        score["Борьба"] += 3
    elif d == "q10_love":
        score["Предательство"] += 2; score["Одиночество"] += 2
    elif d == "q10_money":
        score["Потеря"] += 2; score["Дефицит"] += 2
    elif d == "q10_free":
        score["Изгнание"] += 2; score["Служение"] += 2
    elif d == "q10_self":
        score["Поиск дома"] += 3
    await callback.message.edit_text("🕯 Анализирую ответы...")
    await asyncio.sleep(2)
    await callback.message.answer("📖 Сопоставляю жизненные сценарии...")
    await asyncio.sleep(2)
    await callback.message.answer("✨ Почти готово...")
    await asyncio.sleep(2)
    await show_result(callback.message, callback.from_user.id)


# ---------------------------
# РЕЗУЛЬТАТ
# ---------------------------

async def show_result(message, user_id):
    scores = users[user_id]["scores"]
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    main = sorted_scores[0][0]
    second = sorted_scores[1][0]

    await message.answer(
        f"🌿 <b>Ваш основной сценарий</b>\n\n<b>{main}</b>\n\n"
        f"Также у вас проявляется сценарий\n\n<b>{second}</b>\n\n"
        f"Именно эти две темы сейчас сильнее всего влияют на ваши решения.",
        parse_mode="HTML")

    await asyncio.sleep(1)
    await message.answer(stories[main], parse_mode="HTML")
    await asyncio.sleep(2)

    await message.answer(
        "💭 Не спешите закрывать этот результат.\n\n"
        "На минуту остановитесь.\n\n"
        "Какая фраза задела вас сильнее всего?\n\n"
        "Не обязательно отвечать мне.\nОтветьте себе.\n\n"
        "Именно с этого начинается настоящее исследование себя.")

    await asyncio.sleep(2)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📂 Получить личное досье", url=CHANNEL)]
    ])

    await message.answer(
        "🤍 Это была лишь короткая история.\n\n"
        "Я подготовила для вас подарок.\n\n"
        "📂 <b>Личное досье</b>\n\n"
        "Внутри вы найдёте:\n\n"
        "✨ подробное описание вашего сценария\n"
        "✨ почему он проявляется в отношениях и деньгах\n"
        "✨ вопросы для самостоятельного исследования\n"
        "✨ медитативную практику\n\n"
        "🎁 Всё это бесплатно. 👇",
        parse_mode="HTML", reply_markup=keyboard)

    await asyncio.sleep(2)

    keyboard2 = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌿 Перейти в Telegram", url=CHANNEL)]
    ])

    await message.answer(
        "🕊 Возможно...\n\n"
        "сегодня вы впервые увидели не просто свою проблему.\n\n"
        "А историю, которую бессознательно повторяете уже много лет.\n\n"
        "Хотите узнать, где она началась?\n\n"
        "👇", reply_markup=keyboard2)

    await asyncio.sleep(2)

    await message.answer(
        "Спасибо, что прошли этот тест. 🤍\n\n"
        "Любой сценарий — это не приговор.\n\n"
        "Это история, которую можно понять,\n"
        "а значит — постепенно изменить.\n\n"
        "До встречи в Telegram 🌿")


# ---------------------------
# ЗАПУСК
# ---------------------------

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    print("Бот запущен")
    asyncio.run(main())