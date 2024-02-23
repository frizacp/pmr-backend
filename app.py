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

db_config_9 = {
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

db_config = {
    'host': '156.67.213.247',
    'user': 'n1569631_admintagcheck',
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
            SELECT data_pelari.race, data_pelari.chipcode, finish.finishtime, finish.chiptime, finish.pace
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
            SELECT data_pelari.bib, data_pelari.firstName,data_pelari.gender,data_pelari.contest,
            finish.finishtime,finish.chiptime,finish.overallplace,finish.divisionplace, finish.pace,
            ws1.finishtime AS ws1,
            ws2.finishtime AS ws2,
            ws3.finishtime AS ws3,
            ws4.finishtime AS ws4,
            ws5.finishtime AS ws5,
            ws6.finishtime AS ws6,
            ws7.finishtime AS ws7,
            ws8.finishtime AS ws8,
            ws9.finishtime AS ws9,
            ws10.finishtime AS ws10,
            ws11.finishtime AS ws11,
            ws12.finishtime AS ws12
            FROM data_pelari 
            LEFT JOIN finish ON data_pelari.bib=finish.bib 
            LEFT JOIN ws1 ON data_pelari.bib=ws1.bib 
            LEFT JOIN ws2 ON data_pelari.bib=ws2.bib 
            LEFT JOIN ws3 ON data_pelari.bib=ws3.bib 
            LEFT JOIN ws4 ON data_pelari.bib=ws4.bib
            LEFT JOIN ws5 ON data_pelari.bib=ws5.bib
            LEFT JOIN ws6 ON data_pelari.bib=ws6.bib
            LEFT JOIN ws7 ON data_pelari.bib=ws7.bib
            LEFT JOIN ws8 ON data_pelari.bib=ws8.bib
            LEFT JOIN ws9 ON data_pelari.bib=ws9.bib
            LEFT JOIN ws10 ON data_pelari.bib=ws10.bib
            LEFT JOIN ws11 ON data_pelari.bib=ws11.bib
            LEFT JOIN ws12 ON data_pelari.bib=ws12.bib
        '''

        cursor.execute(query)

        # Mengambil semua hasil query
        results = cursor.fetchall()

        # Menutup kursor dan koneksi
        cursor.close()
        connection.close()

        df = pd.DataFrame.from_dict(results)
        
        df['count'] = df[['ws1', 'ws2', 'ws3', 'ws4', 'ws5', 'ws6', 'ws7', 'ws8', 'ws9', 'ws10','ws11','ws12']].count(axis=1)
        df = df.fillna('')
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

@app.route('/getmobile', methods=['POST'])
def get_mobile():
    global db_config
    try:
        data = request.json
        data_list = data['data']
        def insert_to_table(connection, table, bibNumber, finishtime):
            cursor = connection.cursor()
            # Query untuk memasukkan data ke tabel
            query = f"INSERT IGNORE INTO {table} (bib, finishtime) VALUES (%s, %s)"
            # Eksekusi query dengan parameter yang diberikan
            cursor.execute(query, (bibNumber, finishtime))
            # Commit perubahan ke database
            connection.commit()
            # Tutup kursor
            cursor.close()

        connection = mysql.connector.connect(**db_config)
        tables = ["ws1","ws2","ws3","ws5","ws6","ws8","ws9","ws11"]

        for record in data_list:
            bibNumber = record['bibNumber']
            # Memasukkan data ke masing-masing tabel
            for table in tables:
                finishtime = record.get(table, None)  # Mengambil nilai waktu dari tabel yang sesuai
                if finishtime is not None:
                    insert_to_table(connection, table, bibNumber, finishtime)
        connection.close()
        now = datetime.now()
        dt = now.strftime("%H:%M:%S")

        return jsonify({'status': 'success', 'date':dt})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})



@app.route('/getdummy', methods=['GET'])
def getdummy():
    results = [
    {
      "name": "Baim",
      "bibNumber": 5000,
      "ws2": "00:02:00",
      "ws3": "00:03:00",
      "ws5": "00:05:00",
      "ws6": "00:06:00",
      "ws8": "00:08:00",
      "ws9": "00:09:00",
      "ws11": "00:011:00"
    },
    {
      "name": "Baim A",
      "bibNumber": 5001,
      "ws2": "00:02:01",
      "ws3": "00:03:01",
      "ws5": "00:05:01",
      "ws6": "00:06:01",
      "ws8": "00:08:01",
      "ws9": "00:09:01",
      "ws11": "00:011:01"
    },
    {
      "name": "Baim B",
      "bibNumber": 5002,
      "ws2": "00:02:02",
      "ws3": "00:03:02",
      "ws5": "00:05:02",
      "ws6": "00:06:02",
      "ws8": "00:08:02",
      "ws9": "00:09:02",
      "ws11": "00:011:02"
    },
    {
      "name": "Baim V",
      "bibNumber": 5003,
      "ws2": "00:02:03",
      "ws3": "00:03:03",
      "ws5": "00:05:03",
      "ws6": "00:06:03",
      "ws8": "00:08:03",
      "ws9": "00:09:03",
      "ws11": "00:011:03"
    },
    {
      "name": "Baim PP",
      "bibNumber": 5004,
      "ws2": "00:02:04",
      "ws3": "00:03:04",
      "ws5": "00:05:04",
      "ws6": "00:06:04",
      "ws8": "00:08:04",
      "ws9": "00:09:04",
      "ws11": "00:011:04"
    }
  ]
    return jsonify({'status': 'success', 'data': results})


if __name__ == '__main__':
    app.run(debug=True)