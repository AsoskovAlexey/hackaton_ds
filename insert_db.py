import pymysql
import pandas as pd

LANGUAGES = ["English",
             "Afrikaans",
             "Albanian",
             "Arabic",
             "Armenian",
             "Basque",
             "Belarusan",
             "Bengali",
             "Breton",
             "Bulgarian",
             "Catalan",
             "Cebuano",
             "Chechen",
             "Chinese",
             "Croatian",
             "Czech",
             "Danish",
             "Dutch",
             "Esperanto",
             "Estonian",
             "Farsi",
             "Finnish",
             "French",
             "Frisian",
             "Georgian",
             "German",
             "Greek",
             "Gujarati",
             "Ancient Greek",
             "Hawaiian",
             "Hebrew",
             "Hindi",
             "Hungarian",
             "Icelandic",
             "Ilongo",
             "Indonesian",
             "Irish",
             "Italian",
             "Japanese",
             "Khmer",
             "Korean",
             "Latin",
             "Latvian",
             "LISP",
             "Lithuanian",
             "Malay",
             "Maori",
             "Mongolian",
             "Norwegian",
             "Occitan",
             "Other",
             "Persian",
             "Polish",
             "Portuguese",
             "Romanian",
             "Rotuman",
             "Russian",
             "Sanskrit",
             "Sardinian",
             "Serbian",
             "Sign Language",
             "Slovak",
             "Slovenian",
             "Spanish",
             "Swahili",
             "Swedish",
             "Tagalog",
             "Tamil",
             "Thai",
             "Tibetan",
             "Turkish",
             "Ukranian",
             "Urdu",
             "Vietnamese",
             "Welsh",
             "Yiddish"]


def get_connection():
    """This function establishes a connection to the database using the given user and password"""
    connection = pymysql.connect(host='eu-central.connect.psdb.cloud',
                                 user='fsvg7rq9qyuartm9nth7',
                                 password='pscale_pw_vxHTF8ZmCW72mxG2ERyi3mJCfY5VlwtVDSgU3C0N3Gd',
                                 database='linkup_db',
                                 ssl_ca='/etc/ssl/certs/ca-certificates.crt',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection


def run_query(connection, query, query_parameters=None):
    """ this is the user function used to execute a query in the sql database
    """
    with connection.cursor() as cursor:
        cursor.execute(query, query_parameters)
        result = cursor.fetchone()
    return result


def run_update(connection, query, query_parameters=None):
    """ this function is used to update the databases and save the changes.
    """
    with connection.cursor() as cursor:
        result = cursor.execute(query, query_parameters)
        connection.commit()
    return result


def insert_row(row, user_id, connection):
    create_user = """INSERT INTO users
                            (id, age ,diet, drinks, education, ethnicity,
                            job, cats, dogs, religion, sex,
                            smokes)
                            VALUES
                            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    values = (user_id,
              row['age'],
              row['diet'],
              row['drinks'], row['education'],
              row['ethnicity'],
              row['job'],
              row['cats'] if row['cats'] != 'other' else None,
              row['dogs'] if row['dogs'] != 'other' else None,
              row['religion'],
              row['sex'],
              row['smokes'] if row['smokes'] != 'other' else None)
    run_update(connection, create_user, values)

    for lang in row['speaks']:
        lang_id = run_query(connection, 'select id from languages where language = lang')
        lang_id = lang_id['id']
        q = """INSERT INTO users_languages
                            (userId, languageId)
                            VALUES
                            (%s, %s)"""
        run_update(connection, q, (user_id, lang_id))


def insert_lan_table(langs, connection):
    q = """INSERT INTO languages (language)
                                VALUES
                                (%s)"""
    for l in langs:
        run_update(connection, q, l)


if __name__ == '__main__':
    connection = get_connection()

    insert_lan_table(LANGUAGES, connection)

    df = pd.read_csv('profiles_for_db.csv')
    for user_id, row in df.iterrows():
        insert_row(row, user_id, connection)
        print(f'Done inserting user number {user_id} to db')

