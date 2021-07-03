import axios from 'axios'

export const addRepository = async (token: string, repositoryName: string) => {
  const [owner, repo] = repositoryName.split('/')
  return await axios.get('/repo_id/' + owner + '/' + repo, {
    headers: {
      Authorization: token,
    },
  })
}
