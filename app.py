#Ngrok для глобала тунелирование
from pyngrok import ngrok
from flask import Flask, request, jsonify
#Импортирует Flask (фреймворк для создания веб-приложений), request (для получения данных из запроса)
# и jsonify (для формирования JSON-ответа).
from flask_cors import CORS  # Импортируем CORS
import os
#Импортирует модуль для работы с файловой системой
import asyncio
#Импортирует библиотеку для работы с асинхронными задачами.
from utils import extract_text_from_docx, extract_text_from_pdf, check_compliance_with_regulations, extract_text_from_xlsx
#мпортирует функции для извлечения текста из файлов и проверки соответствия требованиям регламентов из модуля utils


app = Flask(__name__)
CORS(app)  # Включаем CORS для всего приложения
#Создаётся экземпляр Flask-приложения, которое обрабатывает запросы. Параметр __name__ указывает имя текущего модуля.
UPLOAD_FOLDER = './uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
#UPLOAD_FOLDER = './uploads': Задаётся папка, куда будут сохраняться загружаемые файлы.
#if not os.path.exists(UPLOAD_FOLDER):: Проверяет, существует ли папка uploads. Если нет, она создаётся.
#os.makedirs(UPLOAD_FOLDER): Создаёт папку uploads, если она не существуе

@app.route('/upload', methods=['POST'])
#@app.route('/upload', methods=['POST']): Определяет маршрут /upload, который будет обрабатывать
# POST-запросы. Этот маршрут будет принимать файлы от пользователя.
async def upload_file():  # Асинхронный обработчик
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
#if 'file' not in request.files:: Проверяет, содержит ли запрос файл. Если файла нет, возвращается ошибка.
#return jsonify({"error": "No file uploaded"}), 400: Возвращает JSON-ответ с сообщением об ошибке 400.
    file = request.files['file']#Извлекает загруженный файл из запроса.
    if file.filename == '':#Проверяет, выбрал ли пользователь файл. Если имя файла пустое, возвращается ошибка.
        return jsonify({"error": "No selected file"}), 400#Возвращает ошибку, если файл не был выбран.

    # Сохраняем загруженный файл
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)#Формирует путь, куда будет сохранён файл (в папку uploads).
    file.save(file_path)# Сохраняет загруженный файл по указанному пути.

    proverka = file_path.split(".")[-1]
    # Извлекаем текст из загруженного файла .docx
    if proverka == "docx":
        use_case_text = extract_text_from_docx(file_path)
    elif proverka == "xlsx":# Извлекаем текст из загруженного файла .xlsx
        use_case_text = extract_text_from_xlsx(file_path)

    # Извлекаем текст из регламентов (в .pdf формате)
    regulation1_text = extract_text_from_pdf('./regulations/AVAS_EN.pdf')  # Пример регламента
    regulation2_text = extract_text_from_pdf('./regulations/Braking_EN.pdf')  # Другой регламент
    regulation3_text = extract_text_from_pdf('./regulations/Wipe_and_wash_ENG.pdf')  # Третий регламент

    # Проверяем соответствие требованиям всех регламентов
    result = await check_compliance_with_regulations(use_case_text, [regulation1_text, regulation2_text, regulation3_text])
    
    return jsonify({"result": result})#Возвращает результат проверки в виде JSON-ответа.


@app.route('/text', methods=['POST'])
async def check_text():  # Асинхронный обработчик
    data = request.get_json()

    if 'text' not in data:
        return jsonify({"error": "No text provided"}), 400

    use_case_text = data['text']

    # Извлекаем текст из регламентов (в .pdf формате)
    regulation1_text = extract_text_from_pdf('./regulations/AVAS_EN.pdf')
    regulation2_text = extract_text_from_pdf('./regulations/Braking_EN.pdf')
    regulation3_text = extract_text_from_pdf('./regulations/Wipe_and_wash_ENG.pdf')

    # Проверяем соответствие требованиям всех регламентов
    result = await check_compliance_with_regulations(use_case_text,
                                                     [regulation1_text, regulation2_text, regulation3_text])

    return jsonify({"result": result})


if __name__ == '__main__':
    port=5000
    public_url = ngrok.connect(port)
    print(f" * ngrok tunnel available at: {public_url}")
    app.run(port=port)
