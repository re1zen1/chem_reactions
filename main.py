from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chemistry.db'  # Змініть на відповідний URL вашої бази даних
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secret_key'  # Замініть на ваш ключ для сесій

db = SQLAlchemy(app)

# Модель користувача
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

# Створення класу(таблиці), що працює з усіма уроками нашого застосунку

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    student = db.Column(db.String(50), nullable=True)
    rating = db.Column(db.String(50), nullable=True)

    reagent_1_id = db.Column(db.Integer, nullable=True)
    reagent_1_category = db.Column(db.String(50), nullable=False)
    reagent_1_name = db.Column(db.String(50), nullable=False)
    reagent_1_formula = db.Column(db.String(50), nullable=False)
    reagent_1_weight = db.Column(db.Double, nullable=False)
    reagent_1_about = db.Column(db.Text, nullable=False)

    reagent_2_id = db.Column(db.Integer, nullable=True)
    reagent_2_category = db.Column(db.String(50), nullable=False)
    reagent_2_name = db.Column(db.String(50), nullable=False)
    reagent_2_formula = db.Column(db.String(50), nullable=False)
    reagent_2_weight = db.Column(db.Double, nullable=False)
    reagent_2_about = db.Column(db.Text, nullable=False)

    substance_id = db.Column(db.Integer, nullable=True) 
    substance_name = db.Column(db.String(50), nullable=False)
    substance_formula = db.Column(db.String(50), nullable=False) 
    substance_about = db.Column(db.Text, nullable=False) 
    
# Створення бази даних
with app.app_context():
    db.create_all()

# Відслідковуємо події головної сторінки 
@app.route('/')
def index():
    lessons = Lesson.query.order_by(Lesson.id).all()
    return render_template('index.html', lessons=lessons)

# Відслідковуємо події сторінки контактної інформації
@app.route("/about")
def about():
    return render_template("about.html")

# Відслідковуємо події сторінки зуроками

@app.route("/lessons_catalog")
def lessons_catalog():
    lessons = Lesson.query.order_by(Lesson.id).all()
    user = User.query.filter_by(username=session['username']).first()
    return render_template("lessons_catalog.html", lessons=lessons, user=user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

# Роути для авторизації
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first_or_404()

        if user and check_password_hash(user.password, password):
            # Авторизація успішна
            session['username'] = username
            if user.is_admin:
                # Якщо користувач - адміністратор
                return redirect(url_for('admin_dashboard'))
            else:
                # Якщо користувач - звичайний
                return redirect(url_for('user_dashboard'))
        else:
            flash('Логін або пароль некоректнi')
            return render_template(url_for('login'))
    return render_template('login.html')

@app.route('/admin')
def admin_dashboard():
    # Перевірка, чи користувач має доступ до адмін-панелі
    if 'username' in session:
        user = User.query.filter_by(username=session['username']).first()
        if user and user.is_admin:
            # lessons = Lesson.query.order_by(Lesson.id).all()
            return render_template('admin_page.html', user=user)
    return redirect(url_for('login'))

@app.route('/user')
def user_dashboard():
    # Перевірка, чи користувач має доступ до панелі користувача
    if 'username' in session:
        user = User.query.filter_by(username=session['username']).first()
        if user and not user.is_admin:
            lessons = Lesson.query.order_by(Lesson.id).all()
            return render_template('user_page.html', user=user, lessons=lessons)
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    # Вихід з облікового запису
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route("/create_lesson", methods=["POST", "GET"])
def create_lesson():
    lessons = Lesson.query.order_by(Lesson.id).all()
    user = User.query.filter_by(username=session['username']).first()
    if request.method == "POST":
        
        title = request.form['title']
        content = request.form['content']
        
        # reagent_1_id = request.form['reagent_1_id']
        reagent_1_category = request.form['reagent_1_category']
        reagent_1_name = request.form['reagent_1_name']
        reagent_1_formula = request.form['reagent_1_formula']
        reagent_1_weight = request.form['reagent_1_weight']
        reagent_1_about = request.form['reagent_1_about']
        # reagent_2_id = request.form['reagent_2_id']
        reagent_2_category = request.form['reagent_2_category']
        reagent_2_name = request.form['reagent_2_name']
        reagent_2_formula = request.form['reagent_2_formula']
        reagent_2_weight = request.form['reagent_2_weight']
        reagent_2_about = request.form['reagent_2_about']
        # substance_id = request.form['substance_id']
        substance_name = request.form['substance_name']
        substance_formula = request.form['substance_formula']
        substance_about = request.form['substance_about']
    
        lesson = Lesson(title=title, content=content,
                        reagent_1_category=reagent_1_category,reagent_1_name=reagent_1_name,
                        reagent_1_formula=reagent_1_formula, reagent_1_weight=reagent_1_weight, reagent_1_about=reagent_1_about,
                         reagent_2_category=reagent_2_category, reagent_2_name=reagent_2_name,
                        reagent_2_formula=reagent_2_formula, reagent_2_weight=reagent_2_weight, reagent_2_about=reagent_2_about,
                         substance_name=substance_name, substance_formula=substance_formula,
                        substance_about=substance_about)
        try:
            db.session.add(lesson)
            db.session.commit()
            return redirect("/lessons_catalog")
        except Exception as e:
            return f"Виникла помилкa: {str(e)}"
    else:
        return render_template("create_lesson.html", user=user, lessons=lessons)
                           
# Відслідковуємо події сторінки видалення товару

@app.route("/lessons_catalog/<int:id>/del", methods=["POST", "GET"])
def delete_lesson(id):
    lessons = Lesson.query.get_or_404(id)
    user = User.query.filter_by(username=session['username']).first()
    try:
        db.session.delete(lessons)
        db.session.commit()
        return redirect("admin_page.html", lessons=lessons, user=user)

    except:
        return redirect(url_for('lessons_catalog'))

# Відслідковуємо події сторінки редагування опису товару

@app.route("/create_lesson/<int:id>/update_lesson", methods=["POST", "GET"])
def update_lesson(id):
    lesson = Lesson.query.get_or_404(id)
    user = User.query.filter_by(username=session['username']).first()
    if request.method == "POST":
        lesson.title = request.form['title']
        lesson.content = request.form['content']
    
        lesson.reagent_1_category = request.form['reagent_1_category']
        lesson.reagent_1_name = request.form['reagent_1_name']
        lesson.reagent_1_formula = request.form['reagent_1_formula']
        lesson.reagent_1_weight = request.form['reagent_1_weight']
        lesson.reagent_1_about = request.form['reagent_1_about']

        lesson.reagent_2_category = request.form['reagent_2_category']
        lesson.reagent_2_name = request.form['reagent_2_name']
        lesson.reagent_2_formula = request.form['reagent_2_formula']
        lesson.reagent_2_weight = request.form['reagent_2_weight']
        lesson.reagent_2_about = request.form['reagent_2_about']

        lesson.substance_name = request.form['substance_name']
        lesson.substance_formula = request.form['substance_formula']
        lesson.substance_about = request.form['substance_about']

        try:
            db.session.commit()
            return redirect("/lessons_catalog")

        except:
            return "Виникла помилка"
    else:
        return render_template("lesson_update.html", lesson=lesson, user=user)

# # Відслідковуємо події сторінки зуроками

@app.route("/user/<int:id>/lesson_card/", methods=["POST", "GET"])
def lesson_card(id):
    lesson = Lesson.query.get_or_404(id)
    user = User.query.filter_by(username=session['username']).first()
    return render_template("lesson_card.html", lesson=lesson, user=user)
    

if __name__ == '__main__':
    app.run(debug=True)