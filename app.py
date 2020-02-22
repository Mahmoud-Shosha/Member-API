from flask import Flask, request, jsonify, g
from database import get_db


app = Flask(__name__)


@app.teardown_appcontext
def close_db(error):
    """Close the current DB connection if exists"""
    if hasattr(g, 'db'):
        g.db.close()


@app.route('/members', methods=['GET'])
def get_members():
    """Return all the members in the DB."""

    # Get all members from the DB
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute("select * from members;")
    members = cursor.fetchall()

    # Form Python Data structure for the members
    members_list = []
    for member in members:
        member_dict = {}
        member_dict['id'] = member['id']
        member_dict['name'] = member['name']
        member_dict['email'] = member['email']
        member_dict['level'] = member['level']
        members_list.append(member_dict)

    # Return all the members in the DB as json Data
    return jsonify({'members': members_list})


@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    """Return the member by member_id."""

    return "Return the member by member_id."


@app.route('/member', methods=['POST'])
def add_member():
    """Add a new member in the DB."""

    # Get the member from the request body
    member = request.get_json()
    name = member['name']
    email = member['email']
    level = member['level']

    # Save the member in the DB
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute("""insert into members (name, email, level) values
                   (%s, %s, %s);""", (name, email, level))
    connection.commit()

    # Get the member from the DB
    cursor.execute("select * from members where name = %s;", (name, ))
    member = cursor.fetchone()
    cursor.close()

    # Return the new member in a json format
    return jsonify({'member': {'id': member['id'], 'name': member['name'],
                               'email': member['email'],
                               'level': member['level']}})


@app.route('/member/<int:member_id>', methods=['PUT'])
def modify_member(member_id):
    """Modify a member in the DB by member_id."""

    return "Modify a member in the DB by member_id."


@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    """Delete a member from the DB by member_id."""

    return "Delete a member from the DB by member_id."


if __name__ == '__main__':
    app.run()
