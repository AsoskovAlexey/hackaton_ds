from flask import Flask
from flask import request
app = Flask(__name__)


@app.route('/similar_users')
def get_closest_users():
    user_id = request.args.get('user_id')
    ids_by_distance = [user_id]
    return f'{ids_by_distance}'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
