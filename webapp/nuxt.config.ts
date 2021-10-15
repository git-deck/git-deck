import { NuxtConfig } from '@nuxt/types'
export default {
  // Disable server-side rendering: https://go.nuxtjs.dev/ssr-mode
  ssr: true,
  target: 'static',

  // Global page headers: https://go.nuxtjs.dev/config-head
  head: {
    title: 'GitDeck',
    htmlAttrs: {
      lang: 'ja',
    },
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      {
        hid: 'description',
        name: 'description',
        content:
          'GitDeckはGitHubリポジトリごとにタイムラインを横に並べて表示するサービスです。複数のリポジトリのIssue/Pull Requestやそこで行われている議論を一目でチェックすることができます。',
      },
      {
        hid: 'og:url',
        property: 'og:url',
        content: 'http://git-deck.work/',
      },
      {
        hid: 'og:title',
        property: 'og:title',
        content: 'GitDeck',
      },
      {
        hid: 'og:type',
        property: 'og:type',
        content: 'website',
      },
      {
        hid: 'og:description',
        property: 'og:description',
        content:
          'GitHubの様々なリポジトリの情報をブラウザ上で一目でチェックできるサービスです',
      },
      {
        hid: 'og:image',
        property: 'og:image',
        content: '/ogp.png',
      },
      {
        name: 'twitter:card',
        content: 'summary_large_image',
      },
    ],
    link: [{ rel: 'icon', type: 'image/x-icon', href: '/favicon.svg' }],
  },

  // Global CSS: https://go.nuxtjs.dev/config-css
  css: ['@/assets/scss/app.scss'],

  // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
  plugins: [
    { src: '~/plugins/vue-js-modal', mode: 'client' },
    { src: '~/plugins/getAccessToken', mode: 'client' },
  ],

  // Auto import components: https://go.nuxtjs.dev/config-components
  components: true,

  // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
  buildModules: [
    // https://go.nuxtjs.dev/typescript
    '@nuxt/typescript-build',
    'nuxt-typed-vuex',
  ],

  // Modules: https://go.nuxtjs.dev/config-modules
  modules: [
    // https://go.nuxtjs.dev/axios
    '@nuxtjs/axios',
    'nuxt-webfontloader',
    '@nuxtjs/markdownit',
    '@nuxtjs/color-mode',
    '@nuxtjs/google-adsense',
    '@nuxtjs/firebase',
  ],

  // 'google-adsense': {
  //   id: 'ca-pub-3253334117542861',
  // },

  markdownit: {
    injected: true,
    html: true,
    runtime: true,
    use: ['markdown-it-emoji'],
  },

  firebase: {
    config: {
      apiKey: process.env.NUXT_ENV_API_KEY,
      authDomain: process.env.NUXT_ENV_AUTH_DOMAIN,
      projectId: process.env.NUXT_ENV_PROJECT_ID,
      storageBucket: process.env.NUXT_ENV_STORAGE_BUCKET,
      messagingSenderId: process.env.NUXT_ENV_MESSAGING_SENDER_ID,
      appId: process.env.NUXT_ENV_APP_ID,
      measurementId: process.env.NUXT_ENV_MEASUREMENT_ID,
    },
    services: {
      auth: {
        initialize: {
          onAuthStateChangedAction: 'auth/onAuthStateChanged',
        },
        ssr: true,
      },
    },
  },

  // Axios module configuration: https://go.nuxtjs.dev/config-axios
  axios: {},

  // Build Configuration: https://go.nuxtjs.dev/config-build
  build: {
    transpile: [/typed-vuex/],
  },

  // WebFontLoader
  webfontloader: {
    google: {
      families: ['Material Icons'],
    },
  },

  env: {},

  // typescript: {
  //  typeCheck: {
  //    async: false
  //  }
  // }
} as NuxtConfig
