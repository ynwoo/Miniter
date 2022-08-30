from flask import Flask, jsonify, request, current_app
from flask.json import JSONEncoder
from sqlalchemy import create_engine, text


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)

        return JSONEncoder.default(self, obj)

def get_user(user_id):
    user = current_app.database.execute(text("""
            SELECT
                id,
                name,
                email,
                profile
            FROM users
            WHERE id = :user_id
            """), {
                'user_id' : user_id
            }).fetchone()
        
    return {
        'id'      : user['id'],
        'name'    : user['name'],
        'email'   : user['email'],
        'profile' : user['profile']
    } if user else None

def insert_user(user):
    return current_app.database.execute(text("""
            INSERT INTO users (
                name,
                email,
                profile,
                hashed_password
            ) VALUES (
                :name,
                :email,
                :profile,
                :password
            )
        """), user). lastrowid

def insert_tweet(user_tweet):
    return current_app.database.execute(text("""
            INSERT INTO tweets (
                user_id,
                tweet
            ) VALUES (
                :id,
                :tweet
            )
        """), user_tweet).rowcount

def insert_follow(user_follow):
    return current_app.database.execute(text("""
            INSERT INTO users_follow_list (
                user_id,
                follow_user_id
            ) VALUES (
                :id,
                :follow
            )
        """), user_follow).rowcount

def insert_unfollow(user_unfollow):
    return current_app.database.execute(text("""
            DELETE FROM users_follow_list
            WHERE user_id = :id
            AND follow_user_id = :unfollow
        """), user_unfollow).rowcount

def get_timeline(user_id):
    timeline = current_app.database.execute(text("""
        SELECT
            t.user_id,
            t.tweet
        FROM tweets t
        LEFT JOIN users_follow_list ufl ON ufl.user_id = :user_id
        WHERE t.user_id = :user_id
        OR t.user_id = ufl.follow_user_id
    """), {
        'user_id' : user_id
    }).fetchall()

    return [{
        'user_id' : tweet['user_id'],
        'tweet'   : tweet['tweet']
    } for tweet in timeline]

def create_app(test_config = None):
    app = Flask(__name__)

    app.json_encoder = CustomJSONEncoder

    if test_config is None:
        app.config.from_pyfile("config.py")
    else:
        app.config.update(test_config)

    database = create_engine(app.config['DB_URL'], encoding = 'utf-8', max_overflow = 0)
    app.database = database

    @app.route("/ping", methods=['GET'])
    def ping():
        return "pong"

    @app.route("/sign-up", methods=['POST'])
    def sign_up():
        new_user    = request.json
        new_user_id = insert_user(new_user)
        new_user    = get_user(new_user_id)

        return jsonify(new_user)

    @app.route("/tweet", methods=['POST'])
    def tweet():
        user_tweet = request.json
        tweet      = user_tweet['tweet']

        if len(tweet) > 300:
            return '300자를 초과했습니다', 400

        insert_tweet(user_tweet)

        return '', 200

    @app.route("/follow", methods=['POST'])
    def follow():
        payload            = request.json
        insert_follow(payload)

        return '', 200

    @app.route("/unfollow", methods=['POST'])
    def unfollow():
        payload              = request.json
        insert_unfollow(payload)

        return '', 200

    @app.route("/timeline/<int:user_id>", methods=['GET'])
    def timeline(user_id):
        return jsonify({
            'user_id'  : user_id,
            'timeline' : get_timeline(user_id)
        })
    
    return app

    
# app.users    = {}
# app.id_count = 1
# app.tweets   = []
# app.json_encoder = CustomJSONEncoder

# @app.route("/timeline/<int:user_id>", methods=['GET'])
# def timeline(user_id):
#     if user_id not in app.users:
#         return '사용자가 존재하지 않습니다', 400
    
#     follow_list = app.users[user_id].get('follow', set())
#     follow_list.add(user_id)
#     timeline = [tweet for tweet in app.tweets if tweet['user_id'] in follow_list]

#     return jsonify({
#         'user_id'  : user_id,
#         'timeline' : timeline
#     })

# @app.route("/follow", methods=['POST'])
# def follow():
#     payload            = request.json
#     user_id            = int(payload['id'])
#     user_id_to_follow  = int(payload['follow'])

#     if user_id not in app.users or user_id_to_follow not in app.users:
#         return '사용자가 존재하지 않습니다', 400
    
#     user = app.users[user_id]
#     user.setdefault('follow', set()).add(user_id_to_follow)
    
#     return jsonify(user)

# @app.route("/unfollow", methods=['POST'])
# def unfollow():
#     payload              = request.json
#     user_id              = int(payload['id'])
#     user_id_to_unfollow  = int(payload['unfollow'])

#     if user_id not in app.users or user_id_to_unfollow not in app.users:
#         return '사용자가 존재하지 않습니다', 400

#     user = app.users[user_id]
#     user.setdefault('follow', set()).discard(user_id_to_unfollow)

#     return jsonify(user)

# @app.route("/tweet", methods=['POST'])
# def tweet():
#     payload = request.json
#     user_id = int(payload['id'])
#     tweet   = payload['tweet']

#     if user_id not in app.users:
#         return '사용자가 존재하지 않습니다', 400

#     if len(tweet) > 300:
#         return '300자를 초과했습니다', 400

#     app.tweets.append({
#         'user_id' : user_id,
#         'tweet'   : tweet
#     })

#     return '', 200

# @app.route("/sign-up", methods=['POST'])
# def sign_up():
#     new_user                  = request.json
#     new_user["id"]            = app.id_count
#     app.users[app.id_count]   = new_user
#     app.id_count              = app.id_count + 1

#     return jsonify(new_user)

# @app.route("/ping", methods=['GET'])
# def ping():
#     return "pong"

# if __name__=='__main__':
#     # from waitress import serve
#     # serve(app, host='0.0.0.0', port=8080)
#     app.run(host='0.0.0.0', debug=True)