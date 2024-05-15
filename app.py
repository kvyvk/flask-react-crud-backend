from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


app = Flask(__name__)

#allowing CORS Origin
CORS(app) 
#establishing database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://<username>:<password>@localhost/<dbname>'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Define Employee model
class Employee(db.Model):
    #settign up the table name
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(100))
    lastName = db.Column(db.String(100))
    email = db.Column(db.String(100))
    salary = db.Column(db.Float)
    date = db.Column(db.Date)

    def __init__(self, firstName, lastName, email, salary, date):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.salary = salary
        self.date = date

# Routes for CRUD operations
@app.route('/employees', methods=['GET'])
def get_employees():
    employees = Employee.query.all()
    for employee in employees: 
     print(employee.firstName)
    return jsonify([{
        'id': employee.id,
        'firstName': employee.firstName,
        'lastName': employee.lastName,
        'email': employee.email,
        'salary': employee.salary,
        'date': str(employee.date)
    } for employee in employees])

#get employee by id
@app.route('/employees/<int:id>', methods=['GET'])
def get_employee(id):
    employee = Employee.query.get(id)
    return jsonify({
        'id': employee.id,
        'firstName': employee.firstName,
        'lastName': employee.lastName,
        'email': employee.email,
        'salary': employee.salary,
        'date': str(employee.date)
    })
    
#post employee    
@app.route('/employees', methods=['POST'])
def add_employee():
    data = request.json
    new_employee = Employee(**data)
    
    db.session.add(new_employee)
    db.session.commit()
    
    return jsonify({'message': 'Employee added successfully'})

#update employee using id
@app.route('/employees/<int:id>', methods=['PUT'])
def update_employee(id):
    employee = Employee.query.get(id)

    if employee is None:
        return jsonify({'error': 'Employee not found'}), 404

    data = request.json
    for key, value in data.items():
        setattr(employee, key, value)

    db.session.commit()
    return jsonify({'message': 'Employee updated successfully'})

#delete employee using id
@app.route('/employees/<int:id>', methods=['DELETE'])
def delete_employee(id):
    employee = Employee.query.get(id)
    db.session.delete(employee)
    db.session.commit()
    return jsonify({'message': 'Employee deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)