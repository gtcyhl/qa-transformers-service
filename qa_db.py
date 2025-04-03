import pymysql

def fetch_data_from_mysql():
    mysql_conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='123456',
        database='base-model'
    )

    query = "SELECT question_name, answer_desc FROM rec_question_answer_base;"
    cursor = mysql_conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    results = cursor.fetchall()

    assembled_data = []
    for r in results:
        assembled_data.append(r['question_name'] + "&&&" + r['answer_desc'])

    print(assembled_data)

    cursor.close()
    mysql_conn.close()

    return assembled_data
