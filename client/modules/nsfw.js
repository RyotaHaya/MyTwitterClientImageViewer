import * as nsfwjs from 'nsfwjs'
import { Store } from 'vuex'
import { Context } from '@nuxt/types'

export default function () {
  ;async () => {
    const model = await nsfwjs.load()
    console.log('loaded')
    console.log(model)
    return model
  },
    (error) => {
      console.log(error.message)
    }
}
// import { Plugin, Context } from '@nuxt/types'
// import * as tf from '@tensorflow/tfjs'

// tf.enableProdMode()
// //...
// let model = await nsfwjs.load(`${urlToNSFWJSModel}`)
// //const model = await nsfwjs.load()

// console.log('NSFWJS load')

// export interface NSFWJS {
//   nsfwModel: any
// }

// const nsfwjsModel = {}

// nsfwjs.load().then((model) => {
//   // Classify the image
// })

// // const myplugin: Plugin = async (context) => {
// //   const { store } = context
// // }

// // const imgPredictions = (imgEl: HTMLImageElement) => {
// //   model.classify(imgEl).then((predictions: any) => {
// //     console.log('Predictions: ', predictions)
// //     return predictions
// //   })
// // }

// // const asyncTest = async () => {
// //   await new Promise((resolve) => setTimeout(resolve, 3000))
// //   console.log('finish')
// // }

// // const Predictions2 = async (imgEl: HTMLImageElement) => {
// //   await new Promise((resolve) =>
// //     model.classify(imgEl).then((predictions: any) => {
// //       return predictions
// //     })
// //   )
// // }

// // export default () => {
// //   const model = async () => {
// //     await nsfwjs.load().then((model: any) => {
// //       // Classify the image
// //       return model
// //     })
// //   }
// // }
