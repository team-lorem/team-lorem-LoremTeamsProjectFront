import fitz  # PyMuPDF для работы с PDF
import openai#библиотека для работы с API OpenAI.
from openai import OpenAI
import pandas as pd # для работы с xlxs
from docx import Document #позволяет работать с файлами .docx

# Установите ключ API
openai.api_key = "***"

def count_tokens(messages):#Подсчитывает количество токенов (слов) в сообщениях.
    return sum(len(message['content'].split()) for message in messages)


# Функция для извлечения текста из .docx файлов
#Открывает и извлекает текст из файла .docx, возвращая текст с разбивкой по абзацам.
def extract_text_from_docx(file_path):
    doc = Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

# Открывает PDF-файл с помощью PyMuPDF, извлекает текст с каждой страницы и объединяет его в одну строку.
def extract_text_from_pdf(file_path):
    full_text = []
    with fitz.open(file_path) as pdf:
        for page_num in range(pdf.page_count):
            page = pdf.load_page(page_num)
            full_text.append(page.get_text())
    return '\n'.join(full_text)

# Функция для извлечения текста из .xlsx файлов (Excel)
def extract_text_from_xlsx(file_path):
    df = pd.read_excel(file_path)  # Чтение файла в DataFrame
    full_text = df.to_string(index=False)  # Конвертация таблицы в строковый формат без индексов
    return full_text

raedMe = extract_text_from_docx("./regulations/What is Use Case.docx")

# Функция для проверки соответствия требованиям регламентов с помощью GPT-3.5-turbo
async def check_compliance_with_regulations(use_case_text, regulations_texts):
    #Асинхронная функция для проверки текста на соответствие регламентам
    responses = []#Создаётся список для хранения ответов от OpenAI

    #Проходит по каждому регламенту и формирует запросы к OpenAI
    for regulation_text in regulations_texts:
        #Создаётся сообщение, состоящее из
        messages = [
            #Роли системы (эксперт по автомобильным регламентам, на русском языке)
            {"role": "system", "content": f"Вы эксперт по автомобильным регламентам. Вам нужно проверять текст на соответствие требованиям.Описание данных.\nДанные состоят из двух входных артефактов: регламенты сертификации и требования на разработку. Регламенты описаны для каждого объекта регулирования, а требования на каждую систему.\nВ рамках задания на тестировочных данных могут быть следующие объекты:\nEMC, Doors, Steering mechanism, Braking, Safety belt, Seats, Audible warning devices, Speedometer and odometer, Steering equipment, Heating system, AVAS, wipe and wash.\nОбратите внимание, что названия объектов могут перекликаться, например Steering mechanism и Steering equipment. А название системы может быть Steering Wheel, - ее нужно будет проверить по обоим регламентам.\nТакже названия объектов могут как повторять частично или полностью названия регламентов, так и отличаться. Например, регламент может обозначаться Heating system, а система называться HVAC, - это система кондиционирования, которая должна проверена по этому регламенту.\nСтруктура данных.\nРегламенты сертификации\nрегламенты по некоторым системам автомобиля. Регламенты могут быть разных типов, но стоит обратить внимание на структуру документов. Регламенты содержат следующие главы: определения, технические требования, методы тестирования и другие. Наиболее важное значение имеет раздел технических требований, по которому как раз нужно будет производить проверку.{raedMe}. Пиши ответы на русском языке"},
            #Вопроса пользователя о проверке текста на соответствие регламенту
            {"role": "user", "content": f"Проверьте текст на соответствие регламенту:\n\nРегламент:\n{regulation_text},\n\nТекст требования:\n{use_case_text}\n\nСоответствует ли текст требованиям? Обоснуйте ваш ответ.Если текст соответсвует только одному регламенту, укажи его, в остальных укажи параметр, и в чем заключается его не соответствие. Пиши о несоответствии в каких конкретно параметрах не соответствует ни одному параметру , укажи все не соответствия, и пропускаю только то , что параметрам соответствует. Не забудь , тебе нужно четко и понятно объяснить не соответствия."}
        ]
        total_tokens = count_tokens(messages)#Подсчитывается количество токенов в сообщении
        if total_tokens > 10000:  # Убедитесь, что длина не превышает 10,000 токенов
            print("Сообщение слишком длинное, сократите его.")
            continue  # Пропускаем, если длина превышает лимит


        client = OpenAI()
        # Запрос к OpenAI API с использованием стриминга
        stream = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            stream=True,
            max_tokens = 10000
        )

        # Извлекаем ответ по частям
        response_content = ""#Ответ добавляется в список responses
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                response_content += chunk.choices[0].delta.content

        responses.append(response_content.strip())

    return responses
