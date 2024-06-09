import os
from pymongo import MongoClient
import datetime
import hashlib
import jwt
from flask import Flask, make_response, render_template, jsonify, request, redirect, url_for
from datetime import datetime, timedelta
from bson import ObjectId 
from werkzeug.utils import secure_filename
import random
import string

app = Flask(__name__)

SECRET_KEY = "SUCCESS"
DB_KEY = "sparta"

client = MongoClient(f'mongodb+srv://test:{DB_KEY}@cluster0.6bmi5a1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client.PT_Cahaya_Toner

sekarang = datetime.now()
tanggal = sekarang.strftime("%d-%m-%Y")
hari = tanggal.split("-")[0]
bulan = tanggal.split("-")[1]
tahun = tanggal.split("-")[2]
jam = sekarang.strftime("%H:%M")

def generateID(length):
    characters = string.ascii_uppercase + string.digits
    captcha = ''.join(random.choice(characters) for _ in range(length))
    return captcha
 
@app.route("/")
def home(): 
    myToken = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(myToken, SECRET_KEY, algorithms=["HS256"])
        user_info = db.users.find_one({"username": payload["id"]})
        return render_template('dashboard.html', user_info=user_info)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("sign_in", msg="Waktu login telah berakhir!"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("sign_in", msg="Silahkan login terlebih dahulu!"))


@app.route("/karyawan")
def karyawan():
    myToken = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(myToken, SECRET_KEY, algorithms=["HS256"])
        user_info = db.users.find_one({"username": payload["id"]})
        return render_template("karyawan.html", user_info=user_info)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))

@app.route("/customer")
def customer():
    myToken = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(myToken, SECRET_KEY, algorithms=["HS256"])
        user_info = db.users.find_one({"username": payload["id"]})
        return render_template("customer.html", user_info=user_info)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))

@app.route("/pesanan")
def pesanan():
    myToken = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(myToken, SECRET_KEY, algorithms=["HS256"])
        user_info = db.users.find_one({"username": payload["id"]})
        return render_template("pesanan.html", user_info=user_info)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))

@app.route("/sewa")
def sewa():
    myToken = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(myToken, SECRET_KEY, algorithms=["HS256"])
        user_info = db.users.find_one({"username": payload["id"]})
        return render_template("sewa.html", user_info=user_info)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))
    
@app.route("/pendapatan")
def pendapatan():
    myToken = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(myToken, SECRET_KEY, algorithms=["HS256"])
        user_info = db.users.find_one({"username": payload["id"]})
        return render_template("pendapatan.html", user_info=user_info)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))
    
@app.route("/produk")
def produk():
    myToken = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(myToken, SECRET_KEY, algorithms=["HS256"])
        user_info = db.users.find_one({"username": payload["id"]})
        return render_template("produk.html", user_info=user_info)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))
    
@app.route("/chart")
def chart():
    myToken = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(myToken, SECRET_KEY, algorithms=["HS256"])
        user_info = db.users.find_one({"username": payload["id"]})
        return render_template("chart.html", user_info=user_info, tahun=tahun, bulan=bulan)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))
    
@app.route("/profile")
def profile():
    myToken = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(myToken, SECRET_KEY, algorithms=["HS256"])
        user_info = db.users.find_one({"username": payload["id"]})
        return render_template("profile.html", user_info=user_info)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))

@app.route("/update_profile", methods=["POST"])
def update_profile():
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        username = payload["id"]
        nama = request.form["nama"]
        newDoc = {"profileName": nama}
        if "filePict" in request.files:
            file = request.files["filePict"]
            filename = secure_filename(file.filename)
            extension = filename.split(".")[-1]
            file_path = f"assets/img/profile/{username}.{extension}"
            file.save("./static/" + file_path)
            newDoc["profile"] = filename
            newDoc["profilePict"] = file_path
        db.users.update_one({"username": payload["id"]}, {"$set": newDoc})
        return jsonify({"msg": "Profile berhasil di update!"})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))
 
