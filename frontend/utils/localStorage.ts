const ADDED_REPOSITORY = 'ADDED_REPOSITORY'
export const saveRepositoryToLocalStorage = (repositoryName: string) => {
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
  const str = localStorage.getItem(ADDED_REPOSITORY)
  if (str == null) return []
  const parsed = JSON.parse(str)
  if (Array.isArray(parsed)) {
    return parsed.filter((value) => typeof value === 'string')
  } else {
    return []
  }
}
