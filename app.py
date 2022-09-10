from venv import create
import config

from flask import Flask
from sqlalchemy import create_engine
from flask_cors import CORS

from model import UserDao, TweetDao
from service import UserService, TweetService
from view import create_endpoints

class Services:
    pass

####################################################
#       Create App
####################################################
def create_app(test_config = None):
    app = Flask(__name__)
    #app.config['JWT_SECRET_KEY'] = 'boseop'
    CORS(app)

    if test_config is None:
        app.config.from_pyfile("config.py")
    else:
        app.config.update(test_config)

    database = create_engine(app.config['DB_URL'], encoding = 'utf-8', max_overflow = 0)

    ## Persistence Layer
    user_dao   = UserDao(database)
    tweet_dao  = TweetDao(database)

    ## Business Layer
    services = Services
    services.user_service = UserService(user_dao, config)
    services.tweet_service = TweetService(tweet_dao)

    ## 엔드포인트들을 생성
    create_endpoints(app, services)

    return app

    # app.database = database
    # app.config['JWT_SECRET_KEY'] = 'boseop'
    
    # @app.route("/ping", methods=['GET'])
    # def ping():
    #     return "pong"

    # @app.route("/sign-up", methods=['POST'])
    # def sign_up():
    #     new_user    = request.json
    #     new_user['password'] = bcrypt.hashpw(
    #         new_user['password'].encode('UTF-8'),
    #         bcrypt.gensalt()
    #     )
    #     new_user_id      = insert_user(new_user)
    #     new_user_info    = get_user(new_user_id)

    #     return jsonify(new_user_info)

    # @app.route("/login", methods=['POST'])
    # def login():
    #     credential = request.json
    #     email      = credential['email']
    #     password   = credential['password']
    #     user_credential = get_user_id_and_password(email)

    #     if user_credential and bcrypt.checkpw(password.encode('UTF-8'),
    #                                 user_credential['hashed_password'].encode('UTF-8')):
    #         user_id = user_credential['id']
    #         payload = {
    #             'user_id' : user_id,
    #             'exp'     : datetime.utcnow() + timedelta(seconds = 60 * 60 * 24)
    #         }
    #         token = jwt.encode(payload, app.config['JWT_SECRET_KEY'],
    #         'HS256')

    #         return jsonify({
    #             'access_token' : token,  # .decode('UTF-8')
    #             'user_id'      : user_id
    #         })
    #     else:
    #         return '', 401

    # @app.route("/tweet", methods=['POST'])
    # @login_required
    # def tweet():
    #     user_tweet       = request.json
    #     user_tweet['id'] = g.user_id
    #     tweet            = user_tweet['tweet']

    #     if len(tweet) > 300:
    #         return '300자를 초과했습니다', 400

    #     insert_tweet(user_tweet)

    #     return '', 200

    # @app.route("/follow", methods=['POST'])
    # @login_required
    # def follow():
    #     payload       = request.json
    #     payload['id'] = g.user_id

    #     insert_follow(payload)

    #     return '', 200

    # @app.route("/unfollow", methods=['POST'])
    # @login_required
    # def unfollow():
    #     payload       = request.json
    #     payload['id'] = g.user_id

    #     insert_unfollow(payload)

    #     return '', 200

    # @app.route("/timeline/<int:user_id>", methods=['GET'])
    # def timeline(user_id):
    #     return jsonify({
    #         'user_id'  : user_id,
    #         'timeline' : get_timeline(user_id)
    #     })
    
    # @app.route("/timeline", methods=['GET'])
    # @login_required
    # def user_timeline():
    #     user_id = g.user_id

    #     return jsonify({
    #         'user_id' : user_id,
    #         'timeline' : get_timeline(user_id)
    #     })

    # return app

    
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