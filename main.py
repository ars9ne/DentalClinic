from flask import Flask, render_template, request, redirect, url_for, jsonify
import random
import mysql.connector

app = Flask(__name__)

@app.route('/patientlist')
def patientlist():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="121940",
        database="dent"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Patients")
    patients = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', patients=patients)




def generate_unique_patient_id(conn):
    cursor = conn.cursor()

    while True:
        # Генерируем рандомный ID в диапазоне, например, от 1 до 1000000.
        random_id = random.randint(1, 1000000)

        # Проверяем, используется ли этот ID.
        cursor.execute("SELECT COUNT(*) FROM Patients WHERE Patient_ID = %s", (random_id,))
        count = cursor.fetchone()[0]

        # Если ID не используется, возвращаем его.
        if count == 0:
            return random_id


@app.route('/')
def mainpage():
    return render_template('mainpage.html')


@app.route('/patientlist')
def index():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="121940",
        database="dent"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Patients")
    patients = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', patients=patients)


db_config = {
    'user': 'root',
    'password': '121940',
    'host': 'localhost',
    'database': 'dent',
    'raise_on_warnings': True
}

@app.route('/delete_patient/<int:patient_id>', methods=['POST'])
def delete_patient(patient_id):
    conn = None
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM patients WHERE Patient_ID = %s", (patient_id,))
        conn.commit()
        cursor.close()
    except Exception as e:
        print(e)
    finally:
        if conn is not None:
            conn.close()
    # Внутри функции delete_patient
    return redirect(url_for('patientlist'))  # Используйте правильное имя маршрута


db_config = {
    'user': 'root',
    'password': '121940',
    'host': 'localhost',
    'database': 'dent',
    'raise_on_warnings': True
}

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="121940",
        database="dent"
    )

@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="121940",
        database="dent"
    )
    if request.method == 'POST':
        Patient_ID = generate_unique_patient_id(conn)
        name = request.form['name']
        Date_of_Birth = request.form.get('date_of_birth')
        Phone_Number = request.form['phone_number']
        Medical_History = request.form['Medical_History']
        Allergies = request.form['allergy']
        Medication = request.form['medication_taken']
        Other_specialist = request.form['last specialist']
        Symptoms_and_Pain = request.form['symptoms']
        Previous_Dental_Procedures = request.form['previous_dental_procedures']
        Bad_Habits = request.form['bad_habitats']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Patients (Patient_ID, Name, Date_of_Birth, Phone_Number, Medical_History, Allergies, Medications, Other_specialists, Symptoms_and_Pain, Previous_Dental_Procedures, Bad_Habits) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (Patient_ID, name, Date_of_Birth, Phone_Number, Medical_History, Allergies, Medication, Other_specialist, Symptoms_and_Pain, Previous_Dental_Procedures, Bad_Habits))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_patient.html')


def delete_patient(patient_id):
    try:
        # Установление соединения с базой данных
        connection = get_db_connection()

        if connection.is_connected():
            # Создание курсора для выполнения SQL-запросов
            cursor = connection.cursor()

            # SQL запрос на удаление пациента
            query = "DELETE FROM patients WHERE Patient_ID = %s"
            cursor.execute(query, (patient_id,))

            # Подтверждение изменений
            connection.commit()

            print(f"Информация о пациенте с ID {patient_id} удалена успешно.")
    finally:
        # Закрытие соединения с базой данных
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Соединение с MySQL закрыто")


@app.route('/add_doctor', methods=['GET', 'POST'])
def add_doctor():
    if request.method == 'POST':
        conn = get_db_connection()
        Doctor_ID = generate_unique_patient_id(conn)
        name = request.form['name']
        specialization = request.form['specialization']
        # Добавьте другие поля, если нужно

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Doctors (Doctor_ID, name, Specialization) VALUES (%s,%s,%s)", (Doctor_ID, name, specialization))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_doctor.html')

@app.route('/online-reg', methods=['GET', 'POST'])
def online_registration():
    if request.method == 'POST':
        conn = get_db_connection() # Установите соединение здесь
        Patient_ID = generate_unique_patient_id(conn)
        name = request.form['name']
        Phone_Number = request.form['phone_number']
        Medical_History = request.form['Medical_History']

        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Patients (Patient_ID, Name, Phone_Number, Medical_History) VALUES (%s, %s, %s, %s)",
            (Patient_ID, name, Phone_Number, Medical_History))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('index'))
    return render_template('online_registration.html')


@app.route('/doctor_list', methods=['GET', 'POST'])
def doctor_list():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="121940",
        database="dent"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM doctors")
    patients = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('doctor_list.html', patients=patients)


@app.route('/add_appointment', methods=['GET', 'POST'])
def add_appointment():
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        patient_id = request.form['patient_id']
        doctor_id = request.form['doctor_id']
        date = request.form['date']
        time = request.form['time']
        cabinet = request.form['cabinet']
        cursor.execute("INSERT INTO Appointments (Patient_ID, Doctor_ID, Date, Time, Cabinet) VALUES (%s, %s, %s, %s, %s)", (patient_id, doctor_id, date, time, cabinet))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('index'))
    else:
        cursor.execute("SELECT * FROM Patients")
        patients = cursor.fetchall()

        cursor.execute("SELECT * FROM Doctors")
        doctors = cursor.fetchall()

        cursor.execute("SELECT * FROM Doctor_Cabinet")
        cabinets = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template('add_appointment.html', patients=patients, doctors=doctors, cabinets=cabinets)

