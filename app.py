from flask import Flask


app = Flask(__name__)


@app.route('/members', methods=['GET'])
def get_members():
    """Return all the members in the DB."""

    return "Return all the members in the DB."


@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    """Return the member by member_id."""

    return "Return the member by member_id."


@app.route('/member', methods=['POST'])
def add_member():
    """Add a new member in the DB."""

    return "Add a new member in the DB."


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
