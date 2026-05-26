from telegram import Update, ReplyKeyboardMarkup from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
TOKEN = "8755186358:AAHJJ6J2tIJS6cFHqWua_WDFBZOqsAQH2tA"
questions = [ { "text": "Что для вас страшнее в отношениях?", "answers": { "Потерять человека": "abandonment", "Потерять себя": "distance" } },
{
    "text": "Есть ли ощущение, что любовь нужно заслужить?",
    "answers": {
        "Да": "deserve",
        "Нет": "safe"
    }
},

{
    "text": "Часто ли вы выбираете эмоционально недоступных партнёров?",
    "answers": {
        "Да": "cold",
        "Нет": "safe"
    }
},

{
    "text": "Есть ли тревога, когда человек отдаляется?",
    "answers": {
        "Да": "abandonment",
        "Нет": "safe"
    }
},

{
    "text": "Бывает ли, что вы слишком стараетесь ради любви?",
    "answers": {
        "Да": "deserve",
        "Нет": "safe"
    }
},

{
    "text": "Чувствуете ли вы, что отношения часто держатся на вас?",
    "answers": {
        "Да": "strong_woman",
        "Нет": "safe"
    }
},

{
    "text": "Есть ли ощущение, что вы выбираете сложных мужчин, которых хочется спасать?",
    "answers": {
        "Да": "rescuer",
        "Нет": "safe"
    }
},

{
    "text": "Бывает ли сложно расслабиться и довериться в отношениях?",
    "answers": {
        "Да": "control",
        "Нет": "safe"
    }
},

{
    "text": "Есть ли чувство, что вас могут разлюбить, если вы перестанете стараться?",
    "answers": {
        "Да": "deserve",
        "Нет": "safe"
    }
},

{
    "text": "Если отношения становятся спокойными — появляется ли тревога или скука?",
    "answers": {
        "Да": "abandonment",
        "Нет": "safe"
    }
}
]
results = {
"abandonment": """
💔 Похоже, у вас может проявляться сценарий покинутости.
Он часто проявляется через: — тревогу в отношениях; — страх потери; — эмоциональную зависимость; — болезненную реакцию на дистанцию.
Обычно такой сценарий формируется там, где любви, стабильности или эмоциональной близости было недостаточно.
✨ Это не приговор. Такие сценарии можно осознать и постепенно изменить.
Часто глубинные причины становятся видимыми через системные расстановки и работу с семейными сценариями.
Канал Натальи Васильевой: t.me/natalyavassileva """,
"deserve": """
💔 Похоже, внутри есть сценарий: «Любовь нужно заслужить».
Он может проявляться через: — постоянное старание; — страх быть неудобной; — терпение; — желание заслужить тепло и любовь.
Часто это связано с опытом, где любовь зависела от поведения, достижений или ожиданий семьи.
✨ Это можно изменить. Когда человек начинает чувствовать собственную ценность — отношения тоже начинают меняться.
Такие сценарии хорошо раскрываются через системную работу и исследование семейных паттернов.
Канал Натальи Васильевой: t.me/natalyavassileva """,
"cold": """
💔 Похоже, у вас может повторяться сценарий эмоционально недоступных партнёров.
Часто рядом оказываются люди: — холодные; — дистанцированные; — неготовые к близости.
При этом внутри может жить надежда: «если я постараюсь сильнее — меня наконец выберут».
✨ Но любовь не должна быть борьбой за внимание.
Такие сценарии часто уходят корнями в ранний опыт отношений и семейные истории.
Больше о семейных сценариях и расстановках: t.me/natalyavassileva """,
"strong_woman": """
💔 Похоже, у вас проявляется сценарий сильной женщины.
Он может выглядеть как: — постоянный контроль; — ощущение, что всё держится на вас; — невозможность расслабиться; — усталость от ответственности.
Часто за этим стоит опыт, где пришлось слишком рано стать сильной.
✨ Но близость начинается там, где появляется чувство безопасности, а не постоянная необходимость всё удерживать.
Такие сценарии можно постепенно менять через глубокую внутреннюю работу.
Канал Натальи Васильевой: t.me/natalyavassileva """,
"rescuer": """
💔 Похоже, у вас может проявляться сценарий спасательства.
Часто он проявляется в выборе мужчин: — сложных; — эмоционально нестабильных; — нуждающихся в помощи.
Тогда любовь начинает превращаться в спасение, терпение и постоянную эмоциональную работу.
✨ Но отношения не должны строиться только на спасении другого человека.
Такие сценарии нередко повторяются через поколения и становятся заметны в системной работе.
Канал Натальи Васильевой: t.me/natalyavassileva """ }
users = {}
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
welcome_text = """
🌿 Добро пожаловать.
Этот тест поможет увидеть повторяющиеся сценарии в отношениях и возможные семейные паттерны, которые могут влиять на любовь, близость и выбор партнёров.
Вам будет предложено несколько вопросов. Отвечайте честно и интуитивно.
В конце вы получите мягкий психологический разбор вашего сценария отношений 💫 """
await update.message.reply_text(welcome_text)

users[update.effective_user.id] = {
    "step": 0,
    "scores": []
}

await ask_question(update, context)
async def ask_question(update, context):
user = users[update.effective_user.id]
step = user["step"]

if step >= len(questions):
    await show_result(update, context)
    return

q = questions[step]

keyboard = [[a] for a in q["answers"].keys()]
markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

await update.message.reply_text(
    q["text"],
    reply_markup=markup
)
async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
user = users[update.effective_user.id]
step = user["step"]

q = questions[step]

answer = update.message.text

if answer in q["answers"]:
    user["scores"].append(q["answers"][answer])

user["step"] += 1

await ask_question(update, context)
async def show_result(update, context):
user = users[update.effective_user.id]

scores = user["scores"]

if not scores:
    await update.message.reply_text("Не удалось определить сценарий.")
    return

result = max(set(scores), key=scores.count)

text = results.get(result, "Сценарий не найден.")

await update.message.reply_text(text)
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start)) app.add_handler(MessageHandler(filters.TEXT, handle_answer))
print("Бот запущен ")
app.run_polling()
