import os
from dotenv import load_dotenv
import telebot
from pydub import AudioSegment
import whisper

# Загрузка переменных окружения из .env
load_dotenv()
API_TOKEN = os.getenv("TELEGRAM_TOKEN")  # Читаем токен из .env

# Инициализация бота и Whisper
bot = telebot.TeleBot(API_TOKEN)
model = whisper.load_model("base")

# Создание директории для хранения временных файлов
if not os.path.exists("downloads"):
    os.makedirs("downloads")

# Обработка голосовых сообщений
@bot.message_handler(content_types=["voice"])
def handle_voice(message):
    try:
        # Скачиваем голосовое сообщение
        file_info = bot.get_file(message.voice.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        ogg_path = f"downloads/{message.voice.file_id}.ogg"
        with open(ogg_path, "wb") as f:
            f.write(downloaded_file)

        # Конвертируем OGG в WAV
        wav_path = ogg_path.replace(".ogg", ".wav")
        audio = AudioSegment.from_file(ogg_path, format="ogg")
        audio.export(wav_path, format="wav")

        # Распознаём речь с помощью Whisper
        result = model.transcribe(wav_path, language="ru")
        text = result["text"]

        # Отправляем результат
        bot.reply_to(message, f"Распознанный текст: {text}")

        # Удаляем временные файлы
        os.remove(ogg_path)
        os.remove(wav_path)

    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {e}")

# Запуск бота
bot.polling(none_stop=True)
