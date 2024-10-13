import os
from flask import jsonify
from openpyxl import Workbook
from utils import extract_text_from_word, check_compliance

def generate_excel_report(request):
    if 'files' not in request.files:
        return jsonify({"error": "No files uploaded"}), 400
    
    files = request.files.getlist('files')
    report_path = './uploads/report.xlsx'
    
    # Создаем новый Excel файл
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Compliance Report"
    
    # Заголовки столбцов
    sheet.append(['Filename', 'Result'])
    
    for file in files:
        file_path = f"./uploads/{file.filename}"
        file.save(file_path)
        
        # Извлечение текста из загруженного файла и регламента
        text = extract_text_from_word(file_path)
        regulation_text = extract_text_from_word('regulation.docx')  # Пример регламента
        
        # Проверка соответствия
        result = check_compliance(text, regulation_text)
        
        # Записываем данные в Excel
        sheet.append([file.filename, result])
        
        # Удаляем файл после обработки
        os.remove(file_path)
    
    # Сохраняем Excel файл
    workbook.save(report_path)
    
    return jsonify({"report": "Excel report generated successfully", "report_path": report_path})
