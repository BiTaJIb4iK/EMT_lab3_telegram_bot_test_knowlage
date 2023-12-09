from sqlite3 import Cursor, Connection
import sqlite3
from datetime import timedelta, datetime


def createConnectionToDatabase() -> Connection:
    return sqlite3.connect("test.db")

#better not to use this function often
def setUpDataBaseDefault():
    createDataBaseTables()
    fillQuestions()

def createDataBaseTables():
    con = createConnectionToDatabase()
    cur = con.cursor()

    cur.executescript("""

-- Create the "User" table
CREATE TABLE IF NOT EXISTS User (
    user_id INT PRIMARY KEY,
    user_name char(129),
    user_register_date DATE,
    user_admin BOOLEAN
);

-- Create the "Question" table with foreign keys
CREATE TABLE IF NOT EXISTS Questions (
    ques_id INT,
    right_aswer INT,
    question char(500),
    answer1 char(100),
    answer2 char(100),
    answer3 char(100),
    answer4 char(100)
);

-- Create the "Quiz" table with foreign keys
CREATE TABLE IF NOT EXISTS Quiz (
    quiz_id INT,
    user_id int,
    quiz_date Date,
    FOREIGN KEY (user_id) REFERENCES User(user_id)
);

-- Create the "Quiz" table with foreign keys
CREATE TABLE IF NOT EXISTS Quiz_questions (
    quiz_id INT,
    ques_id INT,
    isRightAnswer BOOLEAN,
    FOREIGN KEY (quiz_id) REFERENCES Quiz(Quiz_id),
    FOREIGN KEY (ques_id) REFERENCES Questions(ques_id)
);

""")

    con.commit()

    cur.close()
    con.close()

def fillQuestions():
    con = createConnectionToDatabase()
    cur = con.cursor()

    cur.execute("delete from Questions")
    con.commit()
    
    def_questions = [
        (1, 1, "1 + 1", "2", "4", "3", "5"),
        (2, 2, "What is the capital of France?", "Berlin", "Paris", "Madrid", "Rome"),
        (3, 3, "How many continents are there?", "5", "6", "7", "8"),
        (4, 3, "Which planet is known as the Red Planet?", "Venus", "Earth", "Mars", "Jupiter"),
        (5, 2, "What is the largest mammal?", "Elephant", "Blue Whale", "Giraffe", "Lion"),
        (6, 2, "What is the powerhouse of the cell?", "Nucleus", "Mitochondria", "Ribosome", "Endoplasmic Reticulum"),
        (7, 1, "What is the square of 9?", "81", "64", "100", "121"),
        (8, 3, "Who wrote 'Romeo and Juliet'?", "Charles Dickens", "Jane Austen", "William Shakespeare", "Mark Twain"),
        (9, 3, "What is the currency of Japan?", "Yuan", "Euro", "Yen", "Dollar"),
        (10, 2, "What is the largest ocean on Earth?", "Indian Ocean", "Pacific Ocean", "Atlantic Ocean", "Arctic Ocean"),
        (11, 1, "How many sides does a triangle have?", "3", "4", "5", "6"),  # Question 11
        (12, 2, "What is the capital of Australia?", "Sydney", "Melbourne", "Canberra", "Perth"),  # Question 12
        (13, 3, "What is the largest desert in the world?", "Gobi Desert", "Sahara Desert", "Antarctica", "Arabian Desert"),  # Question 13
        (14, 2, "Who developed the theory of relativity?", "Isaac Newton", "Albert Einstein", "Galileo Galilei", "Stephen Hawking"),  # Question 14
        (15, 1, "What is the chemical symbol for gold?", "Au", "Ag", "Fe", "Cu")  # Question 15
    ]

    for a in def_questions:
        cur.execute("INSERT INTO Questions VALUES (?, ?, ?, ?, ?, ?, ?)", a)
        con.commit()

    cur.close()
    con.close()




