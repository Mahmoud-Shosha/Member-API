from functools import wraps
from flask import Flask, request, jsonify, g
from database import get_db


app = Flask(__name__)


# Hard coded username and password
api_username = 'Mahmoud'
api_password = 'mahmoud'


def protected(view):
    """Return Authentication failed or the passed view functio"""

    @wraps(view)
    def wrapper(*args, **kwargs):

        auth = request.authorization

        if (auth and auth.username == api_username
                and auth.password == api_password):
            return view(*args, **kwargs)

        return jsonify({'message': 'Authentication failed !'}), 403

    return wrapper


@app.teardown_appcontext
def close_db(error):
    """Close the current DB connection if exists"""
    if hasattr(g, 'db'):
        g.db.close()


@app.route('/members', methods=['GET'])
@protected
def get_members():
    """Return all the members in the DB."""

    # Get all members from the DB
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute("select * from members;")
    members = cursor.fetchall()
    cursor.close()

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
@protected
def get_member(member_id):
    """Return the member by member_id."""

    # Get the member from the DB by member_id
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute("select * from members where id = %s;", (member_id, ))
    member = cursor.fetchone()
    cursor.close()

    # Return the member in a json fromat
    return jsonify({'member': {'id': member['id'], 'name': member['name'],
                               'email': member['email'],
                               'level': member['level']}})


@app.route('/member', methods=['POST'])
@protected
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
@protected
def modify_member(member_id):
    """Modify a member in the DB by member_id."""

    # Get the member Data from the request body
    member = request.get_json()
    name = member['name']
    email = member['email']
    level = member['level']

    # modifying the member in the DB
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute("""update members set name = %s, email = %s, level = %s
                   where id = %s;""", (name, email, level, member_id))
    connection.commit()

    # Get the member from the DB by member_id
    cursor.execute("select * from members where id = %s;", (member_id, ))
    member = cursor.fetchone()
    cursor.close()

    # Return the modified member in a json format
    return jsonify({'member': {'id': member['id'], 'name': member['name'],
                               'email': member['email'],
                               'level': member['level']}})


@app.route('/member/<int:member_id>', methods=['DELETE'])
@protected
def delete_member(member_id):
    """Delete a member from the DB by member_id."""

    # Delete the member from the DB by member_id
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute("delete from members where id = %s;", (member_id, ))
    connection.commit()
    cursor.close()

    # Return a confirmation message
    return jsonify({'message': 'The memeber is successfully deleted !'})


if __name__ == '__main__':
    app.run()
