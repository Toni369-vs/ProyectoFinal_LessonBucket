"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint, current_app
from api.models import db, User, Subjects, Students, Comments, Class
from api.utils import generate_sitemap, APIException
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
import random
import string
from flask_mail import Message
import datetime

api = Blueprint('api', __name__)

# ENDPOINT GET A USER

@api.route('/user/<int:user_id>', methods=['GET'])
@jwt_required
def get_one_user_info(user_id):

    try:
        user_information = User.query.filter_by(id=user_id).first()

        response_body = {
            "msg": "usuario obtenido",
            "user": user_information.serialize()
        }

        return jsonify(response_body), 200

    except:
        raise APIException('Usuario no encontrado', 404)

# ENDPOINT CREATE A USER


@api.route("/signup", methods=["POST"])
def register():

    request_body = request.get_json(force=True)

    required_fields = ["name", "email", "password"]
    for field in required_fields:
        if field not in request_body or not request_body[field]:
            raise APIException(f'The "{field}" field cannot be empty', 400)

    verify_email = User.query.filter_by(email=request_body["email"]).first()
    if verify_email:
        raise APIException("An account with this email already exists", 400)

    user = User(name=request_body["name"], email=request_body["email"], password=request_body["password"])

    db.session.add(user)

    try:
        db.session.commit()
    except:
        raise APIException('Internal error', 500)

    response_body = {
        "msg": "Successfully created user",
        "user": user.serialize()
    }

    return jsonify(response_body), 200


# ENDPOINT MODIFY A USER

@api.route('/user/<int:user_id>', methods=['PUT'])
def modify_user(user_id):

    body = request.get_json(force=True)
    user = User.query.get(user_id)

    if not user:
        raise APIException('User no found', 404)

    required_fields = ["name", "email", "birth_date", "address","password"]
    for field in required_fields:
        if field not in body or not body[field]:
            raise APIException(f'The "{field}" field cannot be empty', 400)

    user.name = body["name"]
    user.email = body["email"]
    user.birth_date = body["birth_date"]
    user.address = body["address"]

    try:
        db.session.commit()
    except:
        raise APIException('Internal error', 500)

    response_body = {
        "msg": "User successfully modified",
        "user": user.serialize()
    }
    return jsonify(response_body), 200


### ENDPOINT PATCH  USER


@api.route('/user/<int:user_id>', methods=['PATCH'])
def update_user(user_id):

    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    data = request.get_json()
    if 'name' in data:
        user.name = data['name']
    if 'email' in data:
        user.email = data['email']
    if 'address' in data:
        user.address = data['address']
    if 'birth_date' in data:
        user.birth_date = data['birth_date'] 
    if 'password' in data:
        user.password = data['password'] 

    db.session.commit()
    return jsonify({'message': 'User updated successfully'}), 200





# ENDPOINT GET ALL USERS


@api.route('/users', methods=['GET'])
def get_all_users():

    users_query = User.query.all()

    if not users_query:
        raise APIException('The list of users is empty', 404)

    results = list(map(lambda item: item.serialize(), users_query))

    try:
        response_body = {
            "msg": "List of users obtained",
            "results": results
        }

    except:
        raise APIException('Internal error', 500)

    return jsonify(response_body), 200


# ENDPOINT TO DELETE USER

@api.route('/user/<int:user_id>', methods=['DELETE'])
def del_user(user_id):

    user_query = User.query.filter_by(id=user_id).first()

    if not user_query:
        raise APIException('User not found', 404)

    try:
        db.session.delete(user_query)
        db.session.commit()

        response_body = {
            "msg": "user successfully deleted",
        }

    except:
        raise APIException('Internal error', 500)

    return jsonify(response_body), 200


# ENDPOINT FOR LOGIN

@api.route("/login", methods=["POST"])
def login():

    email = request.json.get("email")
    password = request.json.get("password")

    user = User.query.filter_by(email=email, password=password).first()
    if not user:
        return jsonify("Credenciales incorrectas"), 401

    access_token = create_access_token(identity=email, expires_delta=datetime.timedelta(hours=6))
    # print(access_token)

    response_body = {
        "msg": "logged",
        "user": user.serialize(),
        "token": access_token
    }
    print(response_body),
    return jsonify(response_body), 200


