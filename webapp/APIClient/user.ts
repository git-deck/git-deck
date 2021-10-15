import * as gql from 'gql-query-builder'
import { GraphQLClient } from 'graphql-request'

/**
 * アクセストークンからユーザーのusernameを取得する
 * @param token アクセストークン
 * @returns username
 */
export const getUsername = async (token: string) => {
  const query = gql.query({
    operation: 'viewer',
    fields: ['login'],
  })

  const client = new GraphQLClient('https://api.github.com/graphql', {
    headers: { Authorization: `Bearer ${token}` },
  })

  const res = await client.request(query.query, query.variables)
  return res.viewer.login
}
