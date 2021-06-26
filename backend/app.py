import requests
from urllib.parse import parse_qs
from flask import Flask, request, redirect, session, url_for, jsonify
from github import Github
from github.GithubObject import NotSet
from dotenv import dotenv_values
import datetime


# .env ファイルから環境変数を取得する
# GITHUB_CLIENT_ID: https://github.com/settings/applications/new にアクセスして作る
# GITHUB_CLIENT_SECRET: 上に同じ
# FLASK_SECRET_KEY: flaskのsessionを使うためのシークレットーキー. 適当に設定すればいい.
env = dotenv_values(".env")

app = Flask(__name__)
if "FLASK_SECRET_KEY" in env:
    app.secret_key = env["FLASK_SECRET_KEY"]
app.config['JSON_AS_ASCII'] = False


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


@app.route("/user")
def user():
    # sessionに保存してあるアクセストークンで PyGithubのGithubインスタンスを初期化する
    g = Github(session['access_token'])
    user = g.get_user()
    return "Hello, {}".format(user.name)


# issueを表示
@app.route("/repos/<repo>/issues")
def issues(repo):
    g = Github(session['access_token'])
    user = g.get_user()
    repo = g.get_repo("{}/{}".format(user.login, repo))
    issues = repo.get_issues()
    issues = list(map(lambda issue: {'title': issue.title, 'number': issue.number}, issues))
    return jsonify(issues)


# 指定されたissueのコメントを表示
@app.route("/repos/<repo>/issues/<int:issue_number>/comments")
def comments(repo, issue_number):
    g = Github(session['access_token'])
    user = g.get_user()
    repo = g.get_repo("{}/{}".format(user.login, repo))
    issue = repo.get_issue(issue_number)
    comments = issue.get_comments()
    comments = list(map(lambda comment: {'user': comment.user.login, 'body': comment.body}, comments))
    return jsonify(comments) 


# 指定されたリポジトリのラベル一覧
# e.g.
# {
#   {
#     "color": "d73a4a", 
#     "name": "bug"
#   }, 
#   {
#     "color": "0075ca", 
#     "name": "documentation"
#   }, 
#   ...
# }
@app.route("/repos/<repo>/labels")
def labels(repo):
    g = Github(session['access_token'])
    user = g.get_user()
    repo = g.get_repo("{}/{}".format(user.login, repo))
    labels = repo.get_labels()
    labels = list(map(lambda label: {'name': label.name, 'color': label.color}, labels))
    return jsonify(labels)


# 指定したリポジトリのタイムライン取得
# GET /repos/<repo>/timeline
# GET /repos/<repo>/timeline?label=bug,documentation
# GET /repos/<repo>/timeline?since=2018-06-29
# label: labelでOR検索
# since: updated_atが since以降のものだけとってくる
# TODO: speed up
@app.route("/repos/<repo>/timeline")
def timeline(repo):
    g = Github(session['access_token'])
    user = g.get_user()
    repo = g.get_repo("{}/{}".format(user.login, repo))

    since = datetime.datetime.strptime(request.args['since'], '%Y-%m-%d') if 'since' in request.args else NotSet
    labels = request.args['label'].split(',') if 'label' in request.args else None

    issues = repo.get_issues(since=since)

    timeline = []

    for issue in issues:
        # 指定されたlabelを一つも含まないissueとそのコメントはスキップ
        if labels is not None and all([label not in map(lambda label: label.name, issue.labels) for label in labels]):
            continue

        timeline.append({
            'assignees': [
                {
                    'avatar_url': assignee.avatar_url,
                    'name': assignee.name,
                    'url': assignee.url,
                } for assignee in issue.assignees
            ],
            'body': issue.body,
            'created_at': issue.created_at,
            'updated_at': issue.updated_at,
            'labels': [
                {
                    'name': label.name
                } for label in issue.labels
            ],
            'number': issue.number,
            'title': issue.title,
            'url': issue.url,
        })
        for comment in issue.get_comments(since=since):
            timeline.append({
                'body': comment.body,
                'created_at': comment.created_at,
                'updated_at': issue.updated_at,
                'url': comment.url,
                'user': {
                    'avatar_url': comment.user.avatar_url,
                    'name': comment.user.name,
                    'url': comment.user.url,
                },
            })

    # updated_at が新しい順に並べる
    timeline.sort(key=lambda tweet: tweet['updated_at']).reverse()
    return jsonify(timeline)
