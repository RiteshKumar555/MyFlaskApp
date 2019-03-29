from flask import Flask,render_template,flash,redirect,url_for,session,request,logging,send_from_directory
from data1 import Academicssyallabus
from flask_mysqldb import MySQL
from wtforms import Form,StringField,TextAreaField,PasswordField,validators,FileField
from passlib.hash import sha256_crypt
from functools import wraps
from flask_wtf.file import FileField, FileRequired
from werkzeug import secure_filename
from wtforms.validators import InputRequired
import os




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

        result=cur.execute("SELECT * from users WHERE username = %s ",[username])

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

def dashboard():

    cur=mysql.connection.cursor()

    result=cur.execute("SELECT * FROM articles")
   
    articles=cur.fetchall()
    
  

    if result>0:
        return render_template('dashboard.html',articles=articles)
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
    flash('You have successfully logged',"success")
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


@app.route('/examdates')
def examdates():
    return render_template('examdates.html')



@app.route('/criteria')
def criteria():
    return render_template('criteria.html')  

@app.route('/Cat')
def Cat():
    return render_template('Cat.html')


@app.route('/Cmat')
def Cmat():
    return render_template('Cmat.html')

@app.route('/syallabus')
def syallabus():
    return render_template('syallabus.html')


@app.route('/academicssyallabus')
def academicssyallabus():
    cur=mysql.connection.cursor()

    result=cur.execute("SELECT * FROM academicssyallabus")
   
    academicssyallabus=cur.fetchall()
    
  

    if result>0:
        return render_template('academicssyallabus.html',academicssyallabus=academicssyallabus)
    else:
        msg='No syallabus Found'
        return render_template('academicssyallabus.html')  

        cur.close()
     

@app.route('/academicsyallabus/<string:id>/')
def academicsyallabus(id):

    cur=mysql.connection.cursor()

    result=cur.execute("SELECT * FROM academicssyallabus WHERE  id=%s",[id])
   
    academicsyallabus=cur.fetchone()
    
    return render_template('academicsyallabus.html' , academicsyallabus=academicsyallabus)

@app.route('/ASdashboard')
@is_logged_in
def ASdashboard():

    cur=mysql.connection.cursor()

    result=cur.execute("SELECT * FROM academicssyallabus")
   
    academicssyallabus=cur.fetchall()
    
  

    if result>0:
        return render_template('ASdashboard.html',academicssyallabus=academicssyallabus)
    else:
        msg='No syallabus Found'
        return render_template('ASdashboard.html')  
    return render_template('ASdashboard.html')    


class A_SyallabusForm(Form):
    universityname=StringField('universityname', [validators.Length(min=1, max=200)])
    courses = StringField('courses', [validators.Length(min=1, max=1000)])
    year = StringField('year', [validators.Length(max=11)])
    sysllabus = TextAreaField('sysllabus', [validators.Length(min=1,max=2000)])


@app.route('/addacademic_syallabus', methods=['GET', 'POST'])
@is_logged_in
def addacademic_syallabus():
    form = A_SyallabusForm(request.form)
    if request.method == 'POST' and form.validate():
        universityname = form.universityname.data
        year = form.year.data
        courses = form.courses.data
        sysllabus = form.sysllabus.data

       
        cur = mysql.connection.cursor()

        
        cur.execute("INSERT INTO academicssyallabus(universityname,courses,year, sysllabus) VALUES(%s, %s,%s,%s)",(universityname,courses,year, sysllabus))

       
        mysql.connection.commit()

        cur.close()

        flash('syallabus present here:', 'success')

        return redirect(url_for('ASdashboard'))

    return render_template('addacademic_syallabus.html', form=form) 