@app.route("/add_data/form/<page>", methods=['GET', 'POST'])
def add_data(page):
    if page == 'karyawan':
        if request.method == 'POST':
            id = generateID(4)
            dataCustomer = list(db.data_customer.find({}, {'_id' : False}))
            for data in dataCustomer:
                for data in dataCustomer:
                    if (id == data['id']):
                        id = generateID(4)
                        continue
            nik = request.form['nik']
            namaLengkap = request.form['nama']
            posisi = request.form['posisi']
            email = request.form['email']
            telpone = request.form['telpone']
            gaji = request.form['gaji']
            
            docKaryawan = {
                'id' : id,
                'nik' : nik,
                'namaLengkap' : namaLengkap,
                'posisi' : posisi,
                'email' : email,
                'telpone' : telpone,
                'gaji' : gaji,
            }
            
            db.data_karyawan.insert_one(docKaryawan)
            return redirect(url_for('karyawan'))
        
        return render_template('form_karyawan.html', action="tambah")
    elif page == 'customer':
        if request.method == 'POST':
            id = generateID(4)
            dataCustomer = list(db.data_customer.find({}, {'_id' : False}))
            for data in dataCustomer:
                for data in dataCustomer:
                    if (id == data['id']):
                        id = generateID(4)
                        continue
            perusahaan = request.form['perusahaan']
            namaLengkap = request.form['nama']
            email = request.form['email']
            telpone = request.form['telpone']
            alamat = request.form['alamat']
            
            docCustomer = {
                'id' : id,
                'perusahaan' : perusahaan,
                'namaLengkap' : namaLengkap,
                'email' : email,
                'telpone' : telpone,
                'alamat' : alamat
            }
            
            db.data_customer.insert_one(docCustomer)
            return redirect(url_for('customer'))
        
        return render_template('form_customer.html', action="tambah")
    elif page == 'pesanan':
        if request.method == 'POST':
            id = generateID(4)
            dataPesanana = list(db.data_pesanan.find({}, {'_id' : False}))
            for data in dataPesanana:
                for data in dataPesanana:
                    if (id == data['id']):
                        id = generateID(4)
                        continue 
            tipe = request.form['tipe']
            kuantitas = request.form['kuantitas']
            namaPenerima = request.form['namaPenerima']
            perusahaan = request.form['perusahaan']
            alamat = request.form['alamat']
            harga = request.form['harga']
            metodePembayaran = request.form['metodePembayaran']
            
            docPesanan = {
                'id': id,
                'tanggal': tanggal,
                'jam' : jam, 
                'tipe' : tipe,
                'kuantitas' : kuantitas,
                'namaPenerima' : namaPenerima,
                'perusahaan' : perusahaan,
                'alamat' : alamat,
                'metodePembayaran' : metodePembayaran,
            }
            db.data_pesanan.insert_one(docPesanan)
            
            docPemasukan = {
                'id': id,
                'tanggal': tanggal,
                'jam' : jam, 
                'tipe' : tipe,
                'kuantitas' : kuantitas,
                'harga' : harga,
                'metodePembayaran' : metodePembayaran,
                'tipePemasukan' : "Penjualan"
            }
            db.data_pendapatan.insert_one(docPemasukan)
            return redirect(url_for('pesanan'))
        
        return render_template('form_pesanan.html', action="tambah")
    elif page == 'sewa':
        if request.method == 'POST':
            id = generateID(4)
            dataSewa = list(db.data_sewa.find({}, {'_id' : False}))
            for data in dataSewa:
                for data in dataSewa:
                    if (id == data['id']):
                        id = generateID(4)
                        continue     
            tipe = request.form['tipe']
            kuantitas = request.form['kuantitas']
            namaPic = request.form['namaPic']
            perusahaan = request.form['perusahaan']
            alamat = request.form['alamat']
            harga = request.form['harga']
            metodePembayaran = request.form['metodePembayaran']
            durasiSewa = request.form['durasiSewa']
            
            docSewa = {
                'id': id,
                'tanggal': tanggal,
                'jam' : jam, 
                'tipe' : tipe,
                'kuantitas' : kuantitas,
                'namaPic' : namaPic,
                'perusahaan' : perusahaan,
                'alamat' : alamat,
                'durasiSewa': durasiSewa,
                'metodePembayaran' : metodePembayaran,
            }
            db.data_sewa.insert_one(docSewa)
            docPemasukan = {
                'id': id,
                'tanggal': tanggal,
                'jam' : jam, 
                'tipe' : tipe,
                'kuantitas' : kuantitas,
                'harga' : harga,
                'metodePembayaran' : metodePembayaran,
                'tipePemasukan' : "Penyewaan"
            }
            db.data_pendapatan.insert_one(docPemasukan)
            return redirect(url_for('sewa'))
        
        return render_template('form_sewa.html', action="tambah")
    elif page == 'produk':
        if request.method == 'POST':
            id = generateID(4)
            dataProduk = list(db.data_produk.find({}, {'_id' : False}))
            for data in dataProduk:
                for data in dataProduk:
                    if (id == data['id']):
                        id = generateID(4)
                        continue   
            foto = request.files['foto']
            merk = request.form['merk']
            tipe = request.form['tipe']
            hargaJual = request.form['hargaJual']
            hargaSewa = request.form['hargaSewa']
            deskripsi = request.form['deskripsi']
            
            if foto :
                filename = secure_filename(foto.filename)
                extension = filename.split(".")[-1]
                file = tipe + "." + extension
                filePath = f'static/assets/img/produk/{tipe}.{extension}'
                foto.save(filePath)
            
            docProduk = {
                'id': id,
                'foto' : file,
                'merk' : merk,
                'tipe' : tipe,
                'hargaJual' : hargaJual,
                'hargaSewa' : hargaSewa,
                'deskripsi' : deskripsi
            }
            db.data_produk.insert_one(docProduk)
            
            return redirect(url_for('produk'))
        return render_template('form_produk.html', action="tambah")
   
