import { Middleware } from '@nuxt/types'

const unauthMiddleware: Middleware = ({ $accessor, redirect }) => {
  if ($accessor.auth.isLoggedIn) {
    redirect('/')
  }
}
export default unauthMiddleware
