import requests
from urllib.parse import parse_qs
from flask import Flask, request, redirect, session, url_for, jsonify
from flask_cors import CORS
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import datetime
import json
import os

from database import init_db, db
from model import Idea
import utils


# 環境変数
# GITHUB_CLIENT_ID: https://github.com/settings/applications/new にアクセスして作る
# GITHUB_CLIENT_SECRET: 上に同じ

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

CORS(app)

init_db(app)


@app.route("/")
def hello():
    print('request.headers:', request.headers)
    return "hello"


def github_client():
    authorization = request.headers["Authorization"]

    print("authorization:", authorization)
    return Client(
        transport=RequestsHTTPTransport(
            url = "https://api.github.com/graphql",
            use_json = True,
            headers = {
                "Content-type": "application/json",
                "Authorization": authorization,
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


# 指定されたリポジトリのラベル一覧
# e.g.
# [
#   {
#     "color": "#d73a4a", 
#     "name": "bug"
#   }, 
#   {
#     "color": "#0075ca", 
#     "name": "documentation"
#   }, 
#   ...
# ]
@app.route("/labels/<owner>/<repo>")
def labels(owner, repo):
    labels = github_client().execute(
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
    )["repository"]["labels"]
    
    labels = remove_edge_and_nodes(labels)
    labels = add_hash_to_labels(labels)
    return jsonify(labels)


# 指定したリポジトリのタイムライン取得
#  GET /timeline/<owner>/<repo>
#  GET /timeline/<owner>/<repo>?labels=bug,documentation
# クエリパラメータ:
#  labels: labelでOR検索. 現状ideaに対応するlabelがないので, ideaは弾かれない.
@app.route("/timeline/<owner>/<repo>")
def timeline(owner, repo):
    labels = request.args["labels"].split(",") if "labels" in request.args else None

    issues = get_issues(owner, repo, labels)
    pull_requests = get_pull_requests(owner, repo, labels)
    ideas = get_ideas(owner, repo)

    timeline = issues + pull_requests + ideas

    # updated_at が新しい順に並べる
    timeline = list(reversed(sorted(timeline, key=lambda elem: elem["updatedAt"])))

    # howLongAgo を設定
    timeline = list(map(set_how_long_ago, timeline))

    return jsonify(timeline)


def set_how_long_ago(elem):
    elem["howLongAgo"] = utils.how_long_ago(datetime.datetime.strptime(elem["updatedAt"], "%Y-%m-%dT%H:%M:%SZ"))
    if elem["category"] in ["issue", "pullRequest"]:
        for comment in elem["comments"]:
            comment["howLongAgo"] = \
            utils.how_long_ago(datetime.datetime.strptime(comment["updatedAt"], "%Y-%m-%dT%H:%M:%SZ"))
    return elem


def get_issues(owner, repo, labels):
    filt = {}
    if labels is not None:
        filt["labels"] = labels

    issues = github_client().execute(
        gql("""
        query($owner:String!, $repo:String!, $filter:IssueFilters!) {
            repository(owner: $owner, name: $repo) {
                issues(first:100, filterBy: $filter, orderBy: {field:UPDATED_AT, direction:DESC}) {
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
    )["repository"]["issues"]["edges"]

    issues = [issue["node"] for issue in issues]
    for issue in issues:
        issue["comments"] = remove_edge_and_nodes(issue["comments"])
        issue["assignees"] = remove_edge_and_nodes(issue["assignees"])
        issue["labels"] = remove_edge_and_nodes(issue["labels"])
        issue["labels"] = add_hash_to_labels(issue["labels"])

        issue["category"] = "issue"

    return issues


def get_pull_requests(owner, repo, labels):
    if labels is None:
        pull_requests = github_client().execute(
            gql("""
            query($owner:String!, $repo:String!) {
                repository(owner: $owner, name: $repo) {
                    pullRequests(first:100, orderBy: {field:UPDATED_AT, direction:DESC}) {
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
        )["repository"]["pullRequests"]["edges"]

    else:
        pull_requests = github_client().execute(
            gql("""
            query($owner:String!, $repo:String!, $labels:[String!]) {
                repository(owner: $owner, name: $repo) {
                    pullRequests(first:100, labels: $labels, orderBy: {field:UPDATED_AT, direction:DESC}) {
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
        )["repository"]["pullRequests"]["edges"]

    pull_requests = [pull_request["node"] for pull_request in pull_requests]
    for pull_request in pull_requests:
        pull_request["comments"] = remove_edge_and_nodes(pull_request["comments"])
        pull_request["assignees"] = remove_edge_and_nodes(pull_request["assignees"])
        pull_request["labels"] = remove_edge_and_nodes(pull_request["labels"])
        pull_request["labels"] = add_hash_to_labels(pull_request["labels"])

        pull_request["category"] = "pullRequest"

    return pull_requests


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
    return [{
            "body": idea.body,
            "author": {
                "login": idea.author_login,
                "url": "https://github.com/{}".format(idea.author_login),
                "avatarUrl": "https://github.com/{}.png".format(idea.author_login),
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


def add_hash_to_labels(labels):
    return [
        {
            "color": "#{}".format(label["color"]),
            "name": label["name"],
        } for label in labels]

def remove_edge_and_nodes(obj):
    return [el["node"] for el in obj["edges"]]