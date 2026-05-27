import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("TOKEN")

questions = [
    {
        "text": "Когда партнёр не пишет долго, что происходит внутри?",
        "answers": {
            "Тревога, начинаю накручивать себя": "abandonment",
            "Злюсь, но молчу — не хочу быть навязчивой": "deserve",
            "Сама отдаляюсь в ответ": "distance",
            "Просто жду, всё нормально": "happy"
        }
    },
    {
        "text": "Как вы относитесь к конфликтам в отношениях?",
        "answers": {
            "Боюсь, что после конфликта меня бросят": "abandonment",
            "Терплю и сглаживаю, лишь бы не ссориться": "deserve",
            "Закрываюсь и ухожу в себя": "distance",
            "Стараюсь всё проконтролировать и решить": "control"
        }
    },
    {
        "text": "Что вы чувствуете, когда думаете о близости с партнёром?",
        "answers": {
            "Хочу близости, но боюсь потерять его": "abandonment",
            "Нужно стараться, иначе он уйдёт": "deserve",
            "Иногда близость пугает — теряю себя": "distance",
            "Мне сложно расслабиться и довериться": "control"
        }
    },
    {
        "text": "Как вы выбираете партнёров?",
        "answers": {
            "Часто влюбляюсь в тех, кто недоступен или холоден": "unavailable",
            "Тянет к тем, кому нужна помощь или поддержка": "rescue",
            "Выбираю сама, но потом всё тяну на себе": "strong",
            "Отношения складываются сами, без особого выбора": "happy"
        }
    },
    {
        "text": "Что для вас значит \"хорошие отношения\"?",
        "answers": {
            "Когда он рядом и никуда не уходит": "abandonment",
            "Когда я нужна и меня ценят за то, что делаю": "deserve",
            "Когда я остаюсь собой и не растворяюсь": "distance",
            "Когда всё стабильно и предсказуемо": "control"
        }
    },
    {
        "text": "Как в вашей семье проявлялась любовь?",
        "answers": {
            "Через тревогу и гиперопеку": "abandonment",
            "Нужно было заслужить похвалу или внимание": "deserve",
            "Эмоции не принято было показывать": "unavailable",
            "Мама всё держала в руках и вытягивала семью": "strong"
        }
    },
    {
        "text": "Бывает ли ощущение внутренней пустоты?",
        "answers": {
            "Да, и отношения помогают её заполнить": "emptiness",
            "Да, ищу подтверждения что меня любят": "emptiness",
            "Иногда — особенно когда партнёр далеко": "abandonment",
            "Нет, я достаточно самодостаточна": "happy"
        }
    },
    {
        "text": "Как вы себя чувствуете, когда всё в жизни хорошо?",
        "answers": {
            "Жду, когда что-то пойдёт не так": "happy_ban",
            "Кажется, я этого не заслуживаю": "happy_ban",
            "Наслаждаюсь — это нормально": "happy",
            "Стараюсь удержать это ощущение под контролем": "control"
        }
    },
    {
        "text": "Что происходит, когда партнёру плохо?",
        "answers": {
            "Берусь помочь, даже в ущерб себе": "rescue",
            "Чувствую ответственность за его состояние": "rescue",
            "Поддерживаю, но слежу за своими границами": "happy",
            "Беру управление ситуацией на себя": "strong"
        }
    },
    {
        "text": "Как бы вы описали свою роль в отношениях?",
        "answers": {
            "Я держусь и терплю, потому что люблю": "deserve",
            "Я спасаю, поддерживаю, вытягиваю": "rescue",
            "Я контролирую, чтобы всё было хорошо": "strong",
            "Я стараюсь быть в балансе с партнёром": "happy"
        }
    }
]

