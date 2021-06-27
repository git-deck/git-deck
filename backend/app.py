import requests
from urllib.parse import parse_qs
from flask import Flask, request, redirect, session, url_for, jsonify
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from dotenv import dotenv_values
import datetime
import json

from database import init_db


# .env ファイルから環境変数を取得する
# GITHUB_CLIENT_ID: https://github.com/settings/applications/new にアクセスして作る
# GITHUB_CLIENT_SECRET: 上に同じ
# FLASK_SECRET_KEY: flaskのsessionを使うためのシークレットーキー. 適当に設定すればいい.
env = dotenv_values(".env")

app = Flask(__name__)
if "FLASK_SECRET_KEY" in env:
    app.secret_key = env["FLASK_SECRET_KEY"]
app.config['JSON_AS_ASCII'] = False


db = init_db(app)


@app.route('/')
def hello():
    return 'hello'


@app.route('/oauth')
def oauth():
    # あなたのGitHubアカウントをこのアプリに連携していいですか？の画面にリダイレクトする
    url = "https://github.com/login/oauth/authorize?client_id={}".format(env["GITHUB_CLIENT_ID"])
    return redirect(url)


@app.route("/callback/github")
def callback():
    # https://github.com/settings/applications/new のAuthorization callback URLで
    #   http://localhost:5000/callback/github を設定しておく
    # ユーザが連携を許可してくれたときに呼び出される

    # 入手したrequest.args['code']を利用してユーザのアクセストークンを発行する
    url = "https://github.com/login/oauth/access_token?code={}&client_id={}&client_secret={}".format(
        request.args['code'],
        env["GITHUB_CLIENT_ID"],
        env["GITHUB_CLIENT_SECRET"],
    )
    r = requests.get(url)
    access_token = parse_qs(r.text)['access_token'][0]

    # アクセストークンをsessionに保存し, 後から使えるようにする
    session['access_token'] = access_token
    return redirect(url_for('user'))


def github_client():
    print("access_token:", session['access_token'])
    return Client(
        transport=RequestsHTTPTransport(
            url = "https://api.github.com/graphql",
            use_json = True,
            headers = {
                "Content-type": "application/json",
                "Authorization": "Bearer {}".format(session['access_token'])
            },
            verify = False,
            retries = 3,
        ),
        # これを使うとバグる. なんで?
        #fetch_schema_from_transport=True,
    )


@app.route("/user")
def user():
    resp = github_client().execute(
        gql("""
        query { 
            viewer { 
                login
            }
        }
        """)
    )
    return "Hello, {}".format(resp["viewer"]["login"])


# GraphQL に移行するため削除
#
# # issueを表示
# @app.route("/repos/<repo>/issues")
# def issues(repo):
#     g = Github(session['access_token'])
#     user = g.get_user()
#     repo = g.get_repo("{}/{}".format(user.login, repo))
#     issues = repo.get_issues()
#     issues = list(map(lambda issue: {'title': issue.title, 'number': issue.number}, issues))
#     return jsonify(issues)
# 
# 
# # 指定されたissueのコメントを表示
# @app.route("/repos/<repo>/issues/<int:issue_number>/comments")
# def comments(repo, issue_number):
#     g = Github(session['access_token'])
#     user = g.get_user()
#     repo = g.get_repo("{}/{}".format(user.login, repo))
#     issue = repo.get_issue(issue_number)
#     comments = issue.get_comments()
#     comments = list(map(lambda comment: {'user': comment.user.login, 'body': comment.body}, comments))
#     return jsonify(comments) 


# 指定されたリポジトリのラベル一覧
# e.g.
# [
#   {
#     "color": "d73a4a", 
#     "name": "bug"
#   }, 
#   {
#     "color": "0075ca", 
#     "name": "documentation"
#   }, 
#   ...
# ]
@app.route("/labels/<owner>/<repo>")
def labels(owner, repo):
    resp = github_client().execute(
        gql("""
        query($owner:String!, $repo:String!) {
            repository(owner: $owner, name: $repo) {
                labels(last:100) {
                    edges {
                        node {
                            name
                            color
                        }
                    }
                }
            }
        }
        """),
        variable_values={
            "owner": owner,
            "repo": repo 
        }
    )
    
    ret = [edge["node"] for edge in resp["repository"]["labels"]["edges"]]
    return jsonify(ret)


# 指定したリポジトリのタイムライン取得
# GET /timeline/<owner>/<repo>
# x GET /timeline/<owner>/<repo>?label=bug,documentation
# x GET /timeline/<owner>/<repo>?since=2018-06-29
# x label: labelでOR検索
# x since: updated_atが since以降のものだけとってくる
@app.route("/timeline/<owner>/<repo>")
def timeline(owner, repo):
    #since = datetime.datetime.strptime(request.args['since'], '%Y-%m-%d') if 'since' in request.args else NotSet
    #labels = request.args['label'].split(',') if 'label' in request.args else None
    #issues(last:100, filterBy: {labels: ["bug","documentation"], states:OPEN, since: "2021-01-09T18:55:30.000Z"}) {

    resp = github_client().execute(
        gql("""
        query($owner:String!, $repo:String!) {
            repository(owner: $owner, name: $repo) {
                issues(last:100) {
                    edges {
                        node {
                            number
                            title
                            url
                            createdAt
                            updatedAt
                            body
                            author {
                                login
                                url
                                avatarUrl
                            }
                            assignees(last:100) {
                                edges {
                                    node {
                                        login
                                        url
                                        avatarUrl
                                    }
                                }
                            }
                            labels(last:100) {
                                edges {
                                    node {
                                        name
                                        color
                                    }
                                }
                            }
                            comments(last:100) {
                                edges {
                                    node {
                                        body
                                        createdAt
                                        updatedAt
                                        url
                                        author {
                                            login
                                            url
                                            avatarUrl
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        """),
        variable_values={
            "owner": owner,
            "repo": repo 
        }
    )
    print("resp:", resp)

    timeline = []
    for issue_node in resp["repository"]["issues"]["edges"]:
        timeline.append(issue_node["node"])

        for comment_node in issue_node["node"]["comments"]["edges"]:
            timeline.append(comment_node["node"])
        
    # updated_at が新しい順に並べる
    print("len:", len(timeline))
    return jsonify(list(reversed(sorted(timeline, key=lambda tweet: tweet['updatedAt']))))