@app.route("/get_data/<page>", methods=['GET'])
def get_data(page):
    if page == 'dashboard':
        dataPendapatan = list(db.data_pendapatan.find({}, {'_id' : False}))      
        return jsonify({"dataPendapatan":dataPendapatan, "tanggal": tanggal, "hari": hari, "bulan": bulan, "tahun": tahun})
    elif page == 'karyawan':
        dataKaryawan = list(db.data_karyawan.find({}, {'_id' : False}))
        return jsonify({"dataKaryawan":dataKaryawan})
    elif page == 'customer':
        dataCustomer = list(db.data_customer.find({}, {'_id' : False}))
        return jsonify({"dataCustomer":dataCustomer})    
    elif page == 'pesanan':
        dataPesanana = list(db.data_pesanan.find({}, {'_id' : False}))
        return jsonify({"dataPesanana":dataPesanana})
    elif page == 'sewa':
        dataSewa = list(db.data_sewa.find({}, {'_id' : False}))
        return jsonify({"dataSewa":dataSewa})
    elif page == 'pendapatan':
        dataPendapatan = list(db.data_pendapatan.find({}, {'_id' : False}))      
        return jsonify({"dataPendapatan":dataPendapatan})
    elif page == "chart":
        dataPendapatan = list(db.data_pendapatan.find({}, {'_id' : False}))      
        return jsonify({"dataPendapatan":dataPendapatan, "tanggal": tanggal, "hari": hari, "bulan": bulan, "tahun": tahun})
    elif page == 'produk':
        dataProduk = list(db.data_produk.find({}, {'_id' : False}))      
        return jsonify({"dataProduk":dataProduk})

@app.route('/delete_data/<page>', methods=['POST'])
def delete_data(page):
    if page == "karyawan":
        id = request.form['id']
        db.data_karyawan.delete_one({'id': id})
        return jsonify({'msg': 'Data karyawan berhasil dihapus!'})
    elif page == "customer":
        id = request.form['id']
        db.data_customer.delete_one({'id': id})
        return jsonify({'msg': 'Data customer berhasil dihapus!'})
    elif page == "pesanan":
        id = request.form['id']
        db.data_pesanan.delete_one({'id': id})
        db.data_pendapatan.delete_one({'id': id})
        return jsonify({'msg': 'Data pesanan berhasil dihapus!'})
    elif page == "sewa":
        id = request.form['id']
        db.data_sewa.delete_one({'id': id})
        db.data_pendapatan.delete_one({'id': id})
        return jsonify({'msg': 'Data sewa berhasil dihapus!'})
    elif page == "produk":
        id = request.form['id']
        dataProduk = list(db.data_produk.find({"id" : id}, {'_id' : False}))
        file_path = 'static/assets/img/produk/' + dataProduk[0]['foto']
        if os.path.exists(file_path):
            os.remove(file_path)
        db.data_produk.delete_one({'id': id})
        return jsonify({'msg': 'Data produk berhasil dihapus!'})
    