# ENDPOINT GET ALL SUBJECTS

@api.route('/user/<int:user_id>/subjects', methods=['GET'])
def get_all_subjects(user_id):


    subjects_query = Subjects.query.filter_by(user_id=user_id).all()

    if not subjects_query:
        raise APIException('The list of users is empty', 404)

    results = list(map(lambda item: item.serialize(), subjects_query))

    try:
        response_body = {
            "msg": "List of subjects obtained",
            "results": results
        }

    except:
        raise APIException('Internal error', 500)

    return jsonify(response_body), 200


# ENDPOINT GET ONE SUBJECTS

@api.route('/user/<int:user_id>/subjects/<int:subjects_id>', methods=['GET'])
def get_one_subject(user_id, subjects_id):

    try:
        subject_information = Subjects.query.filter_by(user_id=user_id, id=subjects_id).first()

        response_body = {
            "msg": "Subject obtained",
            "subject": subject_information.serialize()
        }

        return jsonify(response_body), 200

    except:
        raise APIException('Subjects not found', 404)


# ENDPOINT CREATE ONE SUBJECT


@api.route("/user/<int:user_id>/subjects", methods=["POST"])
def create_one_subject(user_id):

    request_body = request.get_json(force=True)

    required_fields = ["Subject"]
    for field in required_fields:
        if field not in request_body or not request_body[field]:
            raise APIException(f'The "{field}" field cannot be empty', 400)

    verify_subjects = Subjects.query.filter_by(
        Subject=request_body["Subject"]).first()
    if verify_subjects:
        raise APIException("This subject already exists", 400)

    subjects = Subjects(user_id=user_id, Subject=request_body["Subject"])

    db.session.add(subjects)

    try:
        db.session.commit()
    except:
        raise APIException('Internal error', 500)

    response_body = {
        "msg": "Subjects created",
        "subjects": subjects.serialize(),
        "userId": user_id
    }

    return jsonify(response_body), 200


# ENDPOINT TO DELETE SUBJECT

@api.route('/user/<int:user_id>/subjects/<int:subjects_id>', methods=['DELETE'])
def del_subjects(user_id, subjects_id):

    subjects_query = Subjects.query.filter_by(id=subjects_id, user_id=user_id).first()

    if not subjects_query:
        raise APIException('User not found', 404)

    try:
        db.session.delete(subjects_query)
        db.session.commit()

        response_body = {
            "msg": "subject successfully deleted",
        }

    except:
        raise APIException('Internal error', 500)

    return jsonify(response_body), 200


# ENDPOINT MODIFY A SUBJECT AND ADD STUDENT TO IT

@api.route('/user/<int:user_id>/subjects/<int:subject_id>', methods=['PATCH'])
def add_student_to_subject(user_id, subject_id):
    
    data = request.get_json()
    if 'student_id' in data:
        student_id = data['student_id']
        student = Students.query.get(student_id)
        if not student :
            return jsonify({"message": "Student not found"}), 404
        if student.user_id != user_id:
            return jsonify({"message": "El usuario no tiene permisos para realizar esta acción"}), 403
        
        subject = Subjects.query.get(subject_id)
        if not subject :
            return jsonify({"message": "Subject not found"}), 404
        
        subject.Students.append(student)
        db.session.commit()

        return jsonify({"message": "Estudiante agregado al tema exitosamente"}), 200
    
    elif 'Subject' in data:
        subject = Subjects.query.get(subject_id)

        subject.Subject = data['Subject']

        db.session.commit()

        response_body = {
             "msg": "Subject updated successfully",
             "student": subject.serialize()
         }
        
        return jsonify(response_body), 200
    else:
        return jsonify("Not a valid request"), 400



# ENDPOINT GET ALL STUDENTS

@api.route('/user/<int:user_id>/students', methods=['GET'])
def get_all_students(user_id):
    
    students_query = Students.query.filter_by(user_id=user_id).all()

    if not students_query:
        raise APIException('The list of students is empty', 404)

    results = list(map(lambda item: item.serialize(), students_query))

    try:
        response_body = {
            "msg": "List of students obtained",
            "results": results
        }

    except:
        raise APIException('Internal error', 500)

    return jsonify(response_body), 200


