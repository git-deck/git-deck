import { Middleware } from '@nuxt/types'

const authMiddleware: Middleware = ({ $accessor, redirect }) => {
  if (!$accessor.auth.isLoggedIn) {
    redirect('/login')
  }
}
export default authMiddleware
