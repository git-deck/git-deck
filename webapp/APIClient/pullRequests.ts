import { howLongAgo } from '@/utils/howLongAgo.js'
import * as gql from 'gql-query-builder'
import { GraphQLClient } from 'graphql-request'

export const getPullRequests = async (
  token: string,
  owner: string,
  repo: string,
  states: Object,
  labels: Array<string>,
  after: string | null
) => {
  const pullRequestsLimit = 10
  const assigneesLimit = 10
  const labelsLimit = 10
  const commentsLimit = 100

  const pullRequestVariables: any = {
    first: { value: pullRequestsLimit },
    states: { value: states, type: '[PullRequestState!]' },
    orderBy: {
      value: {
        field: 'UPDATED_AT',
        direction: 'DESC',
      },
      type: 'IssueOrder',
    },
  }

  if (labels.length > 0) {
    pullRequestVariables.labels = { value: labels, type: '[String!]' }
  }
  if (after !== null) {
    pullRequestVariables.after = { value: after }
  }

  const query = gql.query({
    operation: 'repository',
    variables: {
      owner: { value: owner, required: true },
      name: { value: repo, required: true },
    },
    fields: [
      {
        operation: 'pullRequests',
        variables: pullRequestVariables,
        fields: [
          {
            pageInfo: ['hasNextPage', 'endCursor'],
          },
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
                    author: ['login', 'url', 'avatarUrl'],
                  },
                  {
                    operation: 'assignees',
                    variables: {
                      first: {
                        value: assigneesLimit,
                      },
                    },
                    fields: [
                      { edges: [{ node: ['login', 'url', 'avatarUrl'] }] },
                    ],
                  },
                  {
                    operation: 'labels',
                    variables: {
                      first: {
                        value: labelsLimit,
                      },
                    },
                    fields: [
                      {
                        edges: [
                          {
                            node: ['name', 'color'],
                          },
                        ],
                      },
                    ],
                  },
                  {
                    operation: 'comments',
                    variables: {
                      first: {
                        value: commentsLimit,
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
                              { author: ['login', 'url', 'avatarUrl'] },
                            ],
                          },
                        ],
                      },
                    ],
                  },
                ],
              },
            ],
          },
        ],
      },
    ],
  })

  const client = new GraphQLClient('https://api.github.com/graphql', {
    headers: { Authorization: `Bearer ${token}` },
  })

  return await client.request(query.query, query.variables).then((data) => {
    return {
      pullRequests: data.repository.pullRequests.edges.map((pr: any) => {
        pr = pr.node
        pr.comments = pr.comments.edges.map((comment: any) => {
          comment = comment.node
          comment.howLongAgo = howLongAgo(new Date(comment.updatedAt))
          return comment
        })
        pr.assignees = pr.assignees.edges.map((assignee: any) => assignee.node)
        pr.labels = pr.labels.edges.map((label: any) => ({
          color: `#${label.node.color}`,
          name: label.node.name,
        }))
        pr.category = 'pullRequest'
        pr.howLongAgo = howLongAgo(new Date(pr.updatedAt))
        return pr
      }),
      pageInfo: data.repository.pullRequests.pageInfo,
    }
  })
}
