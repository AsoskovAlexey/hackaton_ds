import pandas as pd
from scipy.spatial.distance import cityblock
from flask import Flask
from flask import request

app = Flask(__name__)

db_df = pd.read_csv('profiles_for_db.csv')
numeric_df = pd.read_csv('preprocessed_data.csv')
numeric_df.drop(columns=['ethnicity', 'sex', 'speaks'], inplace=True)
numeric_df = numeric_df.dropna()


#app will filter according to same language and location and different ethnicity (and id)
#it will then calculate manhattan distance of user with all other users
#it will sort the list by distance (ascending), map the ids accordingly and send back the ids ordered
@app.route('/similar_users')
def get_closest_users():
    user_id = int(request.args.get('user_id'))
    user_num = int(request.args.get('user_num'))
    user_data = db_df.loc[db_df['user_id'] == user_id]
    user_array = numeric_df.loc[numeric_df['user_id'] == user_id]
    suited_users = db_df.loc[db_df['ethnicity'] != user_data['ethnicity'].values[0]]
    user_array = user_array.drop(columns='user_id')
    suited_numeric = numeric_df.loc[(numeric_df.user_id.isin(suited_users.user_id))]
    distances = dict()
    suited_numeric = suited_numeric.head(5000)
    for i in range(len(suited_numeric)):
        user = suited_numeric.iloc[i]
        no_id = user.drop(columns='user_id')
        distance = cityblock(user_array.to_numpy()[0][1:], no_id.to_numpy()[2:])
        distances[user['user_id']] = distance
    sorted_distances = sorted(distances.items(), key=lambda x: x[1])
    ids_by_distance = [int(i[0]) for i in sorted_distances]
    first_ids = ids_by_distance[:user_num]
    return f'{first_ids}'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
