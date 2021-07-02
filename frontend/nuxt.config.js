export default {
  // Disable server-side rendering: https://go.nuxtjs.dev/ssr-mode
  ssr: false,

  // Global page headers: https://go.nuxtjs.dev/config-head
  head: {
    title: 'front',
    htmlAttrs: {
      lang: 'en',
    },
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: '' },
    ],
    link: [{ rel: 'icon', type: 'image/x-icon', href: '/favicon.svg' }],
  },

  // Global CSS: https://go.nuxtjs.dev/config-css
  css: ['@/assets/scss/app.scss'],

  // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
  plugins: [],

  // Auto import components: https://go.nuxtjs.dev/config-components
  components: true,

  // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
  buildModules: [
    // https://go.nuxtjs.dev/typescript
    '@nuxt/typescript-build',
  ],

  // Modules: https://go.nuxtjs.dev/config-modules
  modules: [
    // https://go.nuxtjs.dev/axios
    '@nuxtjs/axios',
    'nuxt-webfontloader',
    '@nuxtjs/auth',
    '@nuxtjs/markdownit',
  ],
  markdownit: {
    injected: true,
    html: true,
  },

  // Axios module configuration: https://go.nuxtjs.dev/config-axios
  axios: {},

  // Build Configuration: https://go.nuxtjs.dev/config-build
  build: {},

  // WebFontLoader
  webfontloader: {
    google: {
      families: ['Material Icons'],
    },
  },

  env: {
    accessToken: process.env.NUXT_ENV_ACCESS_TOKEN || 'dummy_access_token',
    client_id: process.env.NUXT_ENV_GITHUB_CLIENT_ID || '',
  },

  auth: {
    strategies: {
      github: {
        client_id: process.env.NUXT_ENV_GITHUB_CLIENT_ID || '',
        client_secret: process.env.NUXT_ENV_GITHUB_CLIENT_SECRET || '',
        scope: 'repo',
      },
    },
    redirect: {
      login: '/login',
      logout: '/login',
      callback: '/callback',
      home: '/',
    },
  },
}
