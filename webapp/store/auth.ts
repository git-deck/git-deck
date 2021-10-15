import { getterTree, mutationTree, actionTree } from 'typed-vuex'
import firebase from 'firebase'
import { AuthUser } from '~/models/types'
import { getUsername } from '~/APIClient/user'
import { saveAccessTokenToLocalStorage } from '~/utils/localStorage'

export const state = () => ({
  authUser: null as AuthUser | null,
  accessToken: null as string | null,
  userName: null as string | null,
})

export type RootState = ReturnType<typeof state>

export const getters = getterTree(state, {
  isLoggedIn: (state) => state.authUser != null && state.accessToken != null,
})

export const mutations = mutationTree(state, {
  SET_AUTH_USER(state, authUser: firebase.User) {
    const { uid, email, photoURL } = authUser
    state.authUser = {
      uid,
      email: email as string,
      avaterUrl: photoURL as string,
    }
  },
  SET_ACCESS_TOKEN(state, accessToken: string | null) {
    state.accessToken = accessToken
    saveAccessTokenToLocalStorage(accessToken)
  },
  SET_USER_NAME(state, userName: string | null) {
    state.userName = userName
  },
  RESET_USER(state) {
    state.authUser = null
    state.accessToken = null
    state.userName = null
    saveAccessTokenToLocalStorage(null)
  },
})

export const actions = actionTree(
  { state, getters, mutations },
  {
    onAuthStateChanged({ commit }, { authUser }: { authUser: firebase.User }) {
      if (authUser != null) {
        commit('SET_AUTH_USER', authUser)
      } else {
        commit('RESET_USER')
      }
    },
    async setGithubAccessToken({ commit, state }, accessToken: string | null) {
      commit('SET_ACCESS_TOKEN', accessToken)
      if (
        accessToken != null &&
        (state.userName == null || state.accessToken !== accessToken)
      ) {
        const userName = await getUsername(accessToken)
        commit('SET_USER_NAME', userName)
      }
    },
  }
)
