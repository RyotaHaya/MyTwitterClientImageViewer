import { Context } from '@nuxt/types'
import { AuthorizationStore } from '~/store'

export default ({ req, redirect, store, route }: Context) => {
  //if (!AuthorizationStore.getIsLoggedIn) {
  // ログインしていない場合、トップページに遷移
  //return redirect('/')
  //} else {
  //  console.log('current login')
  // ユーザ専用ページ
  //return redirect('/todo')
  //}

  // Only Server
  if (process.server) {
    //redirect('/login')

    //const cookieparser = require('cookieparser')
    // リフレッシュトークン更新のためここではCookieのみでチェックする
    if (req.headers.cookie) {
      //const parsed = cookieparser.parse(req.headers.cookie)
      //console.log(parsed)
      // cookie設定済みの場合、ログイン済みとみなす
      //if (parsed.session == null || parsed.session == '') {
      //console.log('not current login')
      //redirect('/login')
      //redirect('/login')
      //} else {
      //console.log('no setting cookie prama')
      //redirect('/login')
      //}
      //} else {
      //redirect('/login')
    }
  }

  // OnlyClient
  if (process.client) {
    //const user = auth.currentUser
    //console.log(user)
    // 認証処理など
    //console.log('middleware client called')
    // 同期
    // AuthorizationStore.loginCheck({})
    //   .then((result) => {
    //     console.log('login Check result')
    //     if (result == undefined) {
    //       AuthorizationStore.clearCookie()
    //       redirect('/login')
    //     }
    //   })
    //   .catch((err) => {
    //     console.log('not login falild'pc22060417
    //     redirect('/login')
    //   })
  }
}
