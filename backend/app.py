import requests
from urllib.parse import parse_qs
from flask import Flask, request, redirect, session, url_for, jsonify
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from dotenv import dotenv_values
import datetime
import json

from database import init_db, db
from model import Idea


# .env ファイルから環境変数を取得する
# GITHUB_CLIENT_ID: https://github.com/settings/applications/new にアクセスして作る
# GITHUB_CLIENT_SECRET: 上に同じ
# FLASK_SECRET_KEY: flaskのsessionを使うためのシークレットーキー. 適当に設定すればいい.
env = dotenv_values(".env")

app = Flask(__name__)
if "FLASK_SECRET_KEY" in env:
    app.secret_key = env["FLASK_SECRET_KEY"]
app.config["JSON_AS_ASCII"] = False


init_db(app)


@app.route("/")
def hello():
    return "hello"


@app.route("/oauth")
def oauth():
    # あなたのGitHubアカウントをこのアプリに連携していいですか？の画面にリダイレクトする
    url = "https://github.com/login/oauth/authorize?client_id={}".format(env["GITHUB_CLIENT_ID"])
    return redirect(url)


@app.route("/callback/github")
def callback():
    # https://github.com/settings/applications/new のAuthorization callback URLで
    #   http://localhost:5000/callback/github を設定しておく
    # ユーザが連携を許可してくれたときに呼び出される

    # 入手したrequest.args["code"]を利用してユーザのアクセストークンを発行する
    url = "https://github.com/login/oauth/access_token?code={}&client_id={}&client_secret={}".format(
        request.args["code"],
        env["GITHUB_CLIENT_ID"],
        env["GITHUB_CLIENT_SECRET"],
    )
    r = requests.get(url)
    access_token = parse_qs(r.text)["access_token"][0]

    # アクセストークンをsessionに保存し, 後から使えるようにする
    session["access_token"] = access_token
    return redirect(url_for("user"))


@app.route("/logout")
def logout():
    del session["access_token"]
    return redirect(url_for("hello"))


