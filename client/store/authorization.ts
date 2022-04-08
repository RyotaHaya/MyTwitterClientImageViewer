import {
  auth,
  twitterProvider,
  googleProvider,
} from '~/plugins/firebase/firebase'
import Cookies from 'universal-cookie'

import {
  getAuth,
  signInWithPopup,
  TwitterAuthProvider,
  GoogleAuthProvider,
  signOut,
} from 'firebase/auth'

import {
  Module,
  VuexModule,
  Mutation,
  Action,
  MutationAction,
} from 'vuex-module-decorators'

import { $repositories } from '~/plugins/axios/repository'
@Module({
  name: 'authorization',
  stateFactory: true,
  namespaced: true,
})
export default class Authorization extends VuexModule {
  private user: any = null
  private accessToken: string = ''
  private pictcafe_session: string = ''
  private twitter_access_token: string = ''
  private twitter_secret_token: string = ''
  private isLoggedIn = false

  public get getAuth() {
    return { user: this.user, accessToken: this.accessToken }
  }

  public get getIsLoggedIn() {
    return this.isLoggedIn
  }

  public get getUser() {
    return this.user
  }
  public get getAccessToken() {
    return this.accessToken
  }
  public get getPictcafeSession() {
    return this.pictcafe_session
  }

  public get getTwitterAccessToken() {
    return this.twitter_access_token
  }

  public get getTwitterSecret() {
    return this.twitter_secret_token
  }

  public get isAuthenticated() {
    return !!this.pictcafe_session
  }

  public get isAuthenticatedUser() {
    return !!this.user
  }
  @Action
  dummy() {
    console.log('hello')
  }

  @Action
  async signInWithTwitter() {
    return signInWithPopup(auth, twitterProvider)
      .then((result) => {
        const ret: any = {}
        const credential = TwitterAuthProvider.credentialFromResult(result)

        if (credential) {
          ret['token'] = credential.accessToken
          ret['token_secret'] = credential.secret
        }

        return ret
      })
      .catch((error) => {
        console.log('login failed: ')
        // Handle Errors here.
        const errorCode = error.code
        //const errorMessage = error.message
        const errorMessage = 'エラーです'
        throw error
      })
  }

  @Action
  signInWithGoogle() {
    console.log('signInWithGoogle called')
    //const wheels = await get(wheelStore)
    return signInWithPopup(auth, googleProvider)
      .then((result) => {
        // This gives you a Google Access Token. You can use it to access the Google API.
        const credential = GoogleAuthProvider.credentialFromResult(result)
      })
      .catch((error) => {
        console.log('login failed: ')
        // Handle Errors here.
        const errorCode = error.code
        const errorMessage = error.message
        // The email of the user's account used.
        const email = error.email
        // The AuthCredential type that was used.
        const credential = TwitterAuthProvider.credentialFromError(error)
        // ...
      })
  }

  @Action
  signOut() {
    return signOut(auth)
      .then(() => {
        // Sign-out successful.
      })
      .catch((error) => {
        // An error happened.
        throw error
      })
  }

  @Action
  public async setAccessCookieToken(payload: any) {
    const body = {
      firebase_id_token: this.getPictcafeSession,
      token: payload['token'],
      secret: payload['token_secret'],
    }

    return $repositories.authentication
      .post(body, 'sessionLogin')
      .then((data) => {
        console.log('request success')
      })
      .catch((err) => {
        // reject
        throw err
      })
  }

  @Action
  public async loginCheck(payload: any) {
    console.log('loginCheck')

    await $repositories.authentication
      .get('', 'login')
      .then((data) => {
        const ret: any = {}
        return ret
      })
      .catch((err) => {
        console.error(err)
      })
  }

  @Mutation
  setUser(payload: any) {
    this.user = payload
  }

  @Mutation
  setSession(payload: any) {
    this.pictcafe_session = payload['session']
  }

  @Mutation
  setAccessToken(payload: any) {
    this.twitter_access_token = payload['token']
    this.twitter_secret_token = payload['secret']
  }

  @Mutation
  clearCookie() {
    const cookie = new Cookies()
    cookie.remove('session')
    cookie.remove('tw_auth_token')
  }

  // @Mutation
  // setAccessToken(accessToken: string) {
  //   this.accessToken = accessToken
  //   const cookie = new Cookies()
  //   cookie.set('access_token', accessToken, {
  //     path: '/',
  //     secure: true,
  //     httpOnly: true,
  //   })

  //   cookie.set('session', accessToken, {
  //     path: '/',
  //     secure: true,
  //   })
  //   console.log('set cookie')
  //   //cookie.set('access_token', accessToken)
  // }

  @Mutation
  setCookie(cookiePrama: CookieParam) {
    console.log('set cookie')
    console.log(cookiePrama['value'])
  }

  @Mutation
  setCookieHttpOnly(cookiePrama: CookieParam) {
    console.log('set cookie')
    console.log(cookiePrama['value'])
  }
}
