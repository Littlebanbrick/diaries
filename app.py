import os
import json
import sqlite3
from datetime import datetime,timedelta
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__)
app.secret_key = "the_secret_key_of_Diaries"

DATABASE = "diaries.db"
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg',  'heic'}
MAX_IMAGES = 9

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 48 * 1024 * 1024  # 限制上传总大小48MB

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS diaries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                subtitle TEXT,
                content TEXT NOT NULL,
                image_paths TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        db.commit()
        db.close()
        
init_db()

# ========== 工具函数 ==========
def allowed_file(filename):
    """判断一个“图片”文件是否有效"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_images(files):
    """保存上传的图片文件，返回相对路径列表"""
    saved_paths = []
    for file in files:
        if file and allowed_file(file.filename):
            # 生成唯一文件名
            ext = file.filename.rsplit('.', 1)[1].lower()
            new_filename = f"{uuid.uuid4().hex}.{ext}"
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
            file.save(save_path)
            # 存储相对路径（用于 url_for）
            saved_paths.append(f"uploads/{new_filename}")
    return saved_paths

@app.route("/")
def homepage():
    return render_template("homepage.html")

@app.route("/update/")
def update():
    return render_template("update.html")

@app.route('/update/submit/', methods=['POST'])
def submit_diary():
    title = request.form.get('title', '').strip()
    subtitle = request.form.get('subtitle', '').strip()
    content = request.form.get('content', '').strip()

    if not title or not content:
        flash('标题和正文不能为空')
        return redirect(url_for('update'))

    # 处理图片
    uploaded_files = request.files.getlist('images')
    files = [f for f in uploaded_files if f and f.filename != '']
    if len(files) > MAX_IMAGES:
        flash(f'最多上传 {MAX_IMAGES} 张图片')
        return redirect(url_for('update'))

    image_paths = save_images(files)   # 返回相对路径列表
    image_paths_json = json.dumps(image_paths)

    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        INSERT INTO diaries (title, subtitle, content, image_paths)
        VALUES (?, ?, ?, ?)
    ''', (title, subtitle, content, image_paths_json))
    db.commit()
    diary_id = cursor.lastrowid
    db.close()

    return redirect(url_for('success', diary_id=diary_id))

@app.route("/update/success/")
def success():
    diary_id=request.args.get('diary_id')
    return render_template("success.html",diary_id=diary_id)

@app.route("/update/failure/<error_message>/")
def failure(error_message):
    return render_template("failure.html",error_message=error_message)

@app.route('/flashback/')
def flashback():
    db = get_db()
    cursor = db.execute('SELECT * FROM diaries ORDER BY updated_at DESC')
    rows = cursor.fetchall()
    
    diaries = []
    for row in rows:
        diary = dict(row)
        if diary['image_paths']:
            diary['image_list'] = json.loads(diary['image_paths'])
        else:
            diary['image_list'] = []
        diaries.append(diary)
    
    db.close()
    return render_template('flashback.html', diaries=diaries)

@app.route('/diary/<int:diary_id>')
def view_diary(diary_id):
    db = get_db()
    diary = db.execute('SELECT * FROM diaries WHERE id = ?', (diary_id,)).fetchone()
    db.close()
    if diary is None:
        abort(404)

    diary = dict(diary)
    if diary['image_paths']:
        diary['image_list'] = json.loads(diary['image_paths'])
    else:
        diary['image_list'] = []

    # 东八区时间转换（假设 updated_at 是 UTC 字符串）
    if diary['updated_at']:
        utc_time = datetime.strptime(diary['updated_at'], '%Y-%m-%d %H:%M:%S')
        beijing_time = utc_time + timedelta(hours=8)
        diary['display_date'] = beijing_time.strftime('%Y-%m-%d')
    else:
        diary['display_date'] = ''

    return render_template('view.html', diary=diary)

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)