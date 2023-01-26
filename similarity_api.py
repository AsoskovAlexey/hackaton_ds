import pandas as pd
from scipy.spatial.distance import cityblock
from flask import Flask
from flask import request

app = Flask(__name__)

db_df = pd.read_csv('profiles_for_db.csv')
numeric_df = pd.read_csv('preprocessed_data.csv')


#app will filter according to same language and location and different ethnicity (and id)
#it will then calculate manhattan distance of user with all other users
#it will sort the list by distance (ascending), map the ids accordingly and send back the ids ordered
@app.route('/similar_users')
def get_closest_users():
    user_id = int(request.args.get('user_id'))
    user_num = int(request.args.get('user_num'))
    user_data = db_df.loc[db_df['user_id'] == user_id]
    user_array = numeric_df.loc[numeric_df['user_id'] == user_id]
    suited_users = db_df.loc[(db_df['ethnicity'] != str(user_data['ethnicity']))]
    print(suited_users)
    user_array = user_array.drop(columns='user_id')
    suited_numeric = numeric_df[~(numeric_df.user_id.isin(suited_users.user_id))]
    distances = dict()
    for user in suited_numeric:
        no_id = user.drop(columns='user_id')
        distance = cityblock(user_array, no_id)
        distances[user['user_id']] = distance
    sorted_distances = sorted(distances.items(), key=lambda x: x[1])
    ids_by_distance = [i[0] for i in sorted_distances]
    first_ids = ids_by_distance[:user_num]
    return f'{first_ids}'


if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=8080)
    app.run()
