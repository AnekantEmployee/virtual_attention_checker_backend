from flask import Blueprint, request, jsonify
from datetime import datetime
from app.models import Meeting, db
from sqlalchemy.exc import SQLAlchemyError

# Create a Blueprint for meeting routes
meeting_crud = Blueprint("meeting_crud", __name__)


@meeting_crud.route("/", methods=["POST"])
def create_meeting():
    """Create a new meeting"""
    data = request.get_json()

    required = ["name", "host_id", "start_time", "attendees"]
    if not all(field in data for field in required):
        return jsonify({"error": "Missing required fields", "required": required}), 400

    if not isinstance(data.get("attendees", []), list):
        return jsonify({"error": "Attendees must be a list"}), 400

    try:
        new_meeting = Meeting(
            name=data["name"],
            host_id=data["host_id"],
            attendees=data["attendees"],
            start_time=datetime.fromisoformat(data["start_time"]),
            end_time=(
                datetime.fromisoformat(data["end_time"])
                if data.get("end_time")
                else None
            ),
            agenda=data.get("agenda", ""),
            meeting_link=data.get("meeting_link", ""),
        )

        db.session.add(new_meeting)
        db.session.commit()

        return (
            jsonify(
                {
                    "message": "Meeting created successfully",
                    "meeting_id": new_meeting.id,
                    "meeting_link": f"/meetings/{new_meeting.id}",
                    "details": {
                        "name": new_meeting.name,
                        "start_time": new_meeting.start_time.isoformat(),
                    },
                }
            ),
            201,
        )

    except ValueError as e:
        db.session.rollback()
        return jsonify({"error": "Invalid datetime format", "details": str(e)}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


@meeting_crud.route("/", methods=["GET"])
def list_meetings():
    """List all meetings with pagination support"""
    try:
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)

        meetings = Meeting.query.paginate(page=page, per_page=per_page, error_out=False)

        return jsonify(
            {
                "meetings": [
                    {
                        "id": meeting.id,
                        "name": meeting.name,
                        "host_id": meeting.host_id,
                        "start_time": meeting.start_time.isoformat(),
                        "end_time": (
                            meeting.end_time.isoformat() if meeting.end_time else None
                        ),
                    }
                    for meeting in meetings.items
                ],
                "pagination": {
                    "total": meetings.total,
                    "pages": meetings.pages,
                    "current_page": meetings.page,
                    "per_page": meetings.per_page,
                    "has_next": meetings.has_next,
                    "has_prev": meetings.has_prev,
                },
            }
        )
    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


@meeting_crud.route("/<int:meeting_id>", methods=["GET"])
def get_meeting(meeting_id):
    """Get meeting details by ID"""
    try:
        meeting = Meeting.query.get(meeting_id)
        if not meeting:
            return jsonify({"error": "Meeting not found"}), 404

        return jsonify(
            {
                "id": meeting.id,
                "name": meeting.name,
                "host_id": meeting.host_id,
                "attendees": meeting.attendees,
                "start_time": meeting.start_time.isoformat(),
                "end_time": meeting.end_time.isoformat() if meeting.end_time else None,
                "agenda": meeting.agenda,
                "meeting_link": meeting.meeting_link,
                "created_at": meeting.created_at.isoformat(),
            }
        )
    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


@meeting_crud.route("/<int:meeting_id>", methods=["PUT"])
def update_meeting(meeting_id):
    """Update meeting details"""
    data = request.get_json()

    try:
        meeting = Meeting.query.get(meeting_id)
        if not meeting:
            return jsonify({"error": "Meeting not found"}), 404

        if "start_time" in data:
            datetime.fromisoformat(data["start_time"])
        if "end_time" in data and data["end_time"] is not None:
            datetime.fromisoformat(data["end_time"])

        update_fields = {
            "name": data.get("name"),
            "host_id": data.get("host_id"),
            "attendees": data.get("attendees"),
            "start_time": (
                datetime.fromisoformat(data["start_time"])
                if "start_time" in data
                else None
            ),
            "end_time": (
                datetime.fromisoformat(data["end_time"])
                if data.get("end_time")
                else None
            ),
            "agenda": data.get("agenda"),
            "meeting_link": data.get("meeting_link"),
        }

        for field, value in update_fields.items():
            if value is not None:
                setattr(meeting, field, value)

        db.session.commit()
        return jsonify(
            {"message": "Meeting updated successfully", "meeting_id": meeting_id}
        )

    except ValueError as e:
        db.session.rollback()
        return jsonify({"error": "Invalid datetime format", "details": str(e)}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


@meeting_crud.route("/<int:meeting_id>", methods=["DELETE"])
def delete_meeting(meeting_id):
    """Delete a meeting"""
    try:
        meeting = Meeting.query.get(meeting_id)
        if not meeting:
            return jsonify({"error": "Meeting not found"}), 404

        db.session.delete(meeting)
        db.session.commit()
        return jsonify(
            {
                "message": "Meeting deleted successfully",
                "meeting_id": meeting_id,
                "deleted_meeting": {"name": meeting.name, "host_id": meeting.host_id},
            }
        )
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal server error", "details": str(e)}), 500
