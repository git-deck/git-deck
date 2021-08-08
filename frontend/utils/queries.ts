import * as gql from 'gql-query-builder'

export const labelsQuery = (owner: string, repo: string, labels_limit: number) => {
  return gql.query({
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
          operation: 'labels',
          variables: {
            first: {
              value: labels_limit
            }
          },
          fields: [
            {
              edges: [
                {
                  node: [
                    'name',
                    'color'
                  ]
                }
              ]
            }
          ]
        }]
      })
}

export const issuesQuery = (
  owner: string,
  repo: string,
  states: Object,
  filter: Object,
  assignees_limit: number,
  labels_limit: number,
  comments_limit: number,
) => {
  return gql.query({
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
              value: 100
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

}
