from flask import Flask
from flask import request

app = Flask(__name__)


@app.route('/similar_users')
def get_closest_users():
    user_id = int(request.args.get('user_id'))
    user_num = int(request.args.get('user_num'))
    ids_by_distance = [user_id][:user_num]
    return f'{ids_by_distance}'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
