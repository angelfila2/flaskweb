from flask import Flask, render_template, request
import pandas as pd
import random
import sqlite3
import requests
import openpyxl
from bs4 import BeautifulSoup

app = Flask(  # Create a flask app
  __name__,
  template_folder='templates',  # Name of html file folder
  static_folder='static'  # Name of directory for static files
)


@app.route('/')
def index():
  return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
  if request.method == 'POST':
    # get the uploaded file
    file = request.files['file']

    # read the Excel file using pandas
    df = pd.read_excel(file)

    # create a database connection
    conn = sqlite3.connect('data.db')

    # save the data to the database
    df.to_sql('data', conn, if_exists='replace')

    # close the database connection
    conn.close()

    return 'File uploaded successfully and data saved to database!'

  return render_template('upload.html')


@app.route('/uploadRegister', methods=['GET', 'POST'])
def upload_file_register():
  if request.method == 'POST':
    # get the uploaded file
    file = request.files['file']

    # read the Excel file using pandas
    df = pd.read_excel(file)

    # create a database connection
    conn = sqlite3.connect('data.db')

    # save the data to the database
    df.to_sql('register', conn, if_exists='replace')

    # close the database connection
    conn.close()

    return 'File uploaded successfully and data saved to database!'

  return render_template('register.html')


@app.route('/data')
def show_data():
  conn = sqlite3.connect('data.db')
  c = conn.cursor()
  c.execute("SELECT * FROM data")
  # c.execute("SELECT * FROM data where Type='Short Courses/Workshops'")
  data = c.fetchall()
  conn.close()
  return render_template('data.html', data=data)


@app.route('/showTable')
def showTable():
  conn = sqlite3.connect('data.db')
  c = conn.cursor()
  c.execute("SELECT name FROM sqlite_master WHERE type='table'")
  table_names = c.fetchall()

  table_data = []
  for table in table_names:
    c.execute(f"PRAGMA table_info({table[0]})")
    columns = c.fetchall()
    table_data.append((table[0], columns))

  conn.close()
  return render_template('showTable.html', data=table_data)


@app.route('/createTable')
def create_table():
  conn = sqlite3.connect('data.db')
  c = conn.cursor()
  c.execute('''CREATE TABLE registeredParticipants
                 (formId INTEGER PRIMARY KEY,
                 course_code TEXT,
                 email TEXT,
                 sentOrNot INTEGER)''')
  conn.commit()
  conn.close()
  return 'Table created successfully'


@app.route('/available')
def availableCourses():
  url = 'https://www2.rp.edu.sg/psc/public/EMPLOYEE/SA/c/N_FLUID_MENU.N_AD_CET_NONCRT_FL.GBL'

  # send a GET request to the URL and retrieve the HTML content
  response = requests.get(url)
  html_content = response.content

  # parse the HTML content with BeautifulSoup
  soup = BeautifulSoup(html_content, 'html.parser')

  # find all elements with class="ps-link" and add their text value to a list
  courses = []
  for link in soup.find_all(class_='ps-link'):
    courses.append(link.text)

  # pass the list of courses to the 'available.html' template
  return render_template('available.html', courses=courses)


if __name__ == "__main__":  # Makes sure this is the main process
  app.run(  # Starts the site
    host='0.0.0.0',  # EStablishes the host, required for repl to detect the site
    port=random.randint(2000,
                        9000)  # Randomly select the port the machine hosts on.
  )

# url = 'https://www2.rp.edu.sg/psc/public/EMPLOYEE/SA/c/N_FLUID_MENU.N_AD_CET_NONCRT_FL.GBL'

# # send a GET request to the URL and retrieve the HTML content
# response = requests.get(url)
# html_content = response.content

# # parse the HTML content with BeautifulSoup
# soup = BeautifulSoup(html_content, 'html.parser')

# # find all elements with class="ps-link" and print their text value
# for link in soup.find_all(class_='ps-link'):
#     print(link.text)
