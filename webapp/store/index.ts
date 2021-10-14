import { getAccessorType } from 'typed-vuex'
import * as auth from './auth'

export const accessorType = getAccessorType({
  modules: {
    auth,
  },
})

declare module 'vue/types/vue' {
  interface Vue {
    $accessor: typeof accessorType
  }
}

declare module '@nuxt/types' {
  interface NuxtAppOptions {
    $accessor: typeof accessorType
  }

  interface Context {
    $accessor: typeof accessorType
  }
}
