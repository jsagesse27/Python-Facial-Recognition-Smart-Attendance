# Python Facial Recognition Smart Attendance

This repository implements a Python-based smart attendance system using facial recognition. It uses the DeepFace library for facial recognition and OpenCV for image handling. The application connects to a MySQL database to store and manage attendance records.

## Features

- **Add Student**: Add a new student to the database along with their facial scan.
- **Remove Student**: Remove an existing student from the database.
- **Login**: Students can log in by scanning their faces.
- **Logout**: Students can log out by scanning their faces again.
- **Export to CSV**: Export attendance records to a CSV file.

## Prerequisites

- Python 3.x
- MySQL Database
- Required Python libraries: `deepface`, `opencv-python`, `mysql-connector-python`, `csv`

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/jsagesse27/Python-Facial-Recognition-Smart-Attendance.git
   cd Python-Facial-Recognition-Smart-Attendance
   
2. Install the required Python libraries:

   ```bash
   pip install deepface opencv-python mysql-connector-python

3. Set up your MySQL database:

   - Create a new database called `facescan_attendance_db`.
   - Configure the `host`, `user`, `passwd`, and `database` parameters in `detectFaces.py` to match your MySQL configuration.

## Usage

1. Run the `detectFaces.py` script:

   ```bash
   python detectFaces.py
   ```

2. Follow the prompts to add or remove students, log in or log out, and export attendance data to CSV.

## Files

- `detectFaces.py`: Main script for handling facial recognition and database operations.
- `login-faces/`: Directory containing sample images for facial recognition.
- `stored-faces/`: Directory where student facial scans are stored.
- `Jovens.JPEG` and `test_image.jpg`: Example images for testing.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [DeepFace](https://github.com/serengil/deepface): A lightweight face recognition and facial attribute analysis library for Python.
