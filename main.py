from flask import Flask, render_template, request, redirect, url_for

import mysql.connector

app = Flask(__name__)

@app.route('/')
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

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="121940",
        database="dent"
    )

@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        Patient_ID = request.form['id']
        name = request.form['name']
        Date_of_Birth = request.form['date_of_birth']
        Medical_History = request.form['Medical_History']
        Allergies = request.form['allergy']
        Medication = request.form['medication_taken']
        Other_specialist = request.form['last specialist']
        Symptoms_and_Pain = request.form['symptoms']
        Previous_Dental_Procedures = request.form['previous_dental_procedures']
        Bad_Habits = request.form['bad_habitats']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Patients (Patient_ID, Name, Date_of_Birth, Medical_History, Allergies, Medications, Other_specialists, Symptoms_and_Pain, Previous_Dental_Procedures, Bad_Habits) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (Patient_ID, name, Date_of_Birth, Medical_History, Allergies, Medication, Other_specialist, Symptoms_and_Pain, Previous_Dental_Procedures, Bad_Habits))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_patient.html')


@app.route('/add_doctor', methods=['GET', 'POST'])
def add_doctor():
    if request.method == 'POST':
        name = request.form['name']
        # Добавьте другие поля, если нужно

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Doctors (name) VALUES (%s)", (name,))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_doctor.html')

@app.route('/add_appointment', methods=['GET', 'POST'])
def add_appointment():
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        doctor_id = request.form['doctor_id']
        date = request.form['date']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Appointments (patient_id, doctor_id, date) VALUES (%s, %s, %s)", (patient_id, doctor_id, date))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_appointment.html')

if __name__ == '__main__':
    app.run(debug=True)
