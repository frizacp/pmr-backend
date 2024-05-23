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

db_config_0= {
    'host': 'localhost',
    'user': 'n1569631_admin',
    'password': 'Ohno210500!',
    'database': 'n1569631_livepmrnew'
}

db_config2 = {
    'host': 'localhost',
    'user': 'n1569631_admin',
    'password': 'Ohno210500!',
    'database': 'n1569631_livepmrnew'
}

db_config = {
    'host': '156.67.213.247',
    'user': 'n1569631_admin',
    'password': 'Ohno210500!',
    'database': 'n1569631_livepmrnew'
}

db_data ='n1569631_pmr_live_'

@app.route('/getinfodevice', methods=['GET'])
def getinfodevice():
    global db_config
    id = request.args.get('id')
    db_config['database'] = 'n1569631_livepmrnew'
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        insert_query = f'SELECT * FROM laptop_info WHERE id = {id}'
        cursor.execute(insert_query)
        results = cursor.fetchall()
        connection.commit()
        cursor.close()
        connection.close()

        now = datetime.now()
        dt = now.strftime("%H:%M:%S")

        return jsonify({'status': 'success', 'data': results,'date':dt})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/geteventdetail', methods=['GET'])
def geteventdetail():
    global db_config
    db_config['database'] = 'n1569631_livepmrnew'
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        insert_query = f'SELECT * FROM event_info'
        cursor.execute(insert_query)
        results = cursor.fetchall()
        connection.commit()
        cursor.close()
        connection.close()

        now = datetime.now()
        dt = now.strftime("%H:%M:%S")

        return jsonify({'status': 'success', 'data': results,'date':dt})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})
    
@app.route('/uploadresult', methods=['POST'])
def upload_result():
    try:
        global db_config
        global db_data
        data = request.json
        data_list = json.loads(data['data'])
        position = data['position']
        race = data['race']
        db_config['database'] = f'{db_data}{race}'
        db_configuration = db_config
        connection = mysql.connector.connect(**db_configuration)
        cursor = connection.cursor()

        bib_numbers = [entry['Bib #'] for entry in data_list]
        finishing_times = [entry['Finishing Time'] for entry in data_list]
        chip_times = [entry['Chip Time'] for entry in data_list]
        overall_places = [entry['Overall Place'] for entry in data_list]
        division_places = [entry['Division Place'] for entry in data_list]
        paces_per_kilometer = [entry['Pace per kilometer'] for entry in data_list]
        change_date = datetime.now().strftime("%H:%M:%S")

        # Menambahkan kolom 'code' dan menggabungkan nilai race dan bib_numbers
        codes = [race +"_"+ str(bib_number) for bib_number in bib_numbers]

        insert_query = f"INSERT IGNORE INTO {position} (`bib`, `finishtime`, `chiptime`, `overallplace`, `divisionplace`, `pace`, `race`, `code`, `change_date`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

        values = [(bib_number, finishing_time, chip_time, overall_place, division_place, pace_per_kilometer, race, code, change_date) 
                for bib_number, finishing_time, chip_time, overall_place, division_place, pace_per_kilometer, code 
                in zip(bib_numbers, finishing_times, chip_times, overall_places, division_places, paces_per_kilometer, codes)]

        cursor.executemany(insert_query, values)

        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({'status': 'success', 'date': change_date})
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


@app.route('/drop', methods=['GET'])
def drop_db():
    try:
        global db_config
        global db_data
        
        type = request.args.get('type')
        race = request.args.get('race')
        db_config['database'] = f'{db_data}{race}'
        
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        insert_query = f"DELETE FROM {type} WHERE race = '{race}'"
        cursor.execute(insert_query)

        connection.commit()
        now = datetime.now()
        dt = now.strftime("%H:%M:%S")
        cursor.close()
        connection.close()
        return jsonify({'status': 'success','date':dt})
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