@app.route('/edit_ACsyallabus/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_ACsyallabus(id):

    cur=mysql.connection.cursor()

    result=cur.execute("SELECT * FROM academicssyallabus WHERE id = %s",[id])

    academicsyallabus = cur.fetchone()


    form = A_SyallabusForm(request.form)
      
    form.universityname.data=academicsyallabus['universityname']
    form.courses.data=academicsyallabus['courses']
    form.year.data=academicsyallabus['year']
    form.sysllabus.data=academicsyallabus['sysllabus']

    if request.method == 'POST' and form.validate():

        universityname = request.form['universityname']
        courses = request.form['courses']
        year = request.form['year']
        sysllabus = request.form['sysllabus']

       
        cur = mysql.connection.cursor()

        
        cur.execute("UPDATE academicssyallabus SET universityname = %s,courses = %s,year=%s, sysllabus = %s WHERE id = %s",(universityname,courses,year,sysllabus,id))

       
        mysql.connection.commit()

        cur.close()

        flash('Syallabus update', 'success')

        return redirect(url_for('ASdashboard'))

    return render_template('edit_ACsyallabus.html', form=form)

@app.route('/delete_ACsyallabus/<string:id>')    
@is_logged_in
def delete_ACsyallabus(id):
    cur=mysql.connection.cursor()

    cur.execute("DELETE FROM academicssyallabus WHERE id = %s",[id])

    mysql.connection.commit()

    cur.close()

    flash('syallabus Updated', 'success')

    return redirect(url_for('ASdashboard'))

@app.route('/academicssyallabus')
def academic_ssyallabus():
    return render_template('academicssyallabus.html')

@app.route('/competitivessyallabus')
def competitivessyallabus():
    cur=mysql.connection.cursor()

    result=cur.execute("SELECT * FROM competitivessyallabus")
   
    competitivessyallabus=cur.fetchall()
    
  

    if result>0:
        return render_template('competitivessyallabus.html',competitivessyallabus=competitivessyallabus)
    else:
        msg='No syallabus Found'
        return render_template('competitivessyallabus.html')  

        cur.close()

@app.route('/competitivesyallabus/<string:id>/')
def competitivesyallabus(id):

    cur=mysql.connection.cursor()

    result=cur.execute("SELECT * FROM competitivessyallabus WHERE  id=%s",[id])
   
    competitivesyallabus=cur.fetchone()
    
    return render_template('competitivesyallabus.html' , competitivesyallabus=competitivesyallabus)

@app.route('/C_dashboard')
@is_logged_in
def C_dashboard():

    cur=mysql.connection.cursor()

    result=cur.execute("SELECT * FROM competitivessyallabus")
   
    competitivessyallabus=cur.fetchall()
    
  

    if result>0:
        return render_template('C_dashboard.html',competitivessyallabus=competitivessyallabus)
    else:
        msg='No syallabus Found'
        return render_template('C_dashboard.html')  
    return render_template('C_dashboard.html')    



class C_SyallabusForm(Form):
   
    courses = StringField('courses', [validators.Length(min=1, max=1000)])
    syllabus = TextAreaField('syllabus', [validators.Length(min=1,max=50000)])


@app.route('/addC_syallabus', methods=['GET', 'POST'])
@is_logged_in
def addC_syallabus():
    form = C_SyallabusForm(request.form)
    if request.method == 'POST' and form.validate():
       
       
        courses = form.courses.data
        syllabus = form.syllabus.data

       
        cur = mysql.connection.cursor()

        
        cur.execute("INSERT INTO competitivessyallabus(courses, syllabus) VALUES(%s, %s)",(courses, syllabus))

       
        mysql.connection.commit()

        cur.close()

        flash('syallabus present here:', 'success')

        return redirect(url_for('C_dashboard'))

    return render_template('addC_syallabus.html', form=form) 


@app.route('/editC_syallabus/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def editC_syallabus(id):

    cur=mysql.connection.cursor()

    result=cur.execute("SELECT * FROM competitivessyallabus WHERE id = %s",[id])

    competitivesyallabus = cur.fetchone()


    form = C_SyallabusForm(request.form)
      
    form.courses.data=competitivesyallabus
    form.syllabus.data=competitivesyallabus['syllabus']

    if request.method == 'POST' and form.validate():

        
        courses = request.form['courses']
       
        syllabus = request.form['syllabus']

       
        cur = mysql.connection.cursor()

        
        cur.execute("UPDATE competitivessyallabus SET courses = %s, syllabus = %s WHERE id = %s",(courses,syllabus,id))

       
        mysql.connection.commit()

        cur.close()

        flash('Syallabus update', 'success')

        return redirect(url_for('C_dashboard'))

    return render_template('editC_syallabus.html', form=form)

@app.route('/deleteC_syallabus/<string:id>')    
@is_logged_in
def deleteC_syallabus(id):
    cur=mysql.connection.cursor()

    cur.execute("DELETE FROM competitivessyallabus WHERE id = %s",[id])

    mysql.connection.commit()

    cur.close()

    flash('syallabus Updated', 'success')

    return redirect(url_for('C_dashboard'))


APP_ROOT = os.path.dirname(os.path.abspath(__file__))



@app.route("/upload", methods=["GET","POST"])
def upload():
    if request.method=='GET':
        return render_template("upload.html")
    if request.method=='POST':

        target = os.path.join(APP_ROOT, 'images/')
        print(target)
        if not os.path.isdir(target):
            os.mkdir(target)
        else:
            print("Couldn't create upload directory: {}".format(target))
            print(request.files.getlist("file"))
        for upload in request.files.getlist("file"):
            print(file)
            print(upload)
            print("{} is the file name".format(upload.filename))
            filename = upload.filename
            # print(testtttttttttttt)
            destination = "/".join([target, filename])
            print ("Accept incoming file:", filename)
            print ("Save it to:", destination)
            upload.save(destination)
            image_names = os.listdir('./images')
            print(image_names)
            if upload:
          
                return render_template("upload.html", image_names=image_names)

        

    if request.method=='GET':
        return render_template("upload.html")    
    return render_template("upload.html")
@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("images",filename)

    





@app.route('/uploads/<path:filename>')
def download_file(filename):
    return send_from_directory("images", filename, as_attachment=True)

@app.route('/upload')
def preview_fle():
    image_names = os.listdir('./images')
    print(image_names)
    return send_from_directory("images", image_names=image_names)




if __name__ == "__main__":
    app.run(debug=True)    