scenario_info = {
    "abandonment": {
        "name": "Сценарий покинутости",
        "text": "Страх потери и тревога пронизывают ваши отношения. Вы остро реагируете на дистанцию и можете цепляться за людей из страха остаться одной."
    },
    "deserve": {
        "name": "«Любовь нужно заслужить»",
        "text": "Вы привыкли стараться ради любви, терпеть и бояться быть неудобной. Любовь ощущается как награда, которую нужно заработать."
    },
    "distance": {
        "name": "Страх близости / потеря себя",
        "text": "Близость пугает — кажется, что в отношениях можно потерять себя. Вы склонны отдаляться, когда партнёр становится слишком близко."
    },
    "unavailable": {
        "name": "Эмоционально недоступные партнёры",
        "text": "Вас притягивают холодные или закрытые люди. Это знакомая боль — возможно, из детства, где кто-то близкий был эмоционально недоступен."
    },
    "rescue": {
        "name": "Сценарий спасательства",
        "text": "Вы хотите помочь, вытянуть, поддержать — даже в ущерб себе. Любовь через заботу о другом стала вашим способом быть нужной."
    },
    "strong": {
        "name": "Сценарий сильной женщины",
        "text": "Вы берёте на себя всё. Контроль, ответственность, решения — расслабиться и довериться партнёру по-настоящему очень сложно."
    },
    "control": {
        "name": "Контроль вместо доверия",
        "text": "Тревога заставляет всё держать под контролем. Доверие даётся тяжело — легче проверить и перестраховаться, чем отпустить."
    },
    "emptiness": {
        "name": "Сценарий эмоциональной недолюбленности",
        "text": "Внутри живёт ощущение пустоты и жажда подтверждения любви. Отношения становятся способом заполнить то, чего не хватило в детстве."
    },
    "happy_ban": {
        "name": "«Нельзя быть счастливой»",
        "text": "Внутри есть запрет на лёгкость и счастье. Когда всё хорошо — ждёте подвоха. Спокойная любовь кажется недостижимой или незаслуженной."
    },
    "happy": {
        "name": "Ресурсное состояние",
        "text": "В ваших ответах много здоровых паттернов. Но родовые сценарии часто скрыты глубоко — стоит присмотреться внимательнее."
    }
}

CHANNEL = "t.me/natalyavassileva"

users = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users[update.effective_user.id] = {
        "step": 0,
        "scores": []
    }
    text = (
        "🌸 Добро пожаловать.\n\n"
        "Этот тест поможет увидеть родовые сценарии, которые влияют на ваши отношения.\n\n"
        "10 вопросов. Отвечайте честно — первым ощущением, не думая долго.\n\n"
        "Начнём? 👇"
    )
    await update.message.reply_text(text)
    await ask_question(update, context)


async def ask_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = users[update.effective_user.id]
    step = user["step"]

    if step >= len(questions):
        await show_result(update, context)
        return

    q = questions[step]
    keyboard = [[a] for a in q["answers"].keys()]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    num = step + 1
    await update.message.reply_text(
        f"Вопрос {num} из {len(questions)}\n\n{q['text']}",
        reply_markup=reply_markup
    )


async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in users:
        await start(update, context)
        return

    user = users[user_id]
    step = user["step"]
    answer = update.message.text
    q = questions[step]

    if answer in q["answers"]:
        user["scores"].append(q["answers"][answer])
        user["step"] += 1
        await ask_question(update, context)
    else:
        await update.message.reply_text("Пожалуйста, выберите один из вариантов ответа 👇")


async def show_result(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = users[update.effective_user.id]
    scores = user["scores"]

    if not scores:
        await update.message.reply_text("Ошибка результата. Напишите /start чтобы начать заново.")
        return

    # Считаем проценты по каждому сценарию
    total = len(scores)
    counts = {}
    for s in scores:
        counts[s] = counts.get(s, 0) + 1

    sorted_scenarios = sorted(counts.items(), key=lambda x: x[1], reverse=True)

    result_text = "🌸 Ваши родовые сценарии:\n\n"

    for scenario_key, count in sorted_scenarios:
        percent = round(count / total * 100)
        info = scenario_info.get(scenario_key, {})
        name = info.get("name", scenario_key)
        desc = info.get("text", "")
        result_text += f"▪️ {name} — {percent}%\n{desc}\n\n"

    result_text += (
        "——————————————\n"
        "🌿 Эти сценарии передаются из поколения в поколение.\n"
        "Их можно увидеть, понять и изменить.\n\n"
        f"Подробнее о родовых сценариях — в моём канале:\n{CHANNEL}"
    )

    await update.message.reply_text(result_text)


app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_answer))

print("Бот запущен")
app.run_polling()