# ENDPOINT GET ONE STUDENT

@api.route('/user/<int:user_id>/students/<int:students_id>', methods=['GET'])
def get_one_student(user_id, student_id):

    try:
        student_information = Students.query.filter_by(user_id=user_id, id=student_id).first()

        response_body = {
            "msg": "Student obtained",
            "students": student_information.serialize()
        }

        return jsonify(response_body), 200

    except:
        raise APIException('Students not found', 404)


# ENDPOINT CREATE ONE STUDENT

@api.route("/user/<int:user_id>/students", methods=["POST"])
def create_one_student(user_id):

    request_body = request.get_json(force=True)

    required_fields = ["name", "email", "address", "phone", "goal"]
    for field in required_fields:
        if field not in request_body or not request_body[field]:
            raise APIException(f'The "{field}" field cannot be empty', 400)

    verify_email = Students.query.filter_by(email=request_body["email"]).first()
    
    if verify_email:
        raise APIException("An account with this email already exists", 402)

    student = Students(user_id=user_id,name=request_body["name"], email=request_body["email"], address=request_body["address"],
                phone=request_body["phone"], goal=request_body["goal"])

    db.session.add(student)

    try:
        db.session.commit()
    except:
        raise APIException('Internal error', 500)

    response_body = {
        "msg": "Student created",
        "student": student.serialize()
    }

    return jsonify(response_body), 200


# ENDPOINT TO DELETE ONE STUDENT

@api.route('/user/<int:user_id>/students/<int:students_id>', methods=['DELETE'])
def del_student(user_id, students_id):

    students_query = Students.query.filter_by(user_id=user_id, id=students_id).first()

    if not students_query:
        raise APIException('Student not found', 404)

    try:
        db.session.delete(students_query)
        db.session.commit()

        response_body = {
            "msg": "student successfully deleted",
        }

    except:
        raise APIException('Internal error', 500)

    return jsonify(response_body), 200


# ENDPOINT MODIFY A STUDENT

@api.route('/user/<int:user_id>/students/<int:student_id>', methods=['PATCH'])
def update_student(user_id, student_id):
    try:
        student = Students.query.filter_by(user_id=user_id, id=student_id).first()

        if not student:
            return jsonify({'message': 'Student not found'}), 404

        data = request.get_json()
        if 'name' in data:
            student.name = data['name']
        if 'email' in data:
            student.email = data['email']
        if 'address' in data:
            student.address = data['address']
        if 'phone' in data:
            student.phone = data['phone']
        if 'goal' in data:
            student.goal = data['goal']

        db.session.commit()

        response_body = {
            "msg": "Student updated successfully",
            "student": student.serialize()
        }

        return jsonify(response_body), 200

    except:

        raise APIException('Internal error', 500)



# ENDPOINT DE VALIDACIÓN


@api.route("/protected", methods=["GET"])
@jwt_required()
def protected():

    current_user = get_jwt_identity()
    user = User.query.filter_by(email=current_user).first()

    if not user:
        return jsonify(success=False, message='User not found'), 404
    
    response_body = {
        "logged_in_as": current_user,
        "user": user.serialize()
    }

    return jsonify(success=True, response=response_body), 200



# ENDPOINT RECUPERAR CONTRASEÑA OLVIDADA

@api.route("/forgotpassword", methods=["POST"])
def forgotpassword():
    
    recover_email = request.json.get('email')

    if not recover_email:
        return jsonify({"msg": "You must provide an email"}), 400
    
    # Busca si el correo existe en la base de datos
    user = User.query.filter_by(email=recover_email).first()
    if user is None:
        return jsonify({"msg": "There is no user with the provided email"}), 400
    
    # Genera una nueva contraseña aleatoria
    recover_password = ''.join(random.choice(
        string.ascii_uppercase + string.digits) for _ in range(8))
    
    # Almacena la nueva contraseña en la base de datos
    user.password = recover_password
    db.session.commit()

    # Envía el correo electrónico con la nueva contraseña
    msg = Message("Password Recovery", recipients=[recover_email])
    msg.html = f"""<h1>Your new password is: {recover_password}</h1>"""
    current_app.mail.send(msg)

    return jsonify({"msg": "Your new password has been sent to your email", "new_password": recover_password}), 200

