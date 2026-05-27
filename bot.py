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
"text": "Что для вас страшнее в отношениях?",
"answers": {
"Потерять человека": "abandonment",
"Потерять себя": "distance"
}
},
{
"text": "Есть ли ощущение, что любовь нужно заслужить?",
"answers": {
"Да": "deserve",
"Нет": "safe"
}
}
]

results = {
"abandonment": "💔 У вас проявляется сценарий покинутости.\n\nЭто можно изменить через глубокую внутреннюю работу и расстановки.\n\nКанал Натальи Васильевой:\nt.me/natalyavassileva",

```
"distance": "💔 У вас может быть страх потерять себя в отношениях.\n\nЭто можно изменить.\n\nКанал Натальи Васильевой:\nt.me/natalyavassileva",

"deserve": "💔 У вас может быть сценарий «любовь нужно заслужить».\n\nЭто можно изменить через работу с родовыми сценариями.\n\nКанал Натальи Васильевой:\nt.me/natalyavassileva"
```

}

users = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

```
users[update.effective_user.id] = {
    "step": 0,
    "scores": []
}

text = """
```

🌿 Добро пожаловать.

Этот тест поможет увидеть сценарии в отношениях.

Отвечайте честно и интуитивно.
"""

```
await update.message.reply_text(text)

await ask_question(update, context)
```

async def ask_question(update: Update, context: ContextTypes.DEFAULT_TYPE):

```
user = users[update.effective_user.id]

step = user["step"]

if step >= len(questions):
    await show_result(update, context)
    return

q = questions[step]

keyboard = [[a] for a in q["answers"].keys()]

reply_markup = ReplyKeyboardMarkup(
    keyboard,
    resize_keyboard=True
)

await update.message.reply_text(
    q["text"],
    reply_markup=reply_markup
)
```

async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):

```
user = users[update.effective_user.id]

step = user["step"]

answer = update.message.text

q = questions[step]

if answer in q["answers"]:
    user["scores"].append(q["answers"][answer])

user["step"] += 1

await ask_question(update, context)
```

async def show_result(update: Update, context: ContextTypes.DEFAULT_TYPE):

```
user = users[update.effective_user.id]

scores = user["scores"]

if not scores:
    await update.message.reply_text("Ошибка результата")
    return

result = max(set(scores), key=scores.count)

text = results.get(result, "Результат не найден")

await update.message.reply_text(text)
```

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(
MessageHandler(filters.TEXT & ~filters.COMMAND, handle_answer)
)

print("Бот запущен")

app.run_polling()
