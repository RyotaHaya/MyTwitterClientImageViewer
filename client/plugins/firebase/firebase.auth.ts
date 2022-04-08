import { auth } from '~/plugins/firebase/firebase'
import { onAuthStateChanged } from 'firebase/auth'
import { AuthorizationStore } from '~/store'
import Cookies from 'universal-cookie'
import { Plugin } from '@nuxt/types'

const authInstance: Plugin = async (context) => {
  const { store } = context

  new Promise<void>((resolve, reject) => {
    onAuthStateChanged(auth, (user: any) => {
      if (user) {
        const sessionCookie: CookieParam = {
          key: 'pictcafe_session',
          value: user.uid,
        }
        console.log('current firebaes login')

        AuthorizationStore.setSession({ session: user.accessToken })
      } else {
        // firebase 非ログイン時
        console.log('firebase current not firebase login')
        //console.log(user)
        AuthorizationStore.clearCookie()
        reject(new Error())
      }
      //console.log('onAuthStateChanged settdt')
      resolve(user)
    })
  })
}
export default authInstance
