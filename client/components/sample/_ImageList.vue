<template>
  <div v-if="tweets.length > 0">
    <keep-alive>
      <div class="infinite-scroll">
        <div class="infinite-scroll-list">
          <v-row>
            <v-col
              v-for="tweet in tweets"
              :key="tweet.ID"
              cols="12"
              xs="6"
              sm="6"
              md="4"
              lg="4"
              xl="4"
            >
              <v-card class="mx-auto" max-width="500">
                <template slot="progress">
                  <v-progress-linear
                    color="deep-purple"
                    height="10"
                    indeterminate
                  ></v-progress-linear>
                </template>

                <a v-bind:href="tweet.MediaUrls[0]" target="_blank">
                  <v-img
                    :src="tweet.MediaUrls[0] + '?format=jpg&name=small'"
                    :lazy-src="tweet.MediaUrls[0] + '?format=jpg&name=small'"
                    aspect-ratio="1"
                    class="blue lighten-5"
                    max-height="300"
                    max-width="500"
                  >
                    <template v-slot:placeholder>
                      <v-row
                        class="fill-height ma-0"
                        align="center"
                        justify="center"
                      >
                        <v-progress-circular
                          indeterminate
                          color="blue lighten-5"
                        ></v-progress-circular>
                      </v-row>
                    </template>
                  </v-img>
                </a>

                <v-row align="center" class="mx-0">
                  <div class="ma-4" style="float: letf">
                    <a
                      v-bind:href="
                        'https://twitter.com/' + tweet.User.UserScreenName
                      "
                      target="_blank"
                    >
                      <v-avatar color="grey darken-1 shrink" size="32">
                        <img
                          v-bind:src="tweet.User.UserProfileImageUrl"
                          alt="avatarImage"
                          class="avatar-image" /></v-avatar
                    ></a>
                  </div>
                  <div>
                    <v-card-text
                      >{{ tweet.User.UserName }} @{{
                        tweet.User.UserScreenName
                      }}</v-card-text
                    >
                  </div>
                </v-row>

                <v-divider class="mx-4"></v-divider>
                <v-card-text>
                  <!-- <p>TODO TweetTxetをリンク化するメソッドを作る</p> -->
                </v-card-text>

                <v-card-actions> </v-card-actions>
              </v-card>
            </v-col>
          </v-row>
        </div>
        <infinite-loading
          ref="infiniteLoading"
          spinner="spiral"
          @infinite="infiniteHandler(dispListId)"
        >
          <div slot="no-results" />
          ddd
        </infinite-loading>
      </div>
    </keep-alive>
  </div>
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
</template>
<script>
import * as nsfwjs from 'nsfwjs'
import { AuthorizationStore, TwitterStore } from '~/store'

export default {
  data() {
    return {
      getCnt: 30,
      tweets: [],
      listTweets: [],

      lastTweet: [],
      maxCount: 0,
      targetListId: '',
      includeReTweet: true,
      getListTimeLineImagesUrl:
        // 開発時 this.$config.apiURL + '/api/listTimelineMedia'
        // デプロイ時  /api/listTimelineMedia
        this.$config.apiURL + '/api/listTimelineMedia',
    }
  },
  props: {
    listIdArray: {
      type: Array,
      default: () => {},
      required: false,
    },
    dispListId: {
      type: String,
      default: '',
      required: false,
    },
  },
  // fetch メソッドは、ページがレンダリングされる前に実行される。データをストアvuexに入れる
  async fetch() {
    console.log('async fetch')

    // const listIdArray = ["1280477992594993153", "1304418413037498368"];

    // listIdArray.forEach(id => {
    //   console.log("id is " + id);
    //   this.$store.dispatch({
    //     type: "tweet-store/fetchListTweets",
    //     id: id
    //   });
    // });

    console.log('fetch END')

    //this.$store.commit("storeTweets", response.data["ImageTweetList"]);
  },
  beforeMount: function () {
    console.log('beforemoud')
    //this.tweets = this.$store.getters["tweets"];
  },
  mounted: function () {
    console.log(this.dispListId)
    this.tweets = this.$store.getters['tweets']
    //console.log("mouted");
    // const applicationCache = sessionStorage.getItem("my-key");
    // console.log(applicationCache.tweets.length);
    // if (applicationCache.tweets.length > 0) {
    //   this.tweets = cacheTweets;
    // }
  },

  watch: {
    lastTweet: function () {
      console.log('watch')
      //this.$store.commit("storeTweets", this.tweets);
    },
  },

  methods: {
    fetchUserTimeLine() {
      let maxId =
        this.lastTweet.RetweetedID !== ''
          ? this.lastTweet.RetweetedID
          : this.lastTweet.ID
      this.$axios
        .get(this.getListTimeLineImagesUrl, {
          params: {
            // ここにクエリパラメータを指定する
            listId: this.targetListId,
            maxCount: 30,
            include_rts: this.includeReTweet,
            range_count: 200,
            maxId: maxId,
          },
        })
        .then((response) => {
          return response.data['ImageTweetList']
          //this.storeTweets();
        })
        .catch((err) => {
          //リクエスト失敗時
          //alert('request ffe')
        })
    },
    infiniteHandler(listid) {
      console.log(listid)
      if (this.maxCount < 300) {
        let maxId =
          this.lastTweet.RetweetedID !== ''
            ? this.lastTweet.RetweetedID
            : this.lastTweet.ID

        this.$axios
          .get(this.getListTimeLineImagesUrl, {
            params: {
              // ここにクエリパラメータを指定する
              listId: listid,
              maxCount: this.getCnt,
              include_rts: this.includeReTweet,
              range_count: 200,
              maxId: maxId,
            },
          })
          .then((response) => {
            const retTweets = response.data['ImageTweetList']
            if (response.data['TotalCount'] > 0) {
              for (let i = 0; i < response.data['TotalCount']; i++) {
                let t = retTweets[i]
                if (t.ID !== this.lastTweet.ID) {
                  //this.tweets.push(t);
                }
              }

              const preLastTweet = this.lastTweet
              this.lastTweet = retTweets[retTweets.length - 1]
              console.log(
                'preLastTweetId=' +
                  preLastTweet.ID +
                  ' lastTweet.ID=' +
                  this.lastTweet.ID
              )
              if (preLastTweet.ID == this.lastTweet.ID) {
                this.$refs.infiniteLoading.stateChanger.complete()
              }
              this.maxCount += retTweets.length - 1

              this.$refs.infiniteLoading.stateChanger.loaded()
            } else {
              ;<v-alert
                border="left"
                color="red"
                dismissible
                icon="これ以上読み込みできません。"
                outlined
                prominent
                text
                type="info"
              ></v-alert>
              this.$refs.infiniteLoading.stateChanger.complete()
            }
          })
          .catch((err) => {
            //リクエスト失敗時
            //alert('request ffe')
            this.$refs.infiniteLoading.stateChanger.complete()
          })
      }
    },
    storeTweets(tweets) {
      this.$store.commit('storeTweets', tweets)
    },
  },
  beforeCreate: function () {
    console.log('beforeCreate')
  },
  created: function () {
    console.log('created')
    //const listIdArray = ['1280477992594993153', '1304418413037498368']

    TwitterStore.fetchListTweets({ id: '1280477992594993153' })

    // listIdArray.forEach((id) => {
    //   console.log('id is ' + id)
    //   this.$store.dispatch({
    //     type: 'tweet-store/fetchListTweets',
    //     id: id,
    //   })
    // })
  },
  beforeMount: function () {
    console.log('beforeMount')
  },
}
</script>
