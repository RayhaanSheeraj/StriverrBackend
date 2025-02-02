from flask import Blueprint, jsonify
from flask_restful import Api, Resource
student_api = Blueprint('student_api', __name__, url_prefix='/api')
# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(student_api)
class StudentAPI:
    @staticmethod
    def get_student(name):
        students = {
            "Rayhaan": {
                "name": "Rayhaan",
                "age": 15,
                "favorite_subject": "Science",
                "favorite_color": "Blue"
            },
            "Hithin": {
                "name": "Hithin",
                "age": 15,
                "favorite_subject": "HPOE",
                "favorite_color": "Red" 
            },
            "Kush": {
                "name": "Kush",
                "age": 15,
                "favorite_subject": "CSP",
                "favorite_color": "Blue"
            },
            "Neil": {
                "name": "Neil",
                "age": 15,
                "favorite_subject": "AP Chemistry",
                "favorite_color": "Cyan"
            },
            "Pradyun": {
                "name": "Pradyun",
                "age": 15,
                "favorite_subject": "AP Physics",
                "favorite_color": "Blue"
            },
            "Zaid": {  
                "name": "Zaid",
                "age": 15,
                "favorite_subject": "AP Bio",
                "favorite_color": "Green"
            },
            "Nikith": {
                "name": "Nikith",
                "age": 16,
                "favorite_subject": "Math",    
                "favorite_color": "red"
            },
        }
        return students.get(name)
    class _Rayhaan(Resource):
        def get(self):
            rayhaan_details = StudentAPI.get_student("Rayhaan")
            return jsonify(rayhaan_details)
    class _Kush(Resource):
        def get(self):
            kush_details = StudentAPI.get_student("Kush")
            return jsonify(kush_details)
    class _Neil(Resource):
        def get(self):
            neil_details = StudentAPI.get_student("Neil")
            return jsonify(neil_details)
    class _Pradyun(Resource):
        def get(self):
            pradyun_details = StudentAPI.get_student("Pradyun")
            return jsonify(pradyun_details)
    class _Hithin(Resource):
        def get(self):
            hithin_details = StudentAPI.get_student("Hithin")
            return jsonify(hithin_details)
    class _Zaid(Resource):
        def get(self):
            zaid_details = StudentAPI.get_student("Zaid")
            return jsonify(zaid_details)
    class _Nikith(Resource):
        def get(self):
            nikith_details = StudentAPI.get_student("Nikith")
            return jsonify(nikith_details)
        
        
    class _Bulk(Resource):
        def get(self):
            rayhaan_details = StudentAPI.get_student("Rayhaan")
            kush_details = StudentAPI.get_student("Kush")
            neil_details = StudentAPI.get_student("Neil")
            pradyun_details = StudentAPI.get_student("Pradyun")
            hithin_details = StudentAPI.get_student("Hithin")
            zaid_details = StudentAPI.get_student("Zaid")
            nikith_details = StudentAPI.get_student("Niktih")            
            return jsonify({"students": [rayhaan_details, kush_details, neil_details, pradyun_details, hithin_details, nikith_details, zaid_details]})

        
    api.add_resource(_Rayhaan, '/student/rayhaan')
    api.add_resource(_Kush, '/student/kush')
    api.add_resource(_Neil, '/student/neil')
    api.add_resource(_Hithin, '/student/hithin')
    api.add_resource(_Pradyun, '/student/pradyun')   
    api.add_resource(_Bulk, '/students')
    api.add_resource(_Zaid, '/student/zaid')
    api.add_resource(_Nikith, '/student/nikith') 

