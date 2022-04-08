// axiosの共通設定(Interceptorsを利用)
// https://axios.nuxtjs.org/helpers/#interceptors
import { AuthorizationStore } from '~/store'

export default ({ store, $axios }: any) => {
  // リクエストログ(axiosの拡張機能)
  $axios.onRequest((config: any) => {
    console.log('index onRequest')
    // リクエスト毎に認証用ヘッダーを設定
    config.headers.common[
      'Authorization'
    ] = `Bearer ${AuthorizationStore.getAccessToken}`
    config.headers.common['Accept'] = 'application/json'
    //console.log(config)
  })
  // レスポンスログ
  $axios.onResponse((response: any) => {
    console.log('index onResponse')
  })
  // エラーログ
  $axios.onError((e: any) => {
    console.log(e.response)
  })
}
