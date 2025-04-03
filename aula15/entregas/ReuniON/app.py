from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import calendar
from babel.dates import format_date
from datetime import datetime
import secrets
import os

# Inicialização do app e db
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reunion.db'
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'

# Configurações de e-mail (substitua com seus dados reais)
app.config['MAIL_SERVER'] = 'smtp.example.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'seu_email@example.com'
app.config['MAIL_PASSWORD'] = 'sua_senha'

db = SQLAlchemy(app)
mail = Mail(app)

# Modelos (agora definidos no mesmo arquivo)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    password_hash = db.Column(db.String(128), nullable=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    participants = db.relationship('User', secondary='meeting_participants')

meeting_participants = db.Table('meeting_participants',
    db.Column('meeting_id', db.Integer, db.ForeignKey('meeting.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

class CustomCalendar(calendar.LocaleHTMLCalendar):
    def formatday(self, day, weekday):
        if day == 0:
            return '<td></td>'
        return f'<td><span class="day">{day}</span><span class="add-event" data-day="{day}">+</span></td>'

    def formatmonth(self, year, month, withyear=True):
        self.year, self.month = year, month
        return super().formatmonth(year, month, withyear)
    
    
@app.context_processor
def inject_now():
    return {
        'now': datetime.now(),
        'datetime': datetime  
    }


# Rotas de Autenticação
@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('dashboard'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('dashboard'))
        flash('E-mail ou senha incorretos', 'error')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        
        if User.query.filter_by(email=email).first():
            flash('E-mail já cadastrado', 'error')
            return redirect(url_for('register'))
        
        new_user = User(name=name, email=email, phone=phone)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Cadastro realizado com sucesso! Faça login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Você foi desconectado', 'info')
    return redirect(url_for('login'))

# Rotas de Recuperação de Senha
@app.route('/recovery', methods=['GET', 'POST'])
def recovery():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        
        if user:
            token = secrets.token_urlsafe(32)
            reset_url = url_for('reset_password', token=token, _external=True)
            
            try:
                msg = Message(
                    subject="Recuperação de Senha - ReuniOn",
                    recipients=[user.email],
                    html=f"""<h1>Recuperação de Senha</h1>
                           <p>Clique no link para redefinir sua senha:</p>
                           <a href="{reset_url}">{reset_url}</a>"""
                )
                mail.send(msg)
                flash('E-mail de recuperação enviado! Verifique sua caixa de entrada.', 'success')
            except Exception as e:
                flash('Erro ao enviar e-mail de recuperação', 'error')
        else:
            flash('E-mail não encontrado', 'error')
        
        return redirect(url_for('recovery'))
    return render_template('recovery.html')

@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if request.method == 'POST':
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        
        if new_password != confirm_password:
            flash('As senhas não coincidem', 'error')
            return redirect(url_for('reset_password', token=token))
        
        # Aqui você deve validar o token na sua implementação real
        user = User.query.get(1)  # Substitua pela lógica de validação do token
        user.set_password(new_password)
        db.session.commit()
        
        flash('Senha redefinida com sucesso!', 'success')
        return redirect(url_for('login'))
    return render_template('reset_password.html', token=token)

# Rotas do Dashboard e Reuniões
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get_or_404(session['user_id'])
    year = request.args.get('year', datetime.now().year, type=int)
    month = request.args.get('month', datetime.now().month, type=int)
    
    cal = CustomCalendar(locale='pt_BR').formatmonth(year, month)
    month_names = [format_date(datetime(2023, m, 1), 'MMMM', locale='pt_BR').capitalize() 
                  for m in range(1, 13)]
    
    meetings = Meeting.query.filter(
        Meeting.date >= datetime(year, month, 1),
        Meeting.date < (datetime(year, month + 1, 1) if month < 12 else datetime(year + 1, 1, 1))
    ).all()
    
    return render_template('dashboard.html',
                         user=user,
                         calendar=cal,
                         year=year,
                         month=month,
                         month_names=month_names,
                         meetings=meetings,
                         now=datetime.now(),
                         User=User
                         ) 

@app.route('/meeting/add', methods=['POST'])
def add_meeting():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    title = request.form['title']
    date_str = request.form['date']
    time_str = request.form['time']
    description = request.form.get('description', '')
    participants = request.form.getlist('participants')
    
    try:
        date = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    except ValueError:
        flash('Data/hora inválida', 'error')
        return redirect(url_for('dashboard'))
    
    new_meeting = Meeting(
        title=title,
        date=date,
        description=description,
        creator_id=session['user_id']
    )
    
    for user_id in participants:
        user = User.query.get(user_id)
        if user:
            new_meeting.participants.append(user)
    
    db.session.add(new_meeting)
    db.session.commit()
    
    flash('Reunião agendada com sucesso!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/meeting/delete/<int:id>')
def delete_meeting(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    meeting = Meeting.query.get_or_404(id)
    if meeting.creator_id != session['user_id']:
        flash('Você não tem permissão para cancelar esta reunião', 'error')
        return redirect(url_for('dashboard'))
    
    db.session.delete(meeting)
    db.session.commit()
    
    flash('Reunião cancelada com sucesso', 'success')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

