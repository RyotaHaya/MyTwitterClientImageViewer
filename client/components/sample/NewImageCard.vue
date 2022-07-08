<template>
  <div>
    <v-card class="mx-auto" max-width="500">
      <!--ローディングされるまで非表示 -->
      <div v-if="(mediaType = 'photo')">
        <v-card-text class="text-body-2 font-weight"> </v-card-text>

        <v-list-item class="grow">
          <v-list-item-avatar color="grey darken-3" size="32">
            <a
              v-bind:href="'https://twitter.com/' + user.screenName"
              target="_blank"
            >
              <v-img
                class="elevation-6"
                alt=""
                :src="user.profileImageUrl"
              ></v-img>
            </a>
          </v-list-item-avatar>

          <v-list-item-content>
            <v-list-item-title class="mr-1 text-caption">{{
              user.name
            }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn icon @click="downloadImages">
            <v-icon>mdi-download</v-icon>
          </v-btn>

          <v-btn
            icon
            v-bind:href="
              'https://twitter.com/' + user.screenName + '/status/' + tweetId
            "
            target="_blank"
          >
            <v-icon left> mdi-twitter </v-icon>
          </v-btn>
        </v-card-actions>
      </div>
    </v-card>
  </div>
</template>
<style scoped>
.SampleEvent {
  background-color: #00a656;
  border-radius: 1em;
  box-shadow: 0 0.2em 0.5em rgba(0, 0, 0, 0.2);
  padding: 1em 2em;
  color: #ffffff;
  font-weight: bold;
  text-decoration: none;
}
.v-img-radius {
  border-radius: 20%;
  min-height: 10px;
}
.like {
  padding-top: 0.35em;
  padding-right: 0.35em;
  display: inline-block;
  text-align: left;
}
</style>
>
<script>
//import * as nsfwjs from 'nsfwjs'
import Lottie from '~/components/atoms/lottie.vue'
import * as animationData from '~/assets/like.json'

export default {
  components: {
    Lottie,
  },
  data() {
    return {
      // twitterデータ
      tweetId: '',
      retweetdId: '',
      text: '',
      mediaType: '',
      mediaUrls: [],
      user: null,
      favorited: false,
      dialog: false,
      imageMultiple: false,
      imgElement: null,
      isDrawing: true,
      isNsfw: false,
      predictions: null,
      // アニメーション定義
      defaultOptions: { animationData: animationData },
      animationSpeed: 1,
      anim: null,

      model: 3,
      rounded: ['0', 'sm', 'md', 'lg', 'xl', 'pill', 'circle'],
    }
  },
  props: {
    tweet: {
      type: Object,
      default: '',
      required: true,
    },
    parentListId: {
      type: String,
      default: '',
      required: true,
    },
  },
  methods: {
    SampleEvent() {
      alert(`Hello `)
    },
    open: () => {
      // dataのdialogをtrueに書き換えているだけ
    },

    tweetFav() {
      // dataのdialogをtrueに書き換えているだけ
      if (this.favorited) {
        this.favorited = false
      } else {
        this.favorited = true
      }
    },

    downloadImage(url, fileName) {
      const searchParams = new URLSearchParams(url)
      fetch(url, {
        method: 'GET',
        headers: {},
      })
        .then((response) => {
          response.arrayBuffer().then((buffer) => {
            const url = window.URL.createObjectURL(new Blob([buffer]))
            const link = document.createElement('a')
            link.href = url
            link.download = fileName
            link.setAttribute('download', `${fileName}`)
            document.body.appendChild(link)
            link.click()
          })
        })
        .catch((err) => {
          console.log(err)
        })
    },

    downloadImages() {
      for (const [index, url] of this.mediaUrls.entries()) {
        let charIndex = url.indexOf('.')
        const searchParams = new URLSearchParams(url)
        console.log(url)
        console.log(searchParams)

        this.downloadImage(
          url,
          `${this.user.screenName}_${this.tweetId}_${index}.${url.substring(
            charIndex
          )}`
        )
      }
    },

    handleAnimation(anim) {
      this.anim = anim
      if (this.favorited) {
        this.anim = anim.goToAndStop(1000)
      } else {
        this.anim = anim.pause()
      }
      this.anim = anim
    },
    like() {
      if (this.favorited) {
        this.anim.stop()
        this.favorited = false
      } else {
        this.favorited = true
        this.anim.setSpeed(1.8)
        this.anim.playSegments([8, 100], true)
      }
    },
    stop: function () {
      this.anim.stop()
    },

    play: function () {
      this.anim.play()
    },
    replay: function () {
      this.anim.goToAndPlay(0)
    },

    pause: function () {
      this.anim.pause()
    },

    // async classifyImage(imgEl) {
    //   //console.log('called calssfy')
    //   // TODO modelを事前に読み込みするよう修正
    //   nsfwjs
    //     .load()
    //     .then((model) => {
    //       // Classify the image
    //       console.log('Classify the image')

    //       return model.classify(imgEl)
    //     })
    //     .then((predictions) => {
    //       this.predictions = predictions

    //       predictions.forEach((prediction) => {
    //         if (prediction.className == 'Hentai') {
    //           if (prediction.probability > 0.1) {
    //             this.isNsfw = true
    //           }
    //         }
    //         if (prediction.className == 'Neutral') {
    //           if (prediction.probability > 0.2) {
    //             this.isDrawing = false
    //           }
    //         }
    //         console.log('Classify the image End')
    //       })
    //     })
    // },
  },
  async fetch() {
    this.tweetId = this.tweet.id
    this.retweetdId = this.tweet.retweetdId
    // 短縮URL部分をリネーム
    this.text = this.tweet.text.substring(0, this.tweet.text.indexOf('https:'))
    this.mediaType = this.tweet.media.mediaType
    this.mediaUrls = this.tweet.media.url
    this.user = this.tweet.user
    this.imageMultiple = this.mediaUrls.length > 1
    this.favorited = this.tweet.favorited

    // NSFWJS処理用に作成
    let imgElement = document.createElement('img')
    imgElement.src = this.tweet.media.url[0]
    imgElement.crossOrigin = 'anonymous'
    imgElement.width = 200
    imgElement.height = 200
    this.imgElement = imgElement
  },
  async created() {
    //this.classifyImage(this.imgElement)
  },

  mounted(context) {
    //this.classifyImage(this.imgElement)
  },

  computed: {
    radius() {
      let rounded = 'rounded'
      const value = this.rounded[this.model]

      return rounded
    },
  },
}
</script>
