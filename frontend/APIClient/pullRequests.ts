import { request, GraphQLClient } from 'graphql-request'
import * as gql from 'gql-query-builder'
import { howLongAgo } from '@/utils/howLongAgo.js'

export const getPullRequests = async (token: string, owner: string, repo: string, states: Object, labels: Array) => {
  const pull_requests_limit = 100
  const assignees_limit = 100
  const labels_limit = 100
  const comments_limit = 100

  let pullRequestVariables = {
    first: {
      value: pull_requests_limit
    },
    states: {
      value: states,
      type: "[PullRequestState!]"
    },
    orderBy: {
      value: {
        field: 'UPDATED_AT',
        direction: 'DESC',
      },
      type: "IssueOrder"
    }
  }
  if (labels.length > 0) {
    pullRequestVariables.labels = {
      value: labels,
      type: "[String!]"
    };
  }

  const query = gql.query({
        operation: 'repository',
        variables: {
          owner: {
            value: owner,
            required: true
          },
          name: {
            value: repo,
            required: true
          },
        },
        fields: [{
          operation: 'pullRequests',
          variables: pullRequestVariables,
          fields: [
            {
              edges: [
                {
                  node: [
                    'number',
                    'title',
                    'state',
                    'url',
                    'createdAt',
                    'updatedAt',
                    'body',
                    {
                      author: [
                        'login',
                        'url',
                        'avatarUrl',
                      ]
                    },
                    {
                      operation: 'assignees',
                      variables: {
                        first: {
                          value: assignees_limit,
                        },
                      },
                      fields: [
                        {
                          edges: [
                            {
                              node: [
                                'login',
                                'url',
                                'avatarUrl'
                              ]
                            }
                          ]
                        }
                      ]
                    },
                    {
                      operation: 'labels',
                      variables: {
                        first: {
                          value: labels_limit,
                        },
                      },
                      fields: [
                        {
                          edges: [
                            {
                              node: [
                                'name',
                                'color',
                              ]
                            }
                          ]
                        }
                      ]
                    },
                    {
                      operation: 'comments',
                      variables: {
                        first: {
                          value: comments_limit,
                        },
                      },
                      fields: [
                        {
                          edges: [
                            {
                              node: [
                                'body',
                                'createdAt',
                                'updatedAt',
                                'url',
                                {
                                  author: [
                                    'login',
                                    'url',
                                    'avatarUrl'
                                  ]
                                }
                              ]
                            }
                          ]
                        }
                      ]
                    },
                  ]
                }
              ]
            }
          ]
        }]
      })

  const client = new GraphQLClient('https://api.github.com/graphql', {
    headers: {'Authorization': token} })

  return await client
    .request(query.query, query.variables)
    .then((data) => {
      data = data.repository.pullRequests.edges.map((pr) => {
          pr = pr.node
          pr.comments = pr.comments.edges.map((comment) => {
            comment = comment.node
            comment.howLongAgo = howLongAgo(new Date(comment.updatedAt))
            return comment
          })
          pr.assignees = pr.assignees.edges.map((assignee) => (assignee.node))
          pr.labels = pr.labels.edges.map((label) => ({
              color: `#${label.node.color}`,
              name: label.node.name,
          }))
          pr.category = "pullRequest"
          pr.howLongAgo = howLongAgo(new Date(pr.updatedAt))
          return pr
        })
      return data
    })
}

