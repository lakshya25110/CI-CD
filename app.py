from flask import Flask, render_template, request, redirect, url_for, flash
import os
import json
from datetime import datetime
from pathlib import Path

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

# Blog setup
BLOG_FILE = Path('data/blog_posts.json')
Path('data').mkdir(exist_ok=True)

def get_blog_posts():
    if not BLOG_FILE.exists():
        return []
    with open(BLOG_FILE) as f:
        return json.load(f)

def save_blog_post(title, content):
    posts = get_blog_posts()
    posts.append({
        'id': len(posts) + 1,
        'title': title,
        'content': content,
        'date': datetime.now().strftime("%Y-%m-%d %H:%M")
    })
    with open(BLOG_FILE, 'w') as f:
        json.dump(posts, f, indent=2)

@app.route('/')
def home():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/blog')
def blog():
    return render_template('blog.html', posts=get_blog_posts())

@app.route('/write-blog', methods=['GET', 'POST'])
def write_blog():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        if title and content:
            save_blog_post(title, content)
            flash('Blog post published!', 'success')
            return redirect(url_for('blog'))
        flash('Title and content required!', 'error')
    return render_template('write_blog.html')

if __name__ == '__main__':
    app.run(debug=True)
