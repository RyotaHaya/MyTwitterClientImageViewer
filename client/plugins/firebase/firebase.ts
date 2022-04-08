import { initializeApp, getApps, getApp } from 'firebase/app'
import { getAuth, TwitterAuthProvider, GoogleAuthProvider } from 'firebase/auth'

//console.log('plugins firebase.ts')
const firebaseConfig = {
  apiKey: process.env.apiKey,
  authDomain: process.env.authDomain,
  databaseURL: process.env.databaseURL,
  projectId: process.env.projectId,
  storageBucket: process.env.storageBucket,
  messagingSenderId: process.env.messagingSenderId,
  appId: process.env.appId,
  measurementId: process.env.measurementId,
}

const initializedApp = !getApps().length
  ? initializeApp(firebaseConfig)
  : getApp()

const auth = getAuth()
const user = auth.currentUser

console.log('plugins')
console.log(user)

const twitterProvider = new TwitterAuthProvider()
const googleProvider = new GoogleAuthProvider()

export { auth, twitterProvider, googleProvider }
