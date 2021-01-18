from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL


app = Flask(__name__)


# MySql Conneting

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "hospital"
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

mysql = MySQL(app)

@app.route('/') 
def index(): 
    #create a cursor
    cursor = mysql.connection.cursor() 
    #execute select statement to fetch data to be displayed in combo/dropdown
    kontrol = cursor.execute('SELECT id,name FROM doctor') 
    #fetch all rows ans store as a set of tuples 
    joblist = cursor.fetchall() 
    #render template and send the set of tuples to the HTML file for displaying
    if(kontrol>0):
        yaz = "var"
    else:
       yaz = "yok"
    return render_template("input.html",joblist=joblist,test=yaz)

# Hakkımızda Sayfası
@app.route('/hakkimizda')
def hakkimizda():
   return render_template("hakkimizda.html", sayfabasligi="Hakkımızda Sayfası")

# Form Sayfası
@app.route('/mesajyazin')
def mesajyazin():
   return render_template("form.html")


# Form Verileri Alma
@app.route('/hastakayit', methods=['POST', 'GET'])
def verilerial():
   if request.method == 'POST':
      isim = request.form.get('isim') 
      mesaj = request.form.get('soyad')
      tel = request.form.get('tel')
      adres = request.form.get('adres')
      doctor = request.form.get('doctor')

      cursor = mysql.connection.cursor()

      sorgu = "INSERT INTO patient VALUES(%s,%s,%s,%s,%s,%s)"

      cursor.execute(sorgu,(None,isim,mesaj,tel,adres,doctor))
      mysql.connection.commit()
      cursor.close()

      return render_template("verilerigoster.html",isim=isim,mesaj=mesaj,tel=tel,adres=adres,doctor=doctor)

   else:
      return render_template("verilerigoster.html",hata="Formdan veri gelmedi!")

# Mysql Kullanıcı Ekleme
@app.route('/mesajyazin', methods=['POST'])
def kullanicieklesonuc():
   if request.method == 'POST':
      isim = request.form.get('isim') 
      mesaj = request.form.get('soyad')
      tel = request.form.get('tel')
      adres = request.form.get('adres')
      doctor = request.form.get('doctor')

      cursor = mysql.connection.cursor()

      sorgu = "INSERT INTO kullanicilar VALUES(%s,%s,%s,%s,%s,%s)"

      cursor.execute(sorgu,(None,isim,mesaj,tel,adres,doctor))
      mysql.connection.commit()
      cursor.close()


      return render_template("form.html",isim=isim,mesaj=mesaj,tel=tel,adres=adres,doctor=doctor)

   else:
      return render_template("form.html",hata="Formdan veri gelmedi!")

if __name__ == "__main__":
    app.run(debug=True)