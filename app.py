import os
import math
import string
from collections import Counter
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Конфигурация
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'txt'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

# Создаем папку для загрузок, если ее нет
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def process_text(filepath):
    # Чтение файла
    with open(filepath, 'r', encoding='utf-8') as file:
        text = file.read().lower()
    
    # Токенизация и очистка текста
    translator = str.maketrans('', '', string.punctuation + '«»—')
    words = text.translate(translator).split()
    
    # Подсчет TF (терминальной частоты)
    word_counts = Counter(words)
    total_words = len(words)
    
    # Сортировка слов по частоте (первые 50)
    sorted_words = word_counts.most_common(50)
    
    # Подсчет IDF (обратной частоты документа)
    # В реальном приложении нужно использовать корпус документов
    # Здесь используем фиктивное значение для демонстрации
    num_docs_in_corpus = 1000
    
    # Формируем результаты
    results = []
    for word, count in sorted_words:
        tf = count / total_words
        docs_with_word = max(1, count // 10)  # Эвристика для демонстрации
        idf = math.log(num_docs_in_corpus / docs_with_word)
        results.append({
            'word': word,
            'tf': round(tf, 6),
            'idf': round(idf, 6),
            'count': count
        })
    
    return results

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Проверяем, есть ли файл в запросе
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']
        
        # Если пользователь не выбрал файл
        if file.filename == '':
            return redirect(request.url)
        
        # Если файл разрешенного типа
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Обрабатываем файл
            results = process_text(filepath)
            
            # Удаляем файл после обработки (опционально)
            os.remove(filepath)
            
            return render_template('results.html', results=results)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)