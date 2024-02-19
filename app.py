from flask import jsonify
from flask import Flask
from flask import json
from flask import request
from flask_cors import CORS
from datetime import date
import mysql.connector
import json
from datetime import datetime
import pandas as pd


app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

db_config = {
    'host': 'localhost',
    'user': 'n1569631_admin',
    'password': 'Ohno210500!',
    'database': 'n1569631_pickmyrace'
}

db_config_2 = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
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
    try:
        global db_config
        data = request.json
        data_list = data['data']
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute("DELETE FROM data_pelari")
        connection.commit()
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
            SELECT data_pelari.bib, data_pelari.firstName,data_pelari.gender,data_pelari.contest,data_pelari.category,
            finish.finishtime,finish.chiptime,finish.overallplace,finish.divisionplace, finish.pace,
            cp1.finishtime AS cp1,
            cp2.finishtime AS cp2,
            cp3.finishtime AS cp3,
            cp4.finishtime AS cp4,
            cp5.finishtime AS cp5,
            cp6.finishtime AS cp6,
            cp7.finishtime AS cp7,
            cp8.finishtime AS cp8,
            cp9.finishtime AS cp9,
            cp10.finishtime AS cp10,
            cp11.finishtime AS cp11,
            cp12.finishtime AS cp12,
            cp13.finishtime AS cp13,
            cp14.finishtime AS cp14,
            cp15.finishtime AS cp15
            FROM data_pelari 
            LEFT JOIN finish ON data_pelari.bib=finish.bib 
            LEFT JOIN cp1 ON data_pelari.bib=cp1.bib 
            LEFT JOIN cp2 ON data_pelari.bib=cp2.bib 
            LEFT JOIN cp3 ON data_pelari.bib=cp3.bib 
            LEFT JOIN cp4 ON data_pelari.bib=cp4.bib
            LEFT JOIN cp5 ON data_pelari.bib=cp5.bib
            LEFT JOIN cp6 ON data_pelari.bib=cp6.bib
            LEFT JOIN cp7 ON data_pelari.bib=cp7.bib
            LEFT JOIN cp8 ON data_pelari.bib=cp8.bib
            LEFT JOIN cp9 ON data_pelari.bib=cp9.bib
            LEFT JOIN cp10 ON data_pelari.bib=cp10.bib
            LEFT JOIN cp11 ON data_pelari.bib=cp11.bib
            LEFT JOIN cp12 ON data_pelari.bib=cp12.bib
            LEFT JOIN cp13 ON data_pelari.bib=cp13.bib
            LEFT JOIN cp14 ON data_pelari.bib=cp14.bib
            LEFT JOIN cp15 ON data_pelari.bib=cp15.bib
        '''

        cursor.execute(query)

        # Mengambil semua hasil query
        results = cursor.fetchall()

        # Menutup kursor dan koneksi
        cursor.close()
        connection.close()

        df = pd.DataFrame.from_dict(results)
        df['count'] = df[['cp1', 'cp2', 'cp3', 'cp4', 'cp5', 'cp6', 'cp7', 'cp8', 'cp9', 'cp10','cp11','cp12','cp13','cp14','cp15',]].count(axis=1)
        results_pandas = df.to_dict(orient='records')

        # Inisialisasi dictionary untuk menyimpan nilai unik kolom "contest"
        contest_values = [row['contest'] for row in results]

        # Mengonversi list menjadi set untuk mendapatkan nilai unik
        unique_contests = set(contest_values)
        now = datetime.now()
        dt = now.strftime("%H:%M:%S")
        return jsonify({'status': 'success', 'data': results_pandas,'date':dt ,'list_contest':list(unique_contests)})
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