const ADDED_REPOSITORY = 'ADDED_REPOSITORY'
const ACCESS_TOKEN = 'ACCESS_TOKEN'

export const removeRepositoryFromLocalStorage = (repositoryName: string) => {
  if (typeof window === 'undefined') {
    return
  }
  const repositories = JSON.parse(
    localStorage.getItem(ADDED_REPOSITORY) ?? '[]'
  )
  if (Array.isArray(repositories)) {
    localStorage.setItem(
      ADDED_REPOSITORY,
      JSON.stringify([
        ...repositories.filter(
          (value) => typeof value === 'string' && value !== repositoryName
        ),
      ])
    )
  }
}

export const saveRepositoryToLocalStorage = (repositoryName: string) => {
  if (typeof window === 'undefined') {
    return
  }
  const repositories = JSON.parse(
    localStorage.getItem(ADDED_REPOSITORY) ?? '[]'
  )
  if (Array.isArray(repositories)) {
    localStorage.setItem(
      ADDED_REPOSITORY,
      JSON.stringify([
        ...repositories.filter((value) => typeof value === 'string'),
        repositoryName,
      ])
    )
  } else {
    localStorage.setItem(ADDED_REPOSITORY, JSON.stringify([repositoryName]))
  }
}

export const getSavedRepository = () => {
  if (typeof window === 'undefined') {
    return []
  }
  const str = localStorage.getItem(ADDED_REPOSITORY)
  if (str == null) return []
  const parsed = JSON.parse(str)
  if (Array.isArray(parsed)) {
    return parsed.filter((value) => typeof value === 'string')
  } else {
    return []
  }
}

export const saveAccessTokenToLocalStorage = (accessToken: string | null) => {
  if (accessToken == null) {
    localStorage.removeItem(ACCESS_TOKEN)
  } else {
    localStorage.setItem(ACCESS_TOKEN, accessToken)
  }
}

export const getAccessTokenFromLocalStorage = () => {
  const accessToken = localStorage.getItem(ACCESS_TOKEN)
  return typeof accessToken === 'string' ? accessToken : null
}
