<template>
  <v-card class="mx-auto">
    <v-container fluid>
      <div v-if="tweets && tweets.length > 0">
        <div class="infinite-scroll">
          <div class="infinite-scroll-list">
            <v-container fluid>
              <v-row dense>
                <v-col
                  v-for="tweet in dipsTweets"
                  :key="tweet.id"
                  cols="6"
                  xs="6"
                  sm="6"
                  md="4"
                  lg="3"
                  xl="3"
                >
                  <AtomsImageCard
                    v-bind:tweet="tweet"
                    v-bind:parentListId="dispListId"
                    v-bind:classifyModel="classifyModel"
                  />
                </v-col>
              </v-row>
            </v-container>
          </div>

          <infinite-loading
            ref="infiniteLoading"
            spinner="spiral"
            @infinite="infiniteHandler(dispListId)"
          >
            <span slot="no-more"></span>
            <span slot="no-results">これ以上読み込みできません。</span>
          </infinite-loading>
        </div>
      </div>
      <!-- 読み込み中の処理 -->
      <div v-else>
        <v-row>
          <v-col
            v-for="cnt in 9"
            :key="cnt"
            cols="12"
            xs="6"
            sm="6"
            md="4"
            lg="4"
            xl="4"
          >
            <v-skeleton-loader max-width="300" type="card"></v-skeleton-loader>
          </v-col>
        </v-row>
      </div>
    </v-container>
  </v-card>
</template>
<script>
import { TwitterStore, DispSettingsStore } from '~/store'
import ImageCard from '../atoms/ImageCard.vue'
import * as nsfwjs from 'nsfwjs'

export default {
  data() {
    return {
      getCnt: 30,
      tweets: [],
      drawingTweets: [],
      nsfwTweets: [],
      classifyImageDone: [],
      filter: '',
      scrollY: 0,
      processing: false,
      show: true,
      mounted: false,
    }
  },
  props: {
    dispListId: {
      type: String,
      default: '',
      required: false,
    },
    classifyModel: {
      type: Object,
      default: null,
      required: false,
    },
    dispContent: {
      type: String,
      default: '0',
      required: true,
    },
  },
  components: {
    // 画像表示用
    ImageCard,
  },

  computed: {
    dipsTweets: function () {
      const a = this.drawingTweets
      const content = this.dispContent
      return this.tweets.filter(function (tweet) {
        if (content == 1) {
          return a.includes(tweet.id)
        } else if (content == 2) {
          return !a.includes(tweet.id)
        } else {
          return tweet
        }
      })
    },
  },
  methods: {
    // スクロール時の動作
    infiniteHandler(dispListId) {
      this.processing = true
      const fetchOldTweet = this.tweets[this.tweets.length - 1]

      const reqSinceTweetID = fetchOldTweet.retweetId
        ? fetchOldTweet.retweetId
        : fetchOldTweet.id

      TwitterStore.fetchListTweets({
        id: dispListId,
        sinceTweetID: reqSinceTweetID,
      }).then((data) => {
        data.forEach((tweet) => {
          if (fetchOldTweet.id !== tweet.id) {
            this.tweets.push(tweet)
          }
        })

        if (data.length == 1) {
          //alert('これ以上取得できません')
          this.show = false
          this.$refs.infiniteLoading.stateChanger.complete()
        } else {
          this.$refs.infiniteLoading.stateChanger.loaded()
        }

        this.processing = false
      })
    },

    fetchNewTweets(dispListId) {
      this.processing = true
      const fetchOldTweet = this.tweets[this.tweets.length - 1]

      const reqSinceTweetID = fetchOldTweet.retweetId
        ? fetchOldTweet.retweetId
        : fetchOldTweet.id

      TwitterStore.fetchListTweets({
        id: dispListId,
        sinceTweetID: reqSinceTweetID,
      }).then((data) => {
        data.forEach((tweet) => {
          if (fetchOldTweet.id !== tweet.id) {
            this.tweets.push(tweet)
          }
        })

        if (data.length == 1) {
          //alert('これ以上取得できません')
          this.show = false
        }

        this.processing = false
      })
    },

    handleScroll: function () {
      this.scrollY = window.scrollY
    },

    async classifyImage(tweetId, imgEl) {
      const model = await nsfwjs.load()

      // Classify the image
      const predictions = await model.classify(imgEl)

      let scoreDrawing = 0.0
      let scoreNeutral = 0.0
      let scoreHentai = 0.0

      predictions.forEach((prediction) => {
        switch (prediction.className) {
          case 'Drawing':
            // 「条件の値」 が 「値1」 と等しいときの処理
            scoreDrawing = prediction.probability
            break
          case 'Neutral':
            // 「条件の値」 が 「値2」 と等しいときの処理
            scoreNeutral = prediction.probability
            break
          case 'Hentai':
            // 「条件の値」 が 「値3」 と等しいときの処理
            scoreHentai = prediction.probability
            break
          default:
            break
        }
      })

      if (scoreDrawing > 0.2) {
        this.drawingTweets.push(tweetId)
      } else if (scoreNeutral < 0.9) {
        this.drawingTweets.push(tweetId)
      } else {
        console.log('scoreDrawing' + scoreDrawing)
        console.log('scoreNeutral' + scoreNeutral)
        console.log(imgEl.src)
      }

      if (scoreHentai > 0.5) {
        this.nsfwTweets.push(tweetId)
      }

      this.classifyImageDone.push(tweetId)
    },
  },

  // fetch メソッドは、ページがレンダリングされる前に実行される。データをストアvuexに入れる
  async fetch() {
    if (process.server) {
    }

    if (process.client) {
      if (this.dispListId == 'home') {
      } else {
        let fetchTweets = await TwitterStore.fetchListTweets({
          id: this.dispListId,
        })
        console.log('fetch new Tweets')

        TwitterStore.addNewListTweets({
          listId: this.dispListId,
          tweets: fetchTweets,
        })

        this.tweets = fetchTweets

        // NSFWJSの処理
        fetchTweets.forEach((element) => {
          const media = element.media
          if (media.mediaType === 'photo') {
            const url = media.url[0]
          }
        })
      }
    }
  },

  watch: {
    scrollY: function () {
      let bottom = document.body.scrollHeight - document.body.clientHeight
      if (bottom <= this.scrollY) {
        // TODO スクロールで新規ツイートフェッチしてくるよう修正
        //this.fetchNewTweets()
      }
    },

    tweets: function (newValue, oldValue) {
      if (this.mounted) {
        newValue.forEach((tweet) => {
          if (!this.classifyImageDone.includes(tweet.id)) {
            let imgElement = document.createElement('img')
            imgElement.src = tweet.media.url[0]
            imgElement.crossOrigin = 'anonymous'
            imgElement.width = 400
            imgElement.height = 400

            this.classifyImage(tweet.id, imgElement)
          }
        })
      }
    },
    dispContent: function (newValue, oldValue) {
      //alert('変更されました')
    },
  },

  beforeCreate: function () {
    //console.log(' image List -beforeCreate')
  },
  created: function () {
    //console.log(' image List -created')
    //this.dispContent = DispSettingsStore.getDispContent
  },
  beforeMount: function () {
    //console.log(' image List beforeMount')
  },
  async mounted(context) {
    this.mounted = true
    let message = 'Hello Vue.js!'
    // コンソールにログを出力します。

    this.$nextTick(function () {
      // nextTickを使用してコンソールにログを出力します。
      console.log('dddkjk')
    })
  },
}
</script>