@app.route("/edit_data/form/<page>/<id>", methods=['GET', 'POST'])
def edit_data(page, id):
    if page == 'karyawan':
        if request.method == 'POST':
            id = request.form['id']
            nik = request.form['nik']
            namaLengkap = request.form['nama']
            posisi = request.form['posisi']
            email = request.form['email']
            telpone = request.form['telpone']
            gaji = request.form['gaji']
            
            docKaryawan = {
                'nik' : nik,
                'namaLengkap' : namaLengkap,
                'posisi' : posisi,
                'email' : email,
                'telpone' : telpone,
                'gaji' : gaji,
            }
            
            db.data_karyawan.update_one({'id': id}, {'$set':docKaryawan})
            return redirect(url_for('karyawan'))
        
        dataKaryawan = list(db.data_karyawan.find({"id" : id}, {'_id' : False}))   
        return render_template('form_karyawan.html', dataKaryawan=dataKaryawan, action="edit")
    elif page == 'customer':
        if request.method == 'POST':
            id = request.form['id']
            perusahaan = request.form['perusahaan']
            namaLengkap = request.form['nama']
            email = request.form['email']
            telpone = request.form['telpone']
            alamat = request.form['alamat']
            
            docCustomer = {
                'id' : id,
                'perusahaan' : perusahaan,
                'namaLengkap' : namaLengkap,
                'email' : email,
                'telpone' : telpone,
                'alamat' : alamat
            }
            
            db.data_customer.update_one({'id': id}, {'$set':docCustomer})
            return redirect(url_for('customer'))
        
        dataCustomer = list(db.data_customer.find({"id" : id}, {'_id' : False}))   
        return render_template('form_customer.html', dataCustomer=dataCustomer, action="edit")
    elif page == 'pesanan':
        if request.method == 'POST':
            id = request.form['id']
            tipe = request.form['tipe']
            kuantitas = request.form['kuantitas']
            namaPenerima = request.form['namaPenerima']
            perusahaan = request.form['perusahaan']
            alamat = request.form['alamat']
            harga = request.form['harga']
            metodePembayaran = request.form['metodePembayaran']

            docPes = {
                'id': id,
                'tanggal': tanggal,
                'jam' : jam, 
                'tipe' : tipe,
                'kuantitas' : kuantitas,
                'namaPenerima' : namaPenerima,
                'perusahaan' : perusahaan,
                'alamat' : alamat,
                'metodePembayaran' : metodePembayaran,
            }
            db.data_pesanan.update_one({'id': id}, {'$set':docPes})
            docPemasukan = {
                'id': id,
                'tanggal': tanggal,
                'jam' : jam, 
                'tipe' : tipe,
                'kuantitas' : kuantitas,
                'harga' : harga,
                'metodePembayaran' : metodePembayaran,
                'tipePemasukan' : "pesanan"
            }
            db.data_pendapatan.update_one({'id': id}, {'$set':docPemasukan})
            return redirect(url_for('pesanan'))
        
        dataPesanan = list(db.data_pesanan.find({"id" : id}, {'_id' : False}))
        dataPendapatan = list(db.data_pendapatan.find({"id" : id}, {'_id' : False}))
        return render_template('form_pesanan.html', dataPesanan=dataPesanan, dataPendapatan=dataPendapatan, action="edit")
    elif page == 'sewa':
        if request.method == 'POST':
            id = request.form['id']
            tipe = request.form['tipe']
            kuantitas = request.form['kuantitas']
            namaPic = request.form['namaPic']
            perusahaan = request.form['perusahaan']
            alamat = request.form['alamat']
            harga = request.form['harga']
            metodePembayaran = request.form['metodePembayaran']
            durasiSewa = request.form['durasiSewa']
            
            docSewa = {
                'id': id,
                'tanggal': tanggal,
                'jam' : jam, 
                'tipe' : tipe,
                'kuantitas' : kuantitas,
                'namaPic' : namaPic,
                'perusahaan' : perusahaan,
                'alamat' : alamat,
                'durasiSewa': durasiSewa,
                'metodePembayaran' : metodePembayaran,
            }
            db.data_sewa.update_one({'id': id}, {'$set':docSewa})
            docPemasukan = {
                'id': id,
                'tanggal': tanggal,
                'jam' : jam, 
                'tipe' : tipe,
                'kuantitas' : kuantitas,
                'harga' : harga,
                'metodePembayaran' : metodePembayaran,
                'tipePemasukan' : "Penyewaan"
            }
            db.data_pendapatan.update_one({'id': id}, {'$set':docPemasukan})
            return redirect(url_for('sewa'))
        
        dataSewa = list(db.data_sewa.find({"id" : id}, {'_id' : False}))
        dataPendapatan = list(db.data_pendapatan.find({"id" : id}, {'_id' : False}))
        return render_template('form_sewa.html', dataSewa=dataSewa, dataPendapatan=dataPendapatan, action="edit")
    elif page == 'produk':
        if request.method == 'POST':
            id = request.form['id'] 
            foto = request.files['foto']
            merk = request.form['merk']
            tipe = request.form['tipe']
            hargaJual = request.form['hargaJual']
            hargaSewa = request.form['hargaSewa']
            deskripsi = request.form['deskripsi']
            
            dataProduk = list(db.data_produk.find({"id" : id}, {'_id' : False}))
            
            if foto :
                filename = secure_filename(foto.filename)
                extension = filename.split(".")[-1]
                file = tipe + "." + extension
                filePath = f'static/assets/img/produk/{tipe}.{extension}'
                foto.save(filePath)
            else:
                file = dataProduk[0]['foto']
                
            docProduk = {
                'id': id,
                'foto' : file,
                'merk' : merk,
                'tipe' : tipe,
                'hargaJual' : hargaJual,
                'hargaSewa' : hargaSewa,
                'deskripsi' : deskripsi
            }
            
            db.data_produk.update_one({'id': id}, {'$set':docProduk})
            return redirect(url_for('produk'))
        
        dataProduk = list(db.data_produk.find({"id" : id}, {'_id' : False}))
        return render_template('form_produk.html', dataProduk=dataProduk, action="edit")

