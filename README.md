# qa-transformers-service
This is a model based on sentence-transformers/multi-qa-MiniLM-L6-cos-v1, which can retrieve the corresponding documents from the knowledge base when users input questions.

1. edit qa_db.py
    1.1 create base-demo database
    1.2 insert data.sql
    1.3 edit mysql_conn such as user,password
2. edit model cache
    2.1 edit cache_dir
3. run qa_cli
    params : {"text" : "预约限制"}
    url: http://127.0.0.1:5000/qa