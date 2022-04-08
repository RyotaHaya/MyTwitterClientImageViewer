import { Repositories } from '~/plugins/axios/repository'

declare module 'vue/types/vue' {
  interface Vue {
    readonly $repositories: Repositories
  }
}

declare module 'vuex' {
  interface Store<S> {
    readonly $repositories: Repositories
  }
}

// vuexに入るやつっぽい
declare module 'vuex/types/index' {
  interface Store<S> {
    readonly $repositories: Repositories
  }
}
