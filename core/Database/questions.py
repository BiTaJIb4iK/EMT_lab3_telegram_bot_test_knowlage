from sqlite3 import Cursor, Connection
import sqlite3
from datetime import datetime, timedelta
from typing import List, Tuple, Optional

from core.Database.basic import createConnectionToDatabase

def getQuestionsCount() -> int:
    con = createConnectionToDatabase()
    cur = con.cursor()

    cur.execute("SELECT MAX(ques_id) FROM Questions")
    res = cur.fetchone()
    

    max_ques_id = 0

    if res and res[0] is not None:
        max_ques_id = res[0]
        
    cur.close()
    con.close()

    return max_ques_id

def getQuestion(ques_id: int) -> int:
    con = createConnectionToDatabase()
    cur = con.cursor()

    cur.execute(f"SELECT * FROM Questions where ques_id = {ques_id}")
    res = cur.fetchone()

    cur.close()
    con.close()
    return res

def createQuiz(q: List[int], user_id: int):
    con = createConnectionToDatabase()
    cur = con.cursor()

    cur.execute(f"SELECT max(quiz_id) FROM Quiz")
    res = cur.fetchone()
    if res[0] is not None:
        next_id = res[0]+1
    else:
        next_id=0

    today = datetime.today()
    cur.execute("INSERT INTO Quiz VALUES (?, ?, ?)", (next_id, user_id, today.strftime("'%Y-%m-%d'")))
    con.commit()
    

    for a in q:
        cur.execute(f"Insert into Quiz_questions values(?, ?, ?)", (next_id, a, False))
        con.commit()

    cur.close()
    con.close()

    return next_id

def getQuizQuestion(quiz_id: int, questionIndex: int):
    con = createConnectionToDatabase()
    cur = con.cursor()

    cur.execute(f"SELECT * FROM Questions where ques_id in (select ques_id from Quiz_questions where quiz_id = ?)", (quiz_id,))
    res = cur.fetchall()

    cur.close()
    con.close()
    
    return res[questionIndex]

def updateToRightAnswer(quiz_id: int, questionIndex: int):
    con = createConnectionToDatabase()
    cur = con.cursor()

    
    cur.execute(f"SELECT * FROM Questions where ques_id in (select ques_id from Quiz_questions where quiz_id = ?)", (quiz_id,))
    res = cur.fetchall()

    cur.execute("UPDATE Quiz_questions SET isRightAnswer = true WHERE quiz_id = ? AND ques_id = ?;", (quiz_id, res[questionIndex][0]))
    con.commit()

    cur.close()
    con.close() 


def getQuizHistory(user_id: int):
    con = createConnectionToDatabase()
    cur = con.cursor()

    
    cur.execute(f"SELECT * FROM Quiz where user_id = ?", (user_id,))
    res = cur.fetchall()

    msgs: str = []

    for a in res:
        msgs.append(f"Код опитування : {a[0]}\n Дата проведення : {a[2]}\nРезультат : {getQuizPercentage(a[0])} %\n")

    cur.close()
    con.close() 

    return msgs

def getQuizPercentage(quiz_id: int) -> float:
    con = createConnectionToDatabase()
    cur = con.cursor()
    
    cur.execute(f"SELECT * FROM Quiz_questions where quiz_id  = ?", (quiz_id,))
    res = cur.fetchall()

    count = 0
    for a in res:
        if(a[2] == True):
            count+=1

    cur.close()
    con.close() 

    return count*10

def createQuestion(ques : list[int, int, str, str, str, str, str]):
    con = createConnectionToDatabase()
    cur = con.cursor()
    
    cur.execute(f"insert into Questions values(?, ?, ?, ?, ?, ?, ?)", ques)
    con.commit()

    cur.close()
    con.close() 
