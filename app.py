from flask import jsonify
from flask import Flask
from flask import json
from flask import request
from flask_cors import CORS
from datetime import date
import mysql.connector
import json
from datetime import datetime


app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

db_config = {
    'host': 'localhost',
    'user': 'n1569631_admin',
    'password': 'Ohno210500!',
    'database': 'n1569631_pickmyrace'
}


@app.route('/uploadresult', methods=['POST'])
def upload_result():
    global db_config
    data = request.json
    data_list = json.loads(data['data'])
    type = data['type']

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    for entry in data_list:
        bib_number = entry['Bib #']
        finishing_time = entry['Finishing Time']
        chip_time = entry['Chip Time']
        overall_place = entry['Overall Place']
        divison_place = entry['Division Place']
        pace_per_kilometer = entry['Pace per kilometer']

        
        insert_query = f"INSERT IGNORE INTO {type} (`bib`, `finishtime`,`chiptime`, `overallplace`, `divisionplace`, `pace`) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (bib_number, finishing_time,chip_time,overall_place,divison_place, pace_per_kilometer))

    connection.commit()


    cursor.close()
    connection.close()

    return '200'

@app.route('/drop', methods=['GET'])
def drop_db():
    type = request.args.get('type')
    global db_config

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    insert_query = f"DELETE FROM {type}"
    cursor.execute(insert_query)

    connection.commit()

    cursor.close()
    connection.close()
    return '200'

@app.route('/uploadpeserta', methods=['POST'])
def upload_peserta():
    global db_config
    try:
        data = request.json
        data_list = json.loads(data['data'])

        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        for entry in data_list:
            bib = entry['bib'] 
            firstName = entry['firstName'] 
            lastName = entry['lastName'] 
            gender = entry['gender'] 
            type = entry['type'] 
            dob = entry['dob'] 
            age = entry['age'] 
            contest = entry['contest'] 
            category = entry['category'] 
            race = entry['race'] 
            chipcode = entry['chipcode'] 
            insert_query = f"INSERT IGNORE INTO data_pelari (`bib`, `firstName`, `lastName`, `gender`,`type`,`dob`,`age`,`contest`,`category`,`race`,`chipcode`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(insert_query, (bib,firstName,lastName,gender,type,dob,age,contest,category,race,chipcode))

        connection.commit()

        cursor.close()
        connection.close()
        now = datetime.now()
        dt = now.strftime("%H:%M:%S")

        return jsonify({'status': 'success', 'data': data_list,'date':dt})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/getdata_tagcheck', methods=['GET'])
def get_datatag():
    global db_config
    try:
        # Membuat koneksi ke database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        query = '''
            SELECT data_pelari.chipcode, finish.finishtime, finish.chiptime, finish.pace
            FROM data_pelari
            LEFT JOIN finish ON data_pelari.bib=finish.bib
        '''

        cursor.execute(query)

        # Mengambil semua hasil query
        results = cursor.fetchall()

        # Menutup kursor dan koneksi
        cursor.close()
        connection.close()
        now = datetime.now()
        dt = now.strftime("%H:%M:%S")

        return jsonify({'status': 'success', 'data': results,'date':dt})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/getdata_all', methods=['GET'])
def get_alldata():
    global db_config
    try:
        # Membuat koneksi ke database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        query = '''
            SELECT data_pelari.bib, data_pelari.name,data_pelari.gender,data_pelari.contest,
            finish.finishtime,finish.chiptime,finish.overallplace,finish.divisionplace, finish.pace,
            cp1.finishtime AS cp1,
            cp2.finishtime AS cp2,
            cp3.finishtime AS cp3,
            cp4.finishtime AS cp4
            FROM data_pelari 
            LEFT JOIN finish ON data_pelari.bib=finish.bib 
            LEFT JOIN cp1 ON data_pelari.bib=cp1.bib 
            LEFT JOIN cp2 ON data_pelari.bib=cp2.bib 
            LEFT JOIN cp3 ON data_pelari.bib=cp3.bib 
            LEFT JOIN cp4 ON data_pelari.bib=cp4.bib;
        '''

        cursor.execute(query)

        # Mengambil semua hasil query
        results = cursor.fetchall()

        # Menutup kursor dan koneksi
        cursor.close()
        connection.close()
        now = datetime.now()
        dt = now.strftime("%H:%M:%S")
        # Inisialisasi dictionary untuk menyimpan nilai unik kolom "contest"
        contest_values = [row['contest'] for row in results]

        # Mengonversi list menjadi set untuk mendapatkan nilai unik
        unique_contests = set(contest_values)

        return jsonify({'status': 'success', 'data': results,'date':dt ,'list_contest':list(unique_contests)})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


@app.route('/getdata', methods=['GET'])
def get_data():
    global db_config
    type = request.args.get('type')
    try:
        # Membuat koneksi ke database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        query = f"SELECT * FROM {type}"
        cursor.execute(query)

        # Mengambil semua hasil query
        results = cursor.fetchall()

        # Menutup kursor dan koneksi
        cursor.close()
        connection.close()
        now = datetime.now()
        dt = now.strftime("%H:%M:%S")

        return jsonify({'status': 'success', 'data': results,'date':dt})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})
    
@app.route('/getlocation', methods=['GET'])
def get_location():
    global db_config
    try:
        # Membuat koneksi ke database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        query = "SELECT * FROM counter_lokasi"
        cursor.execute(query)

        # Mengambil semua hasil query
        results = cursor.fetchall()

        # Menutup kursor dan koneksi
        cursor.close()
        connection.close()
        now = datetime.now()
        dt = now.strftime("%H:%M:%S")

        return jsonify({'status': 'success', 'data': results,'date':dt})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)