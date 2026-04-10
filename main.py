from flask import Flask, request, render_template_string
import sqlite3
import os

app = Flask(__name__)

# Функция для настройки базы данных при каждом запуске
def init_db():
    conn = sqlite3.connect('ctf.db')
    cursor = conn.cursor()
    # Создаем таблицу, если её вдруг нет
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS system_vault (
            id INTEGER PRIMARY KEY,
            flag_content TEXT
        )
    ''')
    # Проверяем, есть ли там наш флаг, если нет - добавляем
    cursor.execute("SELECT * FROM system_vault WHERE id=1337")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO system_vault (id, flag_content) VALUES (1337, 'IIAU{sqlite_is_easy_to_hack}')")
    
    conn.commit()
    conn.close()

def get_flag(user_id):
    try:
        conn = sqlite3.connect('ctf.db')
        cursor = conn.cursor()
        # ТА САМАЯ УЯЗВИМОСТЬ для взлома
        query = f"SELECT flag_content FROM system_vault WHERE id = {user_id}"
        cursor.execute(query)
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None
    except Exception as e:
        return f"Ошибка SQL: {e}"

@app.route('/', methods=['GET', 'POST'])
def index():
    msg = ""
    if request.method == 'POST':
        uid = request.form.get('id')
        # Защита от пустого ввода, чтобы не было ошибки
        if not uid:
            msg = "[ОШИБКА]: Введите ID"
        else:
            res = get_flag(uid)
            if res:
                msg = f"[УСПЕХ]: {res}"
            else:
                msg = "[ОШИБКА]: Запись не найдена"
    
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head><meta charset="utf-8"><title>IIAU TERMINAL</title></head>
        <body style="background:#111;col
