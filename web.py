from flask import Flask, make_response, redirect, request, render_template, url_for
import json
import requests
import datetime
import pymysql

app = Flask(__name__)

@app.route('/')
def home():

    return '<a href="https://github.com/AiAe/RippleTweaks">Ripple Tweaks</a>'

def connect():

    with open("mysql.json", "r") as f:
        mysql = json.load(f)

    connection = pymysql.connect(**mysql, charset="utf8")
    connection.autocommit(True)
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    return connection, cursor


def execute(connection, cursor, sql, args=None):
    try:
        cursor.execute(sql, args) if args is not None else cursor.execute(sql)
        return cursor
    except pymysql.err.OperationalError:
        connection.connect()
        return execute(sql, args)

def shift(l, n):
    return l[n:] + l[:n]

days = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
        31]

def get_chart(id, mode):
    connection, cursor = connect()

    mode = int(mode)

    if mode == 0:
        get_rank = execute(connection, cursor, "SELECT std FROM ranks WHERE user_id = %s", [id]).fetchone()[
            'std']
    elif mode == 1:
        get_rank = execute(connection, cursor, "SELECT taiko FROM ranks WHERE user_id = %s", [id]).fetchone()[
            'taiko']
    elif mode == 2:
        get_rank = execute(connection, cursor, "SELECT ctb FROM ranks WHERE user_id = %s", [id]).fetchone()[
            'ctb']
    else:
        get_rank = execute(connection, cursor, "SELECT mania FROM ranks WHERE user_id = %s", [id]).fetchone()[
            'mania']

    date = datetime.datetime.now().strftime("%d")

    gr = json.loads(get_rank)

    return shift(gr, int(date)), shift(days, int(date))

def find_user(id):
    connection, cursor = connect()

    search = execute(connection, cursor, "SELECT user_id FROM ranks WHERE user_id = %s", [id]).fetchone()

    if search != None and len(search) > 0:

        return True

    else:

        return False


def add_event(id):

    connection, cursor = connect()

    get_user = requests.get("https://ripple.moe/api/v1/users/full", params={"id": id}).json()

    std = []
    taiko = []
    ctb = []
    mania = []

    for n in range(1, 32):
        stdg = get_user["std"]["global_leaderboard_rank"]
        if stdg == None:
            stdg = 1000000
        std.append(stdg)

        taikog = get_user["taiko"]["global_leaderboard_rank"]
        if taikog == None:
            taikog = 1000000
        taiko.append(taikog)

        ctbg = get_user["ctb"]["global_leaderboard_rank"]
        if ctbg == None:
            ctbg = 1000000
        ctb.append(ctbg)

        maniag = get_user["mania"]["global_leaderboard_rank"]
        if maniag == None:
            maniag = 1000000
        mania.append(maniag)

    try:
        execute(connection, cursor, "INSERT INTO ranks (`user_id`, `std`, `taiko`, `ctb`, `mania`) VALUES (%s, %s, %s, %s, %s)",
                    [id, str(std), str(taiko), str(ctb), str(mania)])
    except:
        return ''

def update_event(id):
    date = datetime.datetime.now().strftime("%d")

    connection, cursor = connect()

    user = execute(connection, cursor, "SELECT * FROM ranks WHERE user_id = %s", [id]).fetchone()

    std = []
    taiko = []
    ctb = []
    mania = []

    get_user = requests.get("https://ripple.moe/api/v1/users/full", params={"id": id}).json()
    day = int(date) - 1

    if not get_user["std"]["global_leaderboard_rank"] == None:
        for rank in json.loads(user["std"]):
            std.append(rank)

        std[day] = int(get_user["std"]["global_leaderboard_rank"])
        execute(connection, cursor,
                "UPDATE ranks SET std = %s WHERE user_id = %s",
                [str(std), user["user_id"]])

    if not get_user["taiko"]["global_leaderboard_rank"] == None:
        for rank in json.loads(user["taiko"]):
            taiko.append(rank)

        taiko[day] = int(get_user["taiko"]["global_leaderboard_rank"])
        execute(connection, cursor,
                "UPDATE ranks SET taiko = %sWHERE user_id = %s",
                [str(taiko), user["user_id"]])

    if not get_user["ctb"]["global_leaderboard_rank"] == None:
        for rank in json.loads(user["ctb"]):
            ctb.append(rank)

        ctb[day] = int(get_user["ctb"]["global_leaderboard_rank"])
        execute(connection, cursor,
                "UPDATE ranks SET ctb = %s WHERE user_id = %s",
                [str(ctb), user["user_id"]])

    if not get_user["mania"]["global_leaderboard_rank"] == None:
        for rank in json.loads(user["mania"]):
            mania.append(rank)

        mania[day] = int(get_user["mania"]["global_leaderboard_rank"])
        execute(connection, cursor,
                "UPDATE ranks SET mania = %s WHERE user_id = %s",
                [str(mania), user["user_id"]])

@app.route('/<id>/<mode>/<theme>/')
def chart(id, mode, theme):
    modes = [0, 1, 2, 3]

    if id == None and mode not in modes:

        return 'ERROR'

    if theme == 'true':
        c = 'fff'
        rgb = '255, 255, 255, 1'
    else:
        c = '000'
        rgb = '0, 0, 0, .95'

    if find_user(id):
        update_event(id)
        values, dates = get_chart(id, mode)
        return render_template('less.html', values=values, dates=dates, user_id=id, rgb=rgb, c=c)

    else:
        add_event(id)
        values, dates = get_chart(id, mode)
        return render_template('less.html', values=values, dates=dates, user_id=id, rgb=rgb, c=c)


if __name__ == "__main__":
    app.run(debug=True, port=7001, use_reloader=True, threaded=True, host='127.0.0.1')