@app.route("/search_data/<page>", methods=['POST'])
def search_data(page):
    if page == "karyawan":
        query = request.form.get('query')
        dataKaryawan = list(db.data_karyawan.find({'$or': [{'nik': {'$regex': query, '$options': 'i'}}, {'namaLengkap': {'$regex': query, '$options': 'i'}}, {'posisi': {'$regex': query, '$options': 'i'}}, {'email': {'$regex': query, '$options': 'i'}}, {'telpone': {'$regex': query, '$options': 'i'}}, {'gaji': {'$regex': query, '$options': 'i'}}]}, {'_id': False}))
        return jsonify({'dataKaryawan': dataKaryawan})
    elif page == "customer":     
        query = request.form.get('query')
        dataCustomer = list(db.data_customer.find({'$or': [{'id': {'$regex': query, '$options': 'i'}}, {'perusahaan': {'$regex': query, '$options': 'i'}}, {'namaLengkap': {'$regex': query, '$options': 'i'}}, {'email': {'$regex': query, '$options': 'i'}}, {'telpone': {'$regex': query, '$options': 'i'}}, {'alamat': {'$regex': query, '$options': 'i'}}]}, {'_id': False}))
        return jsonify({'dataCustomer': dataCustomer})
    elif page == "pesanan":        
        query = request.form.get('query')
        dataPesanan = list(db.data_pesanan.find({'$or': [{'id': {'$regex': query, '$options': 'i'}}, {'tanggal': {'$regex': query, '$options': 'i'}}, {'jam': {'$regex': query, '$options': 'i'}}, {'tipe': {'$regex': query, '$options': 'i'}}, {'kuantitas': {'$regex': query, '$options': 'i'}}, {'namaPenerima': {'$regex': query, '$options': 'i'}}, {'perusahaan': {'$regex': query, '$options': 'i'}}, {'alamat': {'$regex': query, '$options': 'i'}}, {'metodePembayaran': {'$regex': query, '$options': 'i'}}]}, {'_id': False}))
        return jsonify({'dataPesanan': dataPesanan})
    elif page == "sewa":        
        query = request.form.get('query')
        dataSewa = list(db.data_sewa.find({'$or': [{'id': {'$regex': query, '$options': 'i'}}, {'tanggal': {'$regex': query, '$options': 'i'}}, {'jam': {'$regex': query, '$options': 'i'}}, {'tipe': {'$regex': query, '$options': 'i'}}, {'kuantitas': {'$regex': query, '$options': 'i'}}, {'namaPic': {'$regex': query, '$options': 'i'}}, {'perusahaan': {'$regex': query, '$options': 'i'}}, {'alamat': {'$regex': query, '$options': 'i'}}, {'durasiSewa': {'$regex': query, '$options': 'i'}}, {'metodePembayaran': {'$regex': query, '$options': 'i'}}]}, {'_id': False}))
        return jsonify({'dataSewa': dataSewa})
    elif page == "pendapatan":        
        query = request.form.get('query')
        dataPendapatan = list(db.data_pendapatan.find({'$or': [{'id': {'$regex': query, '$options': 'i'}}, {'tanggal': {'$regex': query, '$options': 'i'}}, {'jam': {'$regex': query, '$options': 'i'}}, {'tipe': {'$regex': query, '$options': 'i'}}, {'kuantitas': {'$regex': query, '$options': 'i'}}, {'harga': {'$regex': query, '$options': 'i'}}, {'metodePembayaran': {'$regex': query, '$options': 'i'}}, {'tipePemasukan': {'$regex': query, '$options': 'i'}}]}, {'_id': False}))
        return jsonify({'dataPendapatan': dataPendapatan})
    elif page == "produk":     
        query = request.form.get('query')
        dataProduk = list(db.data_produk.find({'$or': [{'id': {'$regex': query, '$options': 'i'}}, {'merk': {'$regex': query, '$options': 'i'}}, {'tipe': {'$regex': query, '$options': 'i'}}, {'hargaJual': {'$regex': query, '$options': 'i'}}, {'hargaSewa': {'$regex': query, '$options': 'i'}}, {'deskripsi': {'$regex': query, '$options': 'i'}}]}, {'_id': False}))
        return jsonify({'dataProduk': dataProduk})
    
