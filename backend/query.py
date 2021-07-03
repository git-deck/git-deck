from gql import gql, Client


COMMENTS_LIMIT = 100
ASSIGNEES_LIMIT = 100


def execute_issue_query(client, owner, repo, labels, states):
    filt = {}
    if labels is not None:
        filt["labels"] = labels

    return client.execute(
        gql("""
        query($owner:String!, $repo:String!, $filter:IssueFilters!, $assignees_limit:Int!, $comments_limit:Int!, $states:[IssueState!]) {
            repository(owner:$owner, name:$repo) {
                issues(first:100, states:$states, filterBy:$filter, orderBy:{field:UPDATED_AT, direction:DESC}) {
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
                            assignees(first:$assignees_limit) {
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
                            comments(last:$comments_limit) {
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
            "filter": filt,
            "states": states,
            "assignees_limit": ASSIGNEES_LIMIT,
            "comments_limit": COMMENTS_LIMIT,
        }
    )["repository"]["issues"]["edges"]


def execute_pull_request_query(client, owner, repo, labels, states):
    if labels is None:
        return client.execute(
            gql("""
            query($owner:String!, $repo:String!, $assignees_limit:Int!, $comments_limit:Int!, $states:[PullRequestState!]) {
                repository(owner:$owner, name:$repo) {
                    pullRequests(first:100, states:$states, orderBy:{field:UPDATED_AT, direction:DESC}) {
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
                                assignees(first:$assignees_limit) {
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
                                comments(last:$comments_limit) {
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
                "states": states,
                "assignees_limit": ASSIGNEES_LIMIT,
                "comments_limit": COMMENTS_LIMIT,
            }
        )["repository"]["pullRequests"]["edges"]

    else:
        return client.execute(
            gql("""
            query($owner:String!, $repo:String!, $labels:[String!], $assignees_limit:Int!, $comments_limit:Int!, $states:[PullRequestState!]) {
                repository(owner: $owner, name: $repo) {
                    pullRequests(first:100, labels:$labels, states:$states, orderBy:{field:UPDATED_AT, direction:DESC}) {
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
                                assignees(first:$assignees_limit) {
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
                                comments(last:$comments_limit) {
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
                "labels": labels,
                "states": states,
                "assignees_limit": ASSIGNEES_LIMIT,
                "comments_limit": COMMENTS_LIMIT,
            }
        )["repository"]["pullRequests"]["edges"]
