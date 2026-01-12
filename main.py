from telegram.ext import Updater, MessageHandler, Filters

BOT_TOKEN = "7551442437:AAHjvDbpQsSI9wCkxRR_xUFFilaSy4JdVRY"
RESULT_FILE = "result.txt"

def generate_variations(number):
    n = len(number)
    results = []

    for mask in range(1, 1 << (n - 1)):
        out = number[0]
        for i in range(n - 1):
            if mask & (1 << i):
                out += "-"
            out += number[i + 1]
        results.append(out)

    return results

def handle_message(update, context):
    chat_id = update.message.chat_id
    number = update.message.text.strip()

    if not number.isdigit():
        update.message.reply_text("❌ Masukkan angka saja")
        return

    variations = generate_variations(number)

    with open(RESULT_FILE, "w") as f:
        for v in variations:
            f.write(v + "\n")

    context.bot.send_message(
        chat_id=chat_id,
        text=f"✅ Nomor: {number}\n📊 Total variasi: {len(variations)}\n📄 Mengirim file..."
    )

    context.bot.send_document(
        chat_id=chat_id,
        document=open(RESULT_FILE, "rb")
    )

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
