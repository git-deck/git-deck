import { GraphQLClient } from 'graphql-request'
import * as gql from 'gql-query-builder'

export const checkRepository = async (
  token: string,
  repositoryName: string
) => {
  const [owner, repo] = repositoryName.split('/')

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
    fields: ['id'],
  })

  const client = new GraphQLClient('https://api.github.com/graphql', {
    headers: { Authorization: token },
  })

  return await client.request(query.query, query.variables)
}

export const getMyRepositories = async (
  token: string,
  owner: string
): Promise<
  {
    owner: string
    name: string
  }[]
> => {
  const query = gql.query({
    operation: 'repositoryOwner',
    variables: {
      login: {
        value: owner,
        required: true,
      },
    },
    fields: [
      {
        operation: 'repositories',
        variables: {
          first: {
            value: 50,
          },
          orderBy: {
            value: {
              field: 'PUSHED_AT',
              direction: 'DESC',
            },
            type: 'RepositoryOrder',
          },
        },
        fields: [
          {
            nodes: [
              'name',
              {
                owner: ['login'],
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

  const res = await client.request(query.query, query.variables)
  const _repositories = res.repositoryOwner.repositories.nodes.map(
    (node: any) => `${node.owner.login}/${node.name}`
  ) as string[]

  const repositories = Array.from(new Set(_repositories)) // 重複排除

  return repositories.map((repository) => ({
    name: repository.split('/')[1],
    owner: repository.split('/')[0],
  }))
}