@app.route('/uploadpeserta', methods=['POST'])
def uploadpeserta():
    try:
        global db_config
        global db_data
        data = request.json
        race = request.args.get('race')
        data_list = data['data']
        db_config['database'] = f'{db_data}{race}'
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Hapus semua data peserta untuk perlombaan yang diberikan sebelumnya
        cursor.execute("DELETE FROM info_peserta WHERE race = %s", (race,))
        connection.commit()

        # Ekstrak semua nilai peserta ke dalam tupel
        values = [(entry['bib'],(str(entry['race'])+"_"+str(entry['bib'])), entry['firstName'], entry['lastName'], entry['gender'], entry['type'], 
                   entry['dob'], entry['age'], entry['contest'], entry['category'], entry['race'], 
                   entry['chipcode'],(str(entry['contest'])+" "+str(entry['category']))) for entry in data_list]

        # Masukkan semua nilai peserta ke dalam tabel info_peserta
        insert_query = "INSERT IGNORE INTO info_peserta (`bib`,`code`, `firstName`, `lastName`, `gender`,`type`,`dob`,`age`,`contest`,`category`,`race`,`chipcode`,`contest_category`) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.executemany(insert_query, values)
        connection.commit()

        cursor.close()
        connection.close()
        now = datetime.now()
        dt = now.strftime("%H:%M:%S")

        return jsonify({'status': 'success', 'data': data_list, 'date': dt})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


@app.route('/getdata_tagcheck', methods=['GET'])
def get_datatag():
    global db_config
    global db_data
    race = request.args.get('race')
    db_config['database'] = f'{db_data}{race}'
    try:
        # Membuat koneksi ke database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        query = f"SELECT info_peserta.race, info_peserta.chipcode, finish.finishtime, finish.chiptime, finish.pace FROM info_peserta LEFT JOIN finish ON info_peserta.bib=finish.bib WHERE info_peserta.race ='{race}'"

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
    global db_data
    race = request.args.get('race')
    null = request.args.get('null')
    db_config['database'] = f'{db_data}{race}'
    try:
        # Membuat koneksi ke database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        if null == 'true':
            query = f"SELECT info_peserta.bib, info_peserta.lastName, info_peserta.gender, info_peserta.contest_category, info_peserta.race, COALESCE(finish.finishtime, '') AS finishtime, COALESCE(finish.overallplace, 9999) AS overallplace, COALESCE(finish.divisionplace, '') AS divisionplace, COALESCE(finish.pace, '') AS pace, COALESCE(cp1.finishtime, '') AS cp1, COALESCE(cp2.finishtime, '') AS cp2, COALESCE(cp3.finishtime, '') AS cp3 FROM info_peserta LEFT JOIN finish ON info_peserta.bib=finish.bib LEFT JOIN cp1 ON info_peserta.bib=cp1.bib LEFT JOIN cp2 ON info_peserta.bib=cp2.bib LEFT JOIN cp3 ON info_peserta.bib=cp3.bib WHERE info_peserta.race = '{race}'"
        else:
            query = f"SELECT info_peserta.bib, info_peserta.lastName,info_peserta.gender,info_peserta.contest_category,info_peserta.race, finish.finishtime,finish.chiptime,finish.overallplace,finish.divisionplace, finish.pace, cp1.finishtime AS cp1, cp2.finishtime AS cp2, cp3.finishtime AS cp3 FROM info_peserta LEFT JOIN finish ON info_peserta.bib=finish.bib LEFT JOIN cp1 ON info_peserta.bib=cp1.bib LEFT JOIN cp2 ON info_peserta.bib=cp2.bib LEFT JOIN cp3 ON info_peserta.bib=cp3.bib WHERE info_peserta.race = '{race}' AND finish.overallplace IS NOT NULL"

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
    
    

@app.route('/getdata', methods=['GET'])
def get_data():
    global db_config
    global db_data
    type = request.args.get('type')
    race = request.args.get('race')
    db_config['database'] = f'{db_data}{race}'
    try:
        # Membuat koneksi ke database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        query = f"SELECT * FROM {type} WHERE race ='{race}'"
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