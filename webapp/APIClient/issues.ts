import { GraphQLClient } from 'graphql-request'
import * as gql from 'gql-query-builder'
import { howLongAgo } from '@/utils/howLongAgo.js'

export const getIssues = async (token: string, owner: string, repo: string, states: Object, filter: Object) => {
  const issues_limit = 100
  const assignees_limit = 100
  const labels_limit = 100
  const comments_limit = 100

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
          operation: 'issues',
          variables: {
            first: {
              value: issues_limit
            },
            states: {
              value: states,
              type: "[IssueState!]"
            },
            filterBy: {
              value: filter,
              type: "IssueFilters"
            },
            orderBy: {
              value: {
                field: 'UPDATED_AT',
                direction: 'DESC',
              },
              type: "IssueOrder"
            }
          },
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
      data = data.repository.issues.edges.map((issue:any) => {
          issue = issue.node
          issue.comments = issue.comments.edges.map((comment:any) => {
            comment = comment.node
            comment.howLongAgo = howLongAgo(new Date(comment.updatedAt))
            return comment
          })
          issue.assignees = issue.assignees.edges.map((assignee:any) => (assignee.node))
          issue.labels = issue.labels.edges.map((label:any) => ({
              color: `#${label.node.color}`,
              name: label.node.name,
          }))
          issue.category = "issue"
          issue.howLongAgo = howLongAgo(new Date(issue.updatedAt))
          return issue
        })
      return data
    })
}

