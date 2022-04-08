import {
  Module,
  VuexModule,
  Mutation,
  Action,
  MutationAction,
} from 'vuex-module-decorators'

import * as nsfwjs from 'nsfwjs'

//vuex-module-decoratorsではinjectはsupprt対象外のため直接インスタンスから参照する
// https://github.com/nuxt/typescript/issues/342#issuecomment-616514557
import { $repositories } from '~/plugins/axios/repository'
@Module({
  name: 'twitter',
  stateFactory: true,
  namespaced: true,
})
export default class Twitter extends VuexModule {
  user: any = null
  accessToken: string = ''
  currentDispListId: string = ''
  lists: any = []
  listTweets: any = {}
  count1: number = 0
  count2: number = 0
  anotherCount: number = 0

  nsfwModel: any

  public get getUser() {
    return this.user
  }
  public get getAccessToken() {
    return this.accessToken
  }

  public get getLists() {
    return this.lists
  }
  public get getListTweets() {
    return this.listTweets
  }

  public get getCurrentDispListId() {
    return this.currentDispListId
  }

  public get isAuthenticated() {
    return !!this.accessToken
    //return !!this.user
  }

  public get getAnotherCount() {
    return this.anotherCount
    //return !!this.user
  }

  public get getNswfwModel() {
    return this.nsfwModel
  }

  @Mutation
  async setNswfwModel(payload: any) {
    this.nsfwModel = await nsfwjs.load()
  }

  @Mutation
  setUser(payload: any) {
    this.user = payload
  }

  @Mutation
  setCurrentDispList(payload: any) {
    this.currentDispListId = payload
  }

  @Mutation
  setLists(payload: any) {
    this.lists = payload
  }
  @Mutation
  setAccessToken(accessToken: string) {}

  @Action
  public async _fetchListTweets(payload: any) {
    //   console.log('fetchListTweets called')
    //   let query = {
    //     // ここにクエリパラメータを指定する
    //     maxCount: 30,
    //     include_rts: true,
    //     range_count: 200,
    //   }
    //   const queryData = {}
    //   await $repositories.twitterTineline
    //     .get(queryData, 'lists', payload['id'])
    //     .then((data) => {
    //       console.log('request success')
    //       console.log(data)
    //       //this.hoges = hoges
    //     })
    //     .catch((err) => {
    //       console.error(err)
    //     })
  }

  @Action
  public async fetchUserLists(payload: any) {
    const queryData = { user_name: payload['user_name'] }

    return $repositories.userListRepository
      .get(queryData, '')
      .then((data) => {
        const ret: any = {}
        return data['list']
      })
      .catch((err) => {
        console.error(err)
      })
  }

  @MutationAction
  async updateAnotherCountConditionally(payload: any) {
    const newCount = 1232
    return { anotherCount: newCount }
  }

  @MutationAction
  public async updateLists(payload: any) {
    const queryData = { user_name: payload['user_name'] }

    return $repositories.userListRepository
      .get(queryData, '')
      .then((data) => {
        const ret: any = {}
        const lists = data['list']
        return { lists: data['list'] }
      })
      .catch((err) => {
        console.error(err)
      })
  }

  @Mutation
  setListTweets(payload: any) {
    this.listTweets = payload['data']
  }

  @Mutation
  addNewListTweets(payload: any) {
    const listId = payload['listId']
    const tweets = payload['tweets']

    this.listTweets[listId] = tweets
  }

  @Action
  async fetchListTweets(payload: any) {
    let query: any = {
      // ここにクエリパラメータを指定する
      maxCount: 50,
      includeRTweets: false,
      filter: 'media',
    }

    if (payload['sinceTweetID']) {
      query.sinceTweetId = payload['sinceTweetID']
    }

    return $repositories.twitterTimeline
      .get(query, 'lists', payload['id'])
      .then((data) => {
        return data['timeLineTweets']
      })
      .catch((err) => {
        console.error(err)
      })
  }
}
