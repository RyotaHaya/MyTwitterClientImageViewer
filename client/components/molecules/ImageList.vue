<template>
  <v-card class="mx-auto">
    <v-container fluid>
      <div v-if="tweets && tweets.length > 0">
        <div class="infinite-scroll">
          <div class="infinite-scroll-list">
            <v-container fluid>
              <v-row dense>
                <v-col
                  v-for="tweet in tweets"
                  :key="tweet.id"
                  cols="6"
                  xs="12"
                  sm="4"
                  md="3"
                  lg="3"
                  xl="2"
                >
                  <!-- メディア表示 -->
                  <AtomsImageCard
                    v-bind:tweet="tweet"
                    v-bind:parentListId="dispListId"
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
            <span slot="no-more">これ以上読み込みできません。</span>
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
import { TwitterStore } from '~/store'
import ImageCard from '../atoms/ImageCard.vue'
export default {
  data() {
    return {
      getCnt: 30,
      tweets: [],
      filter: '',
      scrollY: 0,
    }
  },
  props: {
    dispListId: {
      type: String,
      default: 'ddd',
      required: false,
    },
  },
  components: {
    // 画像表示用
    ImageCard,
  },

  methods: {
    // スクロール時の動作
    infiniteHandler(listid) {
      this.$refs.infiniteLoading.stateChanger.complete()
      //this.$refs.infiniteLoading.stateChanger.loaded()
      if (this.tweets.length < 50) {
        // const fetchOldTweet = this.tweets[this.tweets.length - 1]
        // this.$refs.infiniteLoading.stateChanger.loaded()
        // TwitterStore.fetchListTweets({
        //   id: this.dispListId,
        //   sinceTweetID: fetchOldTweet.id,
        // }).then((data) => {
        //   data.forEach((tweets) => {
        //     this.tweets.push(tweets)
        //   })
        // })
        //this.$refs.infiniteLoading.stateChanger.loaded()
      } else {
        //this.$refs.infiniteLoading.stateChanger.complete()
      }

      // fetchTweets.forEach((tweets) => {
      //   this.tweets.push(tweets)
      // })

      //this.$refs.infiniteLoading.stateChanger.complete()

      // maxId指定して取得
      // } else {
      //   this.$refs.infiniteLoading.stateChanger.complete()
      // }

      // if (this.maxCount < 300) {
      //   let maxId =
      //     this.lastTweet.RetweetedID !== ''
      //       ? this.lastTweet.RetweetedID
      //       : this.lastTweet.ID

      //   this.$axios
      //     .get(this.getListTimeLineImagesUrl, {
      //       params: {
      //         // ここにクエリパラメータを指定する
      //         listId: listid,
      //         maxCount: this.getCnt,
      //         include_rts: this.includeReTweet,
      //         range_count: 200,
      //         maxId: maxId,
      //       },
      //     })
      //     .then((response) => {
      //       const retTweets = response.data['ImageTweetList']
      //       if (response.data['TotalCount'] > 0) {
      //         for (let i = 0; i < response.data['TotalCount']; i++) {
      //           let t = retTweets[i]
      //           if (t.ID !== this.lastTweet.ID) {
      //             //this.tweets.push(t);
      //           }
      //         }

      //         const preLastTweet = this.lastTweet
      //         this.lastTweet = retTweets[retTweets.length - 1]
      //         console.log(
      //           'preLastTweetId=' +
      //             preLastTweet.ID +
      //             ' lastTweet.ID=' +
      //             this.lastTweet.ID
      //         )
      //         if (preLastTweet.ID == this.lastTweet.ID) {
      //           this.$refs.infiniteLoading.stateChanger.complete()
      //         }
      //         this.maxCount += retTweets.length - 1

      //         this.$refs.infiniteLoading.stateChanger.loaded()
      //       } else {
      //         ;<v-alert
      //           border="left"
      //           color="red"
      //           dismissible
      //           icon="これ以上読み込みできません。"
      //           outlined
      //           prominent
      //           text
      //           type="info"
      //         ></v-alert>
      //         this.$refs.infiniteLoading.stateChanger.complete()
      //       }
      //     })
      //     .catch((err) => {
      //       //リクエスト失敗時
      //       //alert('request ffe')
      //       this.$refs.infiniteLoading.stateChanger.complete()
      //     })
      // }
    },

    fetchNewTweets() {
      // console.log(this)
      // const th = this
      // console.log(th.this)
      // console.log(th.tweets)
      // console.log(th.tweets.length - 1)
      // const fetchOldTweet = th.tweets[th.tweets.length - 1]
      // console.log(fetchOldTweet)
      // TwitterStore.fetchListTweets({
      //   id: th.dispListId,
      //   sinceTweetID: fetchOldTweet.Id,
      // }).then((data) => {
      //   data.forEach((tweets) => {
      //     th.tweets.push(tweets)
      //   })
      // })
    },

    handleScroll: function () {
      this.scrollY = window.scrollY
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
  },

  beforeCreate: function () {
    //console.log(' image List -beforeCreate')
  },
  created: function () {
    //console.log(' image List -created')
  },
  beforeMount: function () {
    //console.log(' image List beforeMount')
  },
  mounted: function () {
    window.addEventListener('scroll', this.handleScroll)
  },
}
</script>
