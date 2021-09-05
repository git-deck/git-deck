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
  const pull_requests_limit = 10
  const assignees_limit = 10
  const labels_limit = 10
  const comments_limit = 100

  let pullRequestVariables: any = {
    first: { value: pull_requests_limit },
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

  console.log('pullRequestVariables:', pullRequestVariables)

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
                        value: assignees_limit,
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
                        value: labels_limit,
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
    headers: { Authorization: token },
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