@app.route("/sign_in")
def sign_in():
    return render_template('signin.html')

@app.route("/sign_in/check", methods=["POST"])
def sign_in_check():
    username = request.form["username"]
    password = request.form["password"]
    pw_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
    result = db.users.find_one(
        {
            "username": username,
            "password": pw_hash,
        }
        
    )

    if result:
        payload = {
            "id": username,
            "exp": datetime.utcnow() + timedelta(hours=8)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

        return jsonify(
            {
                "result": "success",
                "token": token,
            }
        )
    else:
        return jsonify(
            {
                "result": "fail",
                "msg": "Username atau password salah!",
            }
        )

@app.route("/sign_up")
def sign_up():
    return render_template('signup.html')

@app.route("/sign_up/save", methods=["POST"])
def sign_up_save():
    username = request.form['username']
    password = request.form['password']
    akun     = request.form['akun']
    password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    doc = {
        "username": username,                               
        "password": password_hash,                                  
        "akun": akun,
        "profileName" : username, 
        "profile" : "",                                       
        "profilePict": "assets/img/profile/profile_placeholder.jpeg"                                        
    }
    exists = bool(db.users.find_one({"username": username, "akun" : akun}))
    if exists == False:
        db.users.insert_one(doc)
    return jsonify({'result': 'success', 'exists': exists})

@app.route("/logout", methods=["DELETE"])
def logout():
    try:
        response = {"message": "Token berhasil dihapus"}
        resp = make_response(jsonify(response))
        resp.set_cookie("mytoken", "", expires=0, path="/")
        return resp
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        response = {"message": "Token tidak valid"}
        return jsonify(response), 401

# Halaman FrontEnd
@app.route("/index", methods=["GET"])
def helloF():
    return render_template('index.html') 

@app.route("/product-sewaprinter", methods=["GET"])
def productsewaprinter():
    return render_template('product-sewaprinter.html') 

@app.route("/product-jualprinter", methods=["GET"])
def productjualprinter():
    return render_template('product-jualprinter.html') 
@app.route("/product-jualtoner", methods=["GET"])
def productjualtoner():
    return render_template('product-jualtoner.html') 

@app.route("/about", methods=["GET"])
def aboutF():
    return render_template('about.html') 

@app.route("/services", methods=["GET"])
def servicesF():
    return render_template('services.html') 

@app.route("/contact", methods=["GET"])
def contactF():
    return render_template('contact.html') 

@app.route("/cart", methods=["GET"])
def cartF():
    return render_template('cart.html') 

@app.route("/payment", methods=["GET"])
def paymentF():
    return render_template('payment.html') 



if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)
    