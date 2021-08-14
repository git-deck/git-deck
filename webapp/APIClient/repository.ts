import { request, GraphQLClient } from 'graphql-request'
import * as gql from 'gql-query-builder'

export const checkRepository = async (token: string, repositoryName: string) => {
  const [owner, repo] = repositoryName.split('/')

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
        fields: [
          'id'
        ]
      })

  const client = new GraphQLClient('https://api.github.com/graphql', {
    headers: {'Authorization': token} })

  return await client
    .request(query.query, query.variables)
    .then((data) => (data))
}
