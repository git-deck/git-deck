import { GraphQLClient } from 'graphql-request'
import * as gql from 'gql-query-builder'

export const getLabels = async (token: string, owner: string, repo: string) => {
  const labelsLimit = 100
  const query = gql.query({
    operation: 'repository',
    variables: {
      owner: {
        value: owner,
        required: true,
      },
      name: {
        value: repo,
        required: true,
      },
    },
    fields: [
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
    ],
  })

  const client = new GraphQLClient('https://api.github.com/graphql', {
    headers: { Authorization: `Bearer ${token}` },
  })

  return await client.request(query.query, query.variables).then((data) => {
    const labels = data.repository.labels.edges.map((label: any) => ({
      label: {
        color: `#${label.node.color}`,
        name: label.node.name,
      },
      labelOpened: true,
    }))
    return labels
  })
}
