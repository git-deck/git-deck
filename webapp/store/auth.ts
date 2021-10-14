import { getterTree, mutationTree, actionTree } from 'typed-vuex'
import firebase from 'firebase'
import { AuthUser } from '~/models/types'

export const state = () => ({
  authUser: null as AuthUser | null,
  accessToken: null as string | null,
})

export type RootState = ReturnType<typeof state>

export const getters = getterTree(state, {
  isLoggedIn: (state) => state.authUser != null && state.accessToken != null,
})

export const mutations = mutationTree(state, {
  SET_AUTH_USER(state, authUser: firebase.User) {
    const { uid, email } = authUser
    state.authUser = { uid, email }
  },
  SET_ACCESS_TOKEN(state, accessToken: string | null) {
    state.accessToken = accessToken
  },
  RESET_USER(state) {
    state.authUser = null
    state.accessToken = null
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
    setGithubAccessToken({ commit }, accessToken: string | null) {
      commit('SET_ACCESS_TOKEN', accessToken)
    },
  }
)
