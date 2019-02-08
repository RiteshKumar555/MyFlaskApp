from flask import Flask,render_template,flash,redirect,url_for,session,request,logging
# from data import Articles
from flask_mysqldb import MySQL
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt
from functools import wraps
app=Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '-p'
app.config['MYSQL_DB'] = 'myflaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['SECRET_KEY'] = 'FUCK'


mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def  about():
    return render_template('about.html')   

@app.route('/articles')
def  articles():
    cur=mysql.connection.cursor()

    result=cur.execute("SELECT * FROM articles")

    articles=cur.fetchall()

    if result>0:
        return render_template('articles.html',articles=articles)
    else:
        msg='No Article Found'
        return render_template('articles.html',msg=msg)

    cur.close()
 
     

@app.route('/article/<string:id>/')  
def article(id):

    cur=mysql.connection.cursor()

    result=cur.execute("SELECT * FROM articles WHERE id = %s",[id] )

    article=cur.fetchone()

    return render_template('article.html', article=article) 

class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        cur = mysql.connection.cursor()

      
        cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))

     
        mysql.connection.commit()

      
        cur.close()

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method =='POST':
        username=request.form['username']
        password_Candidate=request.form['password']

        cur=mysql.connection.cursor()

        result=cur.execute("SELECT * from usesr WHERE username = %s ",[username])

        if result>0:
            data=cur.fetchone()
            password=data['password']

            if sha256_crypt.verify(password_Candidate,password):
                app.logger.info('PASSWORD MATCHED')

                session['logged_in']=True
                session['username']=username
                

                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
               error='invalid login'
               return render_template('login.html' ,error=error)   

               cur.close()

        else:
            error='Username not found'
            return render_template('login.html' ,error=error)
           

    return render_template('login.html')  

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwrags):
        if 'logged_in' in session:
            return f(*args, **kwrags)
        else:
            flash("unauthorized ,Please Login",'danger')
            return redirect(url_for('login')) 
    return wrap   


@app.route('/dashboard')
@is_logged_in
def dashboard():

    cur=mysql.connection.cursor()

    result=cur.execute("SELECT articles.title,articles.body,syallabuses.courses,syallabuses.syallabus FROM articles,syallabuses WHERE article.articles=syallabuses.syallabuses ")
  


    articles=cur.fetchall()
  

    if result>0:
        return render_template('dashboard.html',articles=articles,syallabuses=syallabuses)
    else:
        msg='No Article Found'
        return render_template('dashboard.html')
    return render_template('dashboard.html')    



    
class ArticleForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=200)])
    body = TextAreaField('Body', [validators.Length(min=30)])


@app.route('/add_article', methods=['GET', 'POST'])
@is_logged_in
def add_article():
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data

       
        cur = mysql.connection.cursor()

        
        cur.execute("INSERT INTO articles(title, body, author) VALUES(%s, %s, %s)",(title, body, session['username']))

       
        mysql.connection.commit()

        cur.close()

        flash('Article Created', 'success')

        return redirect(url_for('dashboard'))

    return render_template('add_articles.html', form=form)


@app.route('/edit_article/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_article(id):

    cur=mysql.connection.cursor()

    result=cur.execute("SELECT * FROM articles WHERE id = %s",[id])

    article = cur.fetchone()


    form = ArticleForm(request.form)

    form.title.data=article['title']
    form.body.data=article['body']

    if request.method == 'POST' and form.validate():
        title = request.form['title']
        body = request.form['body']

       
        cur = mysql.connection.cursor()

        
        cur.execute("UPDATE articles SET title = %s, body = %s WHERE id = %s",(title,body,id))

       
        mysql.connection.commit()

        cur.close()

        flash('Article Updated', 'success')

        return redirect(url_for('dashboard'))

    return render_template('edit_article.html', form=form)

@app.route('/delete_article/<string:id>')    
@is_logged_in
def delete_article(id):
    cur=mysql.connection.cursor()

    cur.execute("DELETE FROM articles WHERE id = %s",[id])

    mysql.connection.commit()

    cur.close()

    flash('Article Updated', 'success')

    return redirect(url_for('dashboard'))

   

@app.route('/logout')
def logout():
    session.clear()
    flash('You have successfully logged')
    return redirect(url_for('login'))

@app.route('/courses')
def courses():
    return render_template('course.html')    

@app.route('/cat')
def cat():
    return render_template('cat.html')    

@app.route('/cmat')
def cmat():
    return render_template('cmat.html')

@app.route('/xat')
def xat():
    return render_template('xat.html')  

@app.route('/iift')
def iift():
    return render_template('iift.html')   

@app.route('/snap')
def snap():
    return render_template('snap.html')   

@app.route('/nmat')
def nmat():
    return render_template('nmat.html') 

@app.route('/mat')
def mat():
    return render_template('mat.html') 


@app.route('/mh-cet')
def mhcet():
    return render_template('mh-cet.html') 

@app.route('/ibsat')
def ibsat():
    return render_template('ibsat.html') 













@app.route('/syallabuses')
def  syallabuses():
    cur=mysql.connection.cursor()

    result=cur.execute("SELECT * FROM syallabuses")

    syallabuses=cur.fetchall()

    if result>0:
        return render_template('syallabuses.html',syallabuses=syallabuses)
    else:
        msg='No syallabus Found'
        return render_template('syallabuses.html',msg=msg)

    cur.close()
 
     

@app.route('/syallabus/<string:id>/')  
def syallabus(id):

    cur=mysql.connection.cursor()

    result=cur.execute("SELECT * FROM syallabuses WHERE id = %s",[id] )

    syallabus=cur.fetchone()

    return render_template('syallabus.html', syallabus=syallabus) 



class SyallabusForm(Form):
    courses = StringField('courses', [validators.Length(min=1, max=200)])
    syallabus = TextAreaField('syallabus', [validators.Length(min=1,max=2000)])


@app.route('/add_syallabus', methods=['GET', 'POST'])
@is_logged_in
def add_syallabus():
    form = SyallabusForm(request.form)
    if request.method == 'POST' and form.validate():
        courses = form.courses.data
        syallabus = form.syallabus.data

       
        cur = mysql.connection.cursor()

        
        cur.execute("INSERT INTO syallabuses(courses, syallabus) VALUES(%s, %s)",(courses, syallabus))

       
        mysql.connection.commit()

        cur.close()

        flash('syallabus present here:', 'success')

        return redirect(url_for('dashboard'))

    return render_template('add_syallabuses.html', form=form)    








       

if __name__ == '__main__':
    app.run(debug=True)

