from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from datetime import datetime, timedelta
import json
import os
import uuid
import hashlib

app = Flask(__name__)
app.secret_key = 'sipsok-secret-key-2024'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

# Файлы для хранения
TASKS_FILE = 'tasks.json'
USERS_FILE = 'users.json'

def load_tasks(user_id='default'):
    if os.path.exists(TASKS_FILE):
        try:
            with open(TASKS_FILE, 'r', encoding='utf-8') as f:
                all_tasks = json.load(f)
                return all_tasks.get(user_id, [])
        except:
            return []
    return []

def save_tasks(tasks, user_id='default'):
    if os.path.exists(TASKS_FILE):
        try:
            with open(TASKS_FILE, 'r', encoding='utf-8') as f:
                all_tasks = json.load(f)
        except:
            all_tasks = {}
    else:
        all_tasks = {}
    
    all_tasks[user_id] = tasks
    
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_tasks, f, indent=4, ensure_ascii=False)

def load_users():
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_users(users):
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=4, ensure_ascii=False)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_task_categories():
    return ['Работа', 'Личное', 'Здоровье', 'Покупки', 'Семья', 'Образование', 'Другое']

def get_task_priorities():
    return ['Высокий', 'Средний', 'Низкий']

@app.before_request
def check_auth():
    # Разрешаем доступ к страницам логина, регистрации и статическим файлам без авторизации
    if request.endpoint in ['login', 'register', 'static']:
        return
    if 'user_id' not in session:
        return redirect(url_for('login'))

@app.route('/')
def index():
    user_id = session['user_id']
    tasks = load_tasks(user_id)
    categories = get_task_categories()
    priorities = get_task_priorities()
    
    # Фильтрация по статусу
    filter_status = request.args.get('status', 'all')
    if filter_status == 'completed':
        tasks = [task for task in tasks if task['completed']]
    elif filter_status == 'active':
        tasks = [task for task in tasks if not task['completed']]
    
    # Фильтрация по категории
    filter_category = request.args.get('category', 'all')
    if filter_category != 'all':
        tasks = [task for task in tasks if task.get('category') == filter_category]
    
    # Сортировка
    sort_by = request.args.get('sort', 'date')
    if sort_by == 'priority':
        priority_order = {'Высокий': 1, 'Средний': 2, 'Низкий': 3}
        tasks.sort(key=lambda x: priority_order.get(x.get('priority', 'Низкий'), 3))
    elif sort_by == 'title':
        tasks.sort(key=lambda x: x['title'].lower())
    else:
        tasks.sort(key=lambda x: x.get('due_date', '9999-99-99'))
    
    return render_template('index.html', 
                         tasks=tasks, 
                         categories=categories,
                         priorities=priorities,
                         filter_status=filter_status,
                         filter_category=filter_category,
                         sort_by=sort_by,
                         now=datetime.now())

@app.route('/add', methods=['POST'])
def add_task():
    if 'user_id' not in session:
        flash('❌ Необходимо авторизоваться', 'error')
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    category = request.form.get('category', 'Другое')
    priority = request.form.get('priority', 'Средний')
    due_date = request.form.get('due_date', '')
    reminder = request.form.get('reminder', '')
    
    print(f"Добавление задачи: {title}")  # Debug
    
    if title:
        tasks = load_tasks(user_id)
        new_task = {
            'id': str(uuid.uuid4()),
            'title': title,
            'description': description,
            'category': category,
            'priority': priority,
            'due_date': due_date,
            'reminder': reminder,
            'completed': False,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'completed_at': None
        }
        tasks.append(new_task)
        save_tasks(tasks, user_id)
        flash('✅ Задача добавлена успешно!', 'success')
    else:
        flash('❌ Название задачи не может быть пустым!', 'error')
    
    return redirect(url_for('index'))

@app.route('/complete/<string:task_id>')
def complete_task(task_id):
    user_id = session['user_id']
    tasks = load_tasks(user_id)
    for task in tasks:
        if task['id'] == task_id:
            task['completed'] = not task['completed']
            task['completed_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S') if task['completed'] else None
            break
    save_tasks(tasks, user_id)
    return redirect(url_for('index'))

@app.route('/delete/<string:task_id>')
def delete_task(task_id):
    user_id = session['user_id']
    tasks = load_tasks(user_id)
    tasks = [task for task in tasks if task['id'] != task_id]
    save_tasks(tasks, user_id)
    flash('🗑️ Задача удалена!', 'warning')
    return redirect(url_for('index'))

@app.route('/edit/<string:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    user_id = session['user_id']
    tasks = load_tasks(user_id)
    task = next((t for t in tasks if t['id'] == task_id), None)
    
    if not task:
        flash('❌ Задача не найдена!', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        category = request.form.get('category', 'Другое')
        priority = request.form.get('priority', 'Средний')
        due_date = request.form.get('due_date', '')
        reminder = request.form.get('reminder', '')
        
        if title:
            task['title'] = title
            task['description'] = description
            task['category'] = category
            task['priority'] = priority
            task['due_date'] = due_date
            task['reminder'] = reminder
            save_tasks(tasks, user_id)
            flash('✅ Задача обновлена!', 'success')
            return redirect(url_for('index'))
        else:
            flash('❌ Название задачи не может быть пустым!', 'error')
    
    categories = get_task_categories()
    priorities = get_task_priorities()
    
    return render_template('edit.html', task=task, categories=categories, priorities=priorities)

@app.route('/clear_completed')
def clear_completed():
    user_id = session['user_id']
    tasks = load_tasks(user_id)
    tasks = [task for task in tasks if not task['completed']]
    save_tasks(tasks, user_id)
    flash('🧹 Выполненные задачи очищены!', 'info')
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        
        users = load_users()
        user = users.get(email)
        
        if user and user['password'] == hash_password(password):
            session['user_id'] = user['id']
            session['user_email'] = email
            flash('✅ Вход выполнен успешно!', 'success')
            return redirect(url_for('index'))
        else:
            flash('❌ Неверный email или пароль', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()
        
        if password != confirm_password:
            flash('❌ Пароли не совпадают', 'error')
            return render_template('register.html')
        
        users = load_users()
        if email in users:
            flash('❌ Пользователь с таким email уже существует', 'error')
            return render_template('register.html')
        
        user_id = str(uuid.uuid4())
        users[email] = {
            'id': user_id,
            'email': email,
            'password': hash_password(password),
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        save_users(users)
        session['user_id'] = user_id
        session['user_email'] = email
        flash('✅ Регистрация успешна!', 'success')
        return redirect(url_for('index'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('👋 До свидания!', 'info')
    return redirect(url_for('login'))

@app.route('/profile')
def profile():
    user_id = session['user_id']
    tasks = load_tasks(user_id)
    
    stats = {
        'total': len(tasks),
        'completed': sum(1 for task in tasks if task['completed']),
        'active': sum(1 for task in tasks if not task['completed'])
    }
    
    return render_template('profile.html', stats=stats, current_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

if __name__ == '__main__':
    # Создаем необходимые файлы если их нет
    if not os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'w', encoding='utf-8') as f:
            json.dump({}, f, indent=4)
    
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump({}, f, indent=4)
    
    print("Запуск приложения на http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)