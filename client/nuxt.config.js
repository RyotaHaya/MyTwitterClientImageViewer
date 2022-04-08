import colors from 'vuetify/es5/util/colors'

export default {
  // CSR時・SSR時どちらでも利用したいもの
  publicRuntimeConfig: {
    baseURL: process.env.BASE_URL || 'http://locahost:3000',
    axios: {
      baseURL: 'http://localhost:5043',
      browserBaseURL: process.env.API_URL || 'http://localhost:5043',
      proxy: true,
      // axios request時にhostに自動付与する
      prefix: '/api',
      // 認証ヘッダーの送信設定
      credentials: true,
    },
    proxy: { '/api/': { target: 'http://localhost:5043' } },
    // 本番環境用
    //baseURL: process.env.BASE_URL || 'http://locahost:3000',
    //apiURL: process.env.API_URL || 'http://localhost:5043',
  },
  // SSR時のサーバーサイド限定で利用したいもの
  privateRuntimeConfig: {
    secret: process.env.SECRET_KEY,
  },
  // Global page headers: https://go.nuxtjs.dev/config-head
  head: {
    titleTemplate: '%s - PictCafe',
    title: 'PictCafe',
    htmlAttrs: {
      lang: 'en',
    },
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: '' },
      { name: 'format-detection', content: 'telephone=no' },
    ],
    link: [{ rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }],
  },

  // Global CSS: https://go.nuxtjs.dev/config-css
  css: [],

  // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
  plugins: [
    // axios plugins
    { src: '~/plugins/axios/axios-accessor', ssr: true },
    { src: '~/plugins/axios/repository', ssr: true },
    { src: '~/plugins/axios/index', ssr: true },
    // firebase plugins
    { src: '~/plugins/firebase/firebase', mode: 'client' },
    { src: '~/plugins/firebase/firebase.auth', mode: 'client' },
    { src: '~/plugins/vuex/cookie-storage', mode: 'client' },
    // nsfw plugins

    { src: '~/plugins/infiniteloading', ssr: false },
  ],

  server: {
    host: '0.0.0.0',
  },

  router: {
    middleware: 'authenticated',
  },

  // Auto import components: https://go.nuxtjs.dev/config-components
  components: true,

  // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
  buildModules: [
    // https://go.nuxtjs.dev/typescript
    '@nuxt/typescript-build',
    // https://go.nuxtjs.dev/vuetify
    '@nuxtjs/vuetify',
    // https://typed-vuex.roe.dev/
    'nuxt-typed-vuex',
  ],

  // Modules: https://go.nuxtjs.dev/config-modules
  modules: [
    '~/modules/example',
    '~/modules/nsfw',
    // https://go.nuxtjs.dev/axios
    '@nuxtjs/dotenv',
    '@nuxtjs/axios',
    //'@nuxtjs/pwa',
    // [
    //   '@nuxtjs/firebase',
    //   {
    //     config: {
    //       apiKey: process.env.apiKey,
    //       authDomain: process.env.authDomain,
    //       databaseURL: process.env.databaseURL,
    //       projectId: process.env.projectId,
    //       storageBucket: process.env.storageBucket,
    //       messagingSenderId: process.env.messagingSenderId,
    //       appId: process.env.appId,
    //       measurementId: process.env.measurementId,
    //     },
    //     services: {
    //       auth: {
    //         persistence: 'local',
    //         initialize: {
    //           onAuthStateChangedAction: 'onAuthStateChanged',
    //         },
    //         ssr: true,
    //       },
    //     },
    //   },
    // ],
  ],

  pwa: {
    //meta: false,
    //icon: false,
    //workbox: {
    //importScripts: ['~/firebase-auth-sw.js'],
    //importScripts: ['~/firebase-auth-sw_.js'],
    //   dev: true,
    //},
  },

  // Axios module configuration: https://go.nuxtjs.dev/config-axios
  // axios: { proxy: true },

  // Vuetify module configuration: https://go.nuxtjs.dev/config-vuetify
  vuetify: {
    customVariables: ['~/assets/variables.scss'],
    theme: {
      dark: false,
      themes: {
        dark: {
          primary: colors.blue.darken2,
          accent: colors.grey.darken3,
          secondary: colors.amber.darken3,
          info: colors.teal.lighten1,
          warning: colors.amber.base,
          error: colors.deepOrange.accent4,
          success: colors.green.accent3,
        },
      },
    },
  },

  // Build Configuration: https://go.nuxtjs.dev/config-build
  build: {
    /*
     ** You can extend webpack config here
     */
    transpile: [/typed-vuex/],
    extend(config, ctx) {},
  },

  // publicRuntimeConfigでbrowserBaseURLを設定しているため設定不要
  axios: {
    proxy: true,
    // axios request時にhostに自動付与する
    prefix: '/api',
    // 認証ヘッダーの送信設定
    credentials: true,
  },

  // proxy: { '/api/': { target: 'http://localhost:5043' } },
}
