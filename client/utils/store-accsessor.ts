/* eslint-disable import/no-mutable-exports */
import { Store } from 'vuex'
import { getModule } from 'vuex-module-decorators'
import Authorization from '~/store/authorization'
import Twitter from '~/store/twitter'
import Todo from '~/store/todo'
import DispSettings from '~/store/disp-settings'

let TodoStore: Todo
let AuthorizationStore: Authorization
let TwitterStore: Twitter
let DispSettingsStore: DispSettings

function initialiseStores(store: Store<any>): void {
  TodoStore = getModule(Todo, store)
  AuthorizationStore = getModule(Authorization, store)
  TwitterStore = getModule(Twitter, store)
  DispSettingsStore = getModule(DispSettings, store)
}

export {
  initialiseStores,
  TodoStore,
  AuthorizationStore,
  TwitterStore,
  DispSettingsStore,
}
