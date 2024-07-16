from deepface import DeepFace
import cv2
from datetime import datetime
import mysql.connector
import random
import csv
import sys

database = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Hearts13",
    database="facescan_attendance_db"
)

db = database.cursor()

backends = [
    'opencv',
    'ssd',
    'dlib',
    'mtcnn',
    'fastmtcnn',
    'retinaface',
    'mediapipe',
    'yolov8',
    'yunet',
    'centerface',
]

alignment_modes = [True, False]


def show_image(image_path):
    image = cv2.imread(image_path)
    cv2.imshow('Student Image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def addStudent(table_name):
    student_name = input("Enter the full name of the student you want to add: ")
    student_img = input("Enter the student's Face Scan (file name): ")
    show_image(student_img)
    update = f"INSERT INTO `{table_name}` (`Student ID`, `Student Name`, `Student Image`) VALUES (%s, %s, %s)"
    studentID = str(random.randint(1000, 9999))
    values = (studentID, student_name, student_img)
    db.execute(update, values)
    database.commit()
    print(f"Student {student_name} has been added successfully.")


def removeStudent(table_name):
    row_count_b4 = db.rowcount
    student_name = input("Enter the full name of the student you want to remove: ")
    db.execute(f"SELECT `Student ID`, `Student Name` FROM `{table_name}` WHERE `Student Name` = %s", (student_name,))
    results = db.fetchall()
    for student in results:
        print(f"Student ID: {student[0]}, Student Name: {student[1]}")
    student_id = input("Enter the Student ID of the student you want to remove: ")
    if any(str(student[0]) == student_id for student in results):
        confirm = input(f"Do you want to remove the student {student_name} with ID {student_id}? (yes/no): ")
        if confirm.lower() == 'yes':
            db.execute(f"DELETE FROM `{table_name}` WHERE `Student ID` = %s", (student_id,))
            database.commit()
            print(f"Student with ID {student_id} has been removed successfully.")
        else:
            print("Operation cancelled.")
    else:
        print("Invalid Student ID entered.")
    row_count_after = db.rowcount
    if row_count_after < row_count_b4:
        print(f"Student with ID {student_id} has been removed successfully.")
    else:
        print(f"No record found with Student ID {student_id}.")


def Login(table_name, student_name):
    # Find Student's face Scan
    db.execute(f"SELECT `Student Image` FROM `{table_name}` WHERE `Student Name` = %s", (student_name,))
    student_img = db.fetchone()
    if not student_img:
        print(f"No face scan found for {student_name}")
        return
    student_img = student_img[0]
    show_image(student_img)
    # Login
    student_login = input("Enter the file name of your face scan: ")
    show_image(student_login)
    result = DeepFace.verify(
        img1_path=str(student_login),
        img2_path=str(student_img),
        detector_backend=backends[3],
        align=alignment_modes[0],
    )
    current_time = datetime.now().strftime('%H:%M:%S')
    if result.get("verified") == True:
        update = f"UPDATE `{table_name}` SET `Present` = %s, `Absent` = %s, `Time In` = %s WHERE `Student Name` = %s"
        values = (1, 0, current_time, student_name)
        db.execute(update, values)
        database.commit()
        print(f"Student {student_name} has been marked present\n"
              f"Time Recorded: {current_time}\n\n"
              f"Have a great day!")
    else:
        print("Sign in failed! Your face scan does not match the student on file")


def Logout(table_name, student_name):
    # Find Student's face Scan
    db.execute(f"SELECT `Student Image` FROM `{table_name}` WHERE `Student Name` = %s", (student_name,))
    student_img = db.fetchone()
    if not student_img:
        print(f"No face scan found for {student_name}")
        return
    student_img = student_img[0]
    show_image(student_img)
    # Logout
    student_login = input("Enter the file name of your face scan: ")
    show_image(student_login)
    result = DeepFace.verify(
        img1_path=str(student_login),
        img2_path=str(student_img),
        detector_backend=backends[3],
        align=alignment_modes[0],
    )
    current_time = datetime.now().strftime('%H:%M:%S')
    if result.get("verified") == True:
        update = f"UPDATE `{table_name}` SET `Time Out` = %s WHERE `Student Name` = %s"
        values = (current_time, student_name)
        db.execute(update, values)
        database.commit()
        print(f"Student {student_name} has been marked out\n"
              f"Time Recorded: {current_time}\n\n"
              f"Have a great day!")
    else:
        print("Sign out failed! Your face scan does not match the student on file")


def export_to_csv(table_name, csv_file_path):
    db.execute(f"SELECT * FROM `{table_name}`")
    rows = db.fetchall()
    columns = [i[0] for i in db.description]
    with open(csv_file_path + ".csv", 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(columns)
        writer.writerows(rows)
    print(f"The attendance from {table_name} has been exported to {csv_file_path}")


def main():
    student_name = input("Enter your full name: ")
    table_name = input("Enter which date you want to access (MM/DD/YYYY): ")

    def menu():
        while True:
            print("\nMenu:")
            print("1. Add Student")
            print("2. Remove Student")
            print("3. Student Login")
            print("4. Sign Out")
            print("5. Export to CSV")
            print("6. Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                addStudent(table_name)
            elif choice == '2':
                removeStudent(table_name)
            elif choice == '3':
                Login(table_name, student_name)
            elif choice == '4':
                Logout(table_name, student_name)
            elif choice == '5':
                csv_file_path = input("Enter the name for the CSV file: ")
                export_to_csv(table_name, csv_file_path)
            elif choice == '6':
                print("Have a nice day!")
                db.close()
                database.close()
                sys.exit()
            else:
                print("Invalid choice. Please enter a number between 1 and 6.")
    menu()

if __name__ == "__main__":
    main()
