from app.models import Employee
from app.utils.database import db, bcrypt
from flask import Blueprint, request, jsonify
from datetime import datetime

employee_crud = Blueprint("employee_crud", __name__)

@employee_crud.route("/create-employee", methods=["POST"])
def create_employee():
    data = request.get_json()
    print(data)

    # Basic validation
    if (
        not data
        or not data.get("emp_id")
        or not data.get("emp_name")
        or not data.get("emp_password")
        or not data.get("emp_email")
    ):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        # Check if employee exists
        if Employee.query.filter_by(emp_email=data["emp_email"].lower().strip()).first():
            return jsonify({"error": "Email already exists"}), 400

        # Hash password
        hashed_password = (
            bcrypt.generate_password_hash(data["emp_password"]).strip().decode("utf-8")
        )

        # Create employee
        employee = Employee(
            emp_id=data["emp_id"],  # Assuming emp_id is provided in the request
            emp_name=data["emp_name"].strip(),
            emp_email=data["emp_email"].lower().strip(),
            emp_password=hashed_password,
            created_at=datetime.utcnow()  # Set the creation time
        )

        db.session.add(employee)
        db.session.commit()

        return (
            jsonify(
                {
                    "message": "Employee created successfully",
                    "employee": {
                        "id": employee.id,
                        "emp_id": employee.emp_id,
                        "emp_name": employee.emp_name,
                        "emp_email": employee.emp_email,
                    },
                }
            ),
            201,
        )
    except Exception as e:
        db.session.rollback()  # Rollback the session in case of error
        return jsonify({"error": str(e)}), 500


@employee_crud.route("/employees/<int:employee_id>", methods=["GET"])
def get_employee(employee_id):
    try:
        employee = Employee.query.get(employee_id)
        if not employee:
            return jsonify({"error": "Employee not found"}), 404

        return jsonify(
            {
                "id": employee.id,
                "emp_id": employee.emp_id,
                "emp_name": employee.emp_name,
                "emp_email": employee.emp_email,
            }
        ), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@employee_crud.route("/employees", methods=["GET"])
def get_all_employees():
    try:
        employees = Employee.query.all()
        employee_list = [
            {
                "id": employee.id,
                "emp_id": employee.emp_id,
                "emp_name": employee.emp_name,
                "emp_email": employee.emp_email,
            }
            for employee in employees
        ]

        return jsonify(employee_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@employee_crud.route("/employee/<int:employee_id>", methods=["PUT"])
def update_employee(employee_id):
    data = request.get_json()
    try:
        employee = Employee.query.get(employee_id)

        if not employee:
            return jsonify({"error": "Employee not found"}), 404

        # Update fields if provided
        if data.get("emp_name"):
            employee.emp_name = data["emp_name"].strip()
        if data.get("emp_email"):
            employee.emp_email = data["emp_email"].lower().strip()
        if data.get("emp_password"):
            employee.emp_password = bcrypt.generate_password_hash(data["emp_password"]).strip().decode("utf-8")

        db.session.commit()

        return jsonify({"message": "Employee updated successfully"}), 200
    except Exception as e:
        db.session.rollback()  # Rollback the session in case of error
        return jsonify({"error": str(e)}), 500


@employee_crud.route("/employee/<int:employee_id>", methods=["DELETE"])
def delete_employee(employee_id):
    try:
        employee = Employee.query.get(employee_id)

        if not employee:
            return jsonify({"error": "Employee not found"}), 404

        db.session.delete(employee)
        db.session.commit()

        return jsonify({"message": "Employee deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()  # Rollback the session in case of error
        return jsonify({"error": str(e)}), 500