from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# Функция для поиска флага в базе
def get_flag(user_id):
    try:
        conn = sqlite3.connect('ctf.db')
        cursor = conn.cursor()
        # ТА САМАЯ УЯЗВИМОСТЬ: прямая вставка строки
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
        res = get_flag(uid)
        if res:
            msg = f"[УСПЕХ]: {res}"
        else:
            msg = "[ОШИБКА]: Доступ запрещен"
    
    return render_template_string('''
        <body style="background:#111;color:#0f0;text-align:center;font-family:monospace;padding-top:100px">
            <h1>IIAU REMOTE TERMINAL</h1>
            <form method="post">
                <input type="text" name="id" placeholder="ID...">
                <button type="submit">ВХОД</button>
            </form>
            <p>{{msg}}</p>
        </body>
    ''', msg=msg)

if __name__ == "__main__":
    app.run()