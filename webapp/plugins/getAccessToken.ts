import { Plugin } from '@nuxt/types'
import firebase from '~/utils/firebase'
import { getAccessTokenFromLocalStorage } from '~/utils/localStorage'

const getAccessTokenPlugin: Plugin = async ({ $accessor }) => {
  const accessToken = getAccessTokenFromLocalStorage()
  if (accessToken != null) {
    $accessor.auth.setGithubAccessToken(getAccessTokenFromLocalStorage())
  } else {
    const result = await firebase.auth().getRedirectResult()
    // @ts-ignore
    const accessToken =
      (result.credential as firebase.auth.OAuthCredential | null)
        ?.accessToken ?? null
    $accessor.auth.setGithubAccessToken(accessToken as string | null)
  }
}

export default getAccessTokenPlugin