# ENDPOINT PARA OBTENER TODAS LAS CLASES

@api.route('/user/<int:user_id>/class', methods=['GET'])
def get_all_class(user_id):

    class_query = Class.query.all()

    if not class_query:
        raise APIException('The list of class is empty', 404)

    results = list(map(lambda item: item.serialize(), class_query))
    

    try:
        response_body = {
            "msg": "List of class obtained",
            "results": results
        }

    except:
        raise APIException('Internal error', 500)

    return jsonify(response_body), 200


# ENDPOINT PARA OBTENER UNA CLASE

@api.route('/user/<int:user_id>/class/<int:class_id>', methods=['GET'])
def get_one_class(user_id, class_id):

    try:
        class_information = Class.query.filter_by(id=class_id).first()

        response_body = {
            "msg": "Class obtained",
            "students": class_information.serialize()
        }

        return jsonify(response_body), 200

    except:
        raise APIException('Class not found', 404)


    # ENDPOINT CREATE ONE CLASS

@api.route("/user/<int:user_id>/class", methods=["POST"])
def create_one_class(user_id):

    request_body = request.get_json(force=True)		
    
						
    required_fields = ["subjects_id", "student_id","comments", "date","hour", "price",]
    for field in required_fields:
        if field not in request_body or not request_body[field]:
            raise APIException(f'The "{field}" field cannot be empty', 400)

    newClass = Class(subjects_id=request_body["subjects_id"], student_id=request_body["student_id"], hour=request_body["hour"], comments=request_body["comments"],
                date=request_body["date"], price=request_body["price"], paid=request_body["paid"], user_id=user_id ,)

    db.session.add(newClass)

    db.session.commit()
    
    response_body = {
        "msg": "Class created",
        "student": newClass.serialize()
    }

    print(response_body)
    return jsonify(response_body), 200

 # ENDPOINT MODIFY A CLASS

@api.route('/user/<int:user_id>/class/<int:class_id>', methods=['PATCH'])
def modify_class(user_id, class_id):


    newClass = Class.query.get(class_id)

    if not newClass:
        raise APIException('Class not found', 404)

    if newClass.user_id != user_id:
        raise APIException('Class does not belong to the specified user', 400)
    

    data = request.get_json()
    if 'subjects_id' in data:
            newClass.subjects_id = data['subjects_id']
    if 'student_id' in data:
            newClass.student_id = data['student_id']
    if 'comments' in data:
            newClass.comments = data['comments']
    if 'date' in data:
            newClass.date = data['date']
    if 'price' in data:
            newClass.price = data['price']
    if 'hour' in data:
            newClass.hour = data['hour']
    if 'paid' in data:
            newClass.paid = data['paid']

    print(data)
    try:
        db.session.commit()

    except:
        raise APIException('Internal error', 500)

    response_body = {
        "msg": "Class successfully modified",
        "user": newClass.serialize()
    }
    return jsonify(response_body), 200


# ENDPOINT DELETE CLASS

@api.route('/user/<int:user_id>/class/<int:class_id>', methods=['DELETE'])
def del_class(user_id, class_id):

    class_query = Class.query.filter_by(id=class_id, user_id=user_id).first()

    if not class_query:
        raise APIException('Class not found', 404)

    try:
        db.session.delete(class_query)
        db.session.commit()

        response_body = {
            "msg": "class successfully deleted",
        }

    except:
        raise APIException('Internal error', 500)

    return jsonify(response_body), 200      

# ENDPOINT GET STUDENTS ASIGNED TO A SUBJECT
@api.route('/user/<int:user_id>/students/<int:subject_id>', methods=['GET'])
def get_all_students_per_subject(user_id, subject_id):
    
    students_query = Students.query.filter_by(user_id=user_id, id=subject_id).all()

    if not students_query:
        raise APIException('The list of students is empty', 404)

    results = list(map(lambda item: item.serialize(), students_query))

    try:
        response_body = {
            "msg": "List of students obtained",
            "results": results
         }

    except:
        raise APIException('Internal error', 500)

    return jsonify(response_body), 200      