@app.route('/delete_appointment/<int:appointment_id>', methods=['POST'])
def delete_appointment(appointment_id):
    conn = None
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM appointments WHERE Appointment_ID = %s", (appointment_id,))
        conn.commit()
        cursor.close()
    except Exception as e:
        print(e)
    finally:
        if conn is not None:
            conn.close()
    # Внутри функции delete_patient
    return redirect(url_for('appointments_list'))  # Используйте правильное имя маршрута

@app.route('/get_doctors_by_cabinet')
def get_doctors_by_cabinet():
    cabinet_id = request.args.get('cabinet_id')
    day = request.args.get('day')
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT Doctors.Doctor_ID, Name FROM Doctor_Cabinet JOIN Doctors ON Doctor_Cabinet.Doctor_ID = Doctors.Doctor_ID WHERE Doctor_Cabinet_ID = %s AND Day_of_Week = %s",
        (cabinet_id, day))

    doctors = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(doctors)


@app.route('/appointments_list')
def appointments_list():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="121940",
        database="dent"
    )
    cursor = conn.cursor()
    # Обновленный запрос для получения информации о приемах и именах врачей
    cursor.execute("""
        SELECT a.Appointment_ID, d.name, a.Date, a.Time, a.Patient_ID, a.Cabinet
        FROM Appointments AS a
        JOIN Doctors AS d ON a.Doctor_ID = d.Doctor_ID
    """)
    appointments = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('appointments_list.html', appointments=appointments)


@app.route('/add_treatment', methods=['GET', 'POST'])
def add_treatment():
    if request.method == 'POST':
        conn = get_db_connection()
        Treatment_ID = generate_unique_patient_id(conn)
        Description = request.form['Description']
        Appointment_ID = request.form['Appointment']
        Recipe = request.form['Recipe']
        Patient_ID = request.form['Patient_ID']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO treatments (Treatment_ID, Description, Appointment_ID, Recipe, Patient_ID) VALUES (%s,%s,%s,%s,%s)",
            (Treatment_ID, Description, Appointment_ID, Recipe, Patient_ID))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_treatment.html')


@app.route('/get_patient_by_appointment')
def get_patient_by_appointment():
    appointment_id = request.args.get('appointment_id')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT Patient_ID FROM Appointments WHERE Appointment_ID = %s", (appointment_id,))
    patient_id = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return jsonify(patient_id=patient_id)


@app.route('/treatment_list')
def treatment_list():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="121940",
        database="dent"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Treatments")
    treatment = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('treatment_list.html', treatments=treatment)

@app.route('/add_medication', methods=['GET', 'POST'])
def add_medication():
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        treatment_id = request.form['treatment_id']
        medication_info = request.form['medication_info']
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="121940",
            database="dent"
        )
        cursor = conn.cursor()
        cursor.execute("INSERT INTO medication (Patient_ID, Treatment_ID, Medication_info) VALUES (%s, %s, %s)", (patient_id, treatment_id, medication_info))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/view_medication')
    return render_template('add_medication.html')



@app.route('/view_medication')
def view_medication():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="121940",
        database="dent"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM medication")
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('view_medication.html', records=records)


@app.route('/update_patient/<int:patient_id>', methods=['GET', 'POST'])
def update_patient(patient_id):
    # Connect to the database
    db_connection = mysql.connector.connect(**db_config)
    db_cursor = db_connection.cursor()

    if request.method == 'POST':
        # Retrieve form data
        name = request.form['name']
        date_of_birth = request.form['date_of_birth']
        phone_number = request.form['phone_number']
        medical_history = request.form['medical_history']
        allergies = request.form['allergies']
        medications = request.form['medications']
        other_specialists = request.form['other_specialists']
        symptoms_and_pain = request.form['symptoms_and_pain']
        previous_dental_procedures = request.form['previous_dental_procedures']
        bad_habits = request.form['bad_habits']

        # SQL to update patient data
        update_sql = """UPDATE patients SET 
                        Name=%s, Date_of_Birth=%s, Phone_Number=%s, 
                        Medical_History=%s, Allergies=%s, Medications=%s, 
                        Other_Specialists=%s, Symptoms_and_Pain=%s, 
                        Previous_Dental_Procedures=%s, Bad_Habits=%s 
                        WHERE Patient_ID=%s"""
        update_values = (name, date_of_birth, phone_number,
                         medical_history, allergies, medications,
                         other_specialists, symptoms_and_pain,
                         previous_dental_procedures, bad_habits, patient_id)

        # Execute the update query
        db_cursor.execute(update_sql, update_values)
        db_connection.commit()
        db_cursor.close()
        db_connection.close()

        # Redirect to the patient list or display a success message
        return redirect(url_for('patientlist'))

    else:
        # For GET request, fetch patient data to populate the form
        select_sql = "SELECT * FROM patients WHERE Patient_ID = %s"
        db_cursor.execute(select_sql, (patient_id,))
        patient_data = db_cursor.fetchone()
        db_cursor.close()
        db_connection.close()

        # Render the edit patient form with the patient data
        return render_template('edit_patient.html', patient=patient_data)

if __name__ == '__main__':
    app.run(debug=True)


