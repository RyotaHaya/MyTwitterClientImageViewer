// nuxtServerInit
// 基本編集しない
// https://github.com/z/vuex-module-decorators#accessing-modules-with-nuxtjs
// https://github.com/championswimmer/vuex-module-decorators/issues/201
import { Store } from 'vuex'
import { Context } from '@nuxt/types'
//import { auth } from '~/plugins/firebase/firebase'
//import authInstance from '~/plugins/firebase/firebase.auth'
import { ActionTree } from 'vuex'
import { ActionContext } from 'vuex/types'
import { initialiseStores } from '~/utils/store-accsessor'

export const state = () => ({
  authUser: null,
})

export type RootState = ReturnType<typeof state>

export const getters = {
  isLoggedIn: (state: any) => !!state.authUser,
}

export const actions: ActionTree<any, any> = {
  nuxtServerInit: async (
    context: ActionContext<RootState, RootState>,
    server: Context
  ) => {
    // nuxtServerInitの処理
    const cookieparser = require('cookieparser')
    if (server.res.req.headers.cookie) {
      const parsed = cookieparser.parse(server.res.req.headers.cookie)
      if (parsed.session != null && parsed.session != '') {
        //console.log('not current login')
      }
    }
  },
}

const initializer = (store: Store<any>) => initialiseStores(store)
export const plugins = [initializer]
export * from '~/utils/store-accsessor'
