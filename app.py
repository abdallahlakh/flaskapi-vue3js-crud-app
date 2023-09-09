from flask import  Flask ,jsonify,request
from flask_restful import Resource,Api
from flask_cors import CORS
from flask_mysqldb import MySQL
from database_fonctions import update_row_by_id,select_student_by_id,fetch_rows_as_dicts,insert_student,delete_student,get_last_student_id
app=Flask(__name__)
api=Api(app)
CORS(app)
host = 'localhost'
username = 'phpmyadmin'
password = '1234'
database = 'phpmyadmin'
query = 'SELECT * FROM students'

result = fetch_rows_as_dicts(host, username, password, database, query)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'phpmyadmin'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'db1'








mysql = MySQL(app)


class Student(Resource):
    
  
    def put(self,student_id):
        global result
        result = [item if item['student_id'] != student_id  else {'student_id': item['student_id'], 'name': request.get_json()['name'], 'age': request.get_json()['age'], 'mark': request.get_json()['mark']} for item in result]
        update_row_by_id(host, username, password, database,"students",student_id,request.get_json())
        return jsonify({"message": "Student added!!",'METHOD':'PUT'})
    

    def post(self):
        data = request.get_json()
        insert_student(host, username, password, database, data['name'], data['age'], data['mark'])
        student_id=get_last_student_id(host, username, password, database)
        data['student_id']=student_id
        result.append(data)
        # refresh_student_ids(host, username, password, database)

        return jsonify({"message": "Student added!!", 'METHOD': 'POST'})
    


    def patch(self):
        return jsonify({'METHOD':'PATCH'})
    def get(self,student_id=None):
        if student_id is None:
            return jsonify({'students':result,'METHOD':'GET'})
        else:
           student=select_student_by_id(student_id, host,username, password, database)
           return jsonify({'student':student,'METHOD':'GET'})



    def delete(self, student_id):
        global result
        delete_student(host, username, password, database,student_id)
        result=[item for item in result if item['student_id']!=student_id]
            
        return jsonify({"massage":"student deleted!!",'METHOD':'DELETE'})
       


api.add_resource(Student, '/api/students', '/api/students/<int:student_id>')


if __name__=='__main__':
    app.run(debug=True)
