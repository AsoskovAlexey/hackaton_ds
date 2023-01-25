import pandas as pd
from scipy.spatial.distance import cityblock
from flask import Flask
from flask import request
app = Flask(__name__)

df = pd.read_csv('file.csv')
#open csv of dataset instead

#app will filter according to same language and location and different ethnicity (and id)
#it will then calculate manhattan distance of user with all other users
#it will sort the list by distance (ascending), map the ids accordingly and send back the ids ordered
@app.route('/similar_users')
def get_closest_users():
    user_id = request.args.get('user_id')
    suited_users = 'df of users passing conditions'
    'preprocess suited users before calculating distances'
    distances = dict()
    for user in suited_users:
        distance = cityblock(df[user_id==user_id], user)
        'insert to dictionary key:id of user value:distance'
    sorted_distances = sorted(distances.items(), key=lambda x: x[1])
    ids_by_distance = [i[0] for i in sorted_distances]
    return f'{ids_by_distance}'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)