def github_client():
    print("access_token:", session["access_token"])
    return Client(
        transport=RequestsHTTPTransport(
            url = "https://api.github.com/graphql",
            use_json = True,
            headers = {
                "Content-type": "application/json",
                "Authorization": "Bearer {}".format(session["access_token"])
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
#     g = Github(session["access_token"])
#     user = g.get_user()
#     repo = g.get_repo("{}/{}".format(user.login, repo))
#     issues = repo.get_issues()
#     issues = list(map(lambda issue: {"title": issue.title, "number": issue.number}, issues))
#     return jsonify(issues)
# 
# 
# # 指定されたissueのコメントを表示
# @app.route("/repos/<repo>/issues/<int:issue_number>/comments")
# def comments(repo, issue_number):
#     g = Github(session["access_token"])
#     user = g.get_user()
#     repo = g.get_repo("{}/{}".format(user.login, repo))
#     issue = repo.get_issue(issue_number)
#     comments = issue.get_comments()
#     comments = list(map(lambda comment: {"user": comment.user.login, "body": comment.body}, comments))
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
                labels(first:100) {
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
#  GET /timeline/<owner>/<repo>
#  GET /timeline/<owner>/<repo>?labels=bug,documentation
# クエリパラメータ:
#  label: labelでOR検索. 現状Ideaに対応するlabelがないので, Ideaは弾かれない.
@app.route("/timeline/<owner>/<repo>")
def timeline(owner, repo):
    labels = request.args["labels"].split(",") if "labels" in request.args else None

    #issue_and_comments = get_issue_and_comments(owner, repo, labels)
    pullrequest_and_comments = get_pullrequest_and_comments(owner, repo, labels)
    ideas = get_ideas(owner, repo)

    #timeline = issue_and_comments + pullrequest_and_comments + ideas
    timeline = pullrequest_and_comments + ideas

    # updated_at が新しい順に並べる
    return jsonify(list(reversed(sorted(timeline, key=lambda element: element["updatedAt"]))))


def get_issue_and_comments(owner, repo, labels):
    filt = {}
    if labels is not None:
        filt["labels"] = labels

    issues = github_client().execute(
        gql("""
        query($owner:String!, $repo:String!, $filter:IssueFilters!) {
            repository(owner: $owner, name: $repo) {
                issues(first:100, filterBy: $filter) {
                    edges {
                        node {
                            number
                            title
                            state
                            url
                            createdAt
                            updatedAt
                            body
                            author {
                                login
                                url
                                avatarUrl
                            }
                            assignees(first:100) {
                                edges {
                                    node {
                                        login
                                        url
                                        avatarUrl
                                    }
                                }
                            }
                            labels(first:100) {
                                edges {
                                    node {
                                        name
                                        color
                                    }
                                }
                            }
                            comments(first:100) {
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
            "repo": repo,
            "filter": filt
        }
    )

    issue_and_comments = []

    for issue_node in issues["repository"]["issues"]["edges"]:
        issue_node["node"]["category"] = "issue"
        issue_and_comments.append(issue_node["node"])

        for comment_node in issue_node["node"]["comments"]["edges"]:
            comment_node["node"]["category"] = "issueComment"
            issue_and_comments.append(comment_node["node"])

    return issue_and_comments


def get_pullrequest_and_comments(owner, repo, labels):
    print(owner)
    print(repo)
    print(labels)
    if labels is None:
        pullrequests = github_client().execute(
            gql("""
            query($owner:String!, $repo:String!) {
                repository(owner: $owner, name: $repo) {
                    pullRequests(first:100) {
                        edges {
                            node {
                                number
                                title
                                state
                                url
                                createdAt
                                updatedAt
                                body
                                author {
                                    login
                                    url
                                    avatarUrl
                                }
                                assignees(first:100) {
                                    edges {
                                        node {
                                            login
                                            url
                                            avatarUrl
                                        }
                                    }
                                }
                                labels(first:100) {
                                    edges {
                                        node {
                                            name
                                            color
                                        }
                                    }
                                }
                                comments(first:100) {
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
                "repo": repo,
            }
        )

    else:
        pullrequests = github_client().execute(
            gql("""
            query($owner:String!, $repo:String!, $labels:[String!]) {
                repository(owner: $owner, name: $repo) {
                    pullRequests(first:100, labels: $labels) {
                        edges {
                            node {
                                number
                                title
                                state
                                url
                                createdAt
                                updatedAt
                                body
                                author {
                                    login
                                    url
                                    avatarUrl
                                }
                                assignees(first:100) {
                                    edges {
                                        node {
                                            login
                                            url
                                            avatarUrl
                                        }
                                    }
                                }
                                labels(first:100) {
                                    edges {
                                        node {
                                            name
                                            color
                                        }
                                    }
                                }
                                comments(first:100) {
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
                "repo": repo,
                "labels": labels
            }
        )

    print(pullrequests)
    pullrequest_and_comments = []

    for pullrequest_node in pullrequests["repository"]["pullRequests"]["edges"]:
        pullrequest_and_comments.append(pullrequest_node["node"])
        pullrequest_node["node"]["category"] = "pullRequest"

        for comment_node in pullrequest_node["node"]["comments"]["edges"]:
            comment_node["node"]["category"] = "pullRequestComment"
            pullrequest_and_comments.append(comment_node["node"])

    return pullrequest_and_comments


def get_repo_id(owner, repo):
    return github_client().execute(
        gql("""
        query($owner:String!, $repo:String!) {
            repository(owner: $owner, name: $repo) {
                id
            }
        }
        """),
        variable_values={
            "owner": owner,
            "repo": repo 
        }
    )["repository"]["id"]


def get_ideas(owner, repo):
    ideas = Idea.query.filter(Idea.repo_id == get_repo_id(owner, repo)).all()

    authors = {}
    for idea in ideas:
        authors[idea.author_login] = {}

    authors = {
        author: github_client().execute(gql("""
            query($login:String!) {
                user(login: $login) {
                    url
                    avatarUrl
                }
            }
            """),
            variable_values={
                "login": author,
            })["user"]
        for author in authors
    }

    return [
        {
            "body": idea.body,
            "author": {
                "login": idea.author_login,
                "url": authors[idea.author_login]["url"],
                "avatarUrl": authors[idea.author_login]["avatarUrl"],
            },
            "createdAt": idea.created_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "updatedAt": idea.updated_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "category": "idea",
        } for idea in ideas]


@app.route("/ideas", methods=["POST"])
def post_idea():
    idea = Idea(
        get_repo_id(request.json["owner"], request.json["repo"]),
        request.json["body"],
        request.json["author_login"]
    )
    db.session.add(idea)
    db.session.commit()
    return 'Idea is created successfully'