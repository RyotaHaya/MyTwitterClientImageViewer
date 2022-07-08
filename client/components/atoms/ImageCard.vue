<template>
  <div>
    <v-hover v-slot="{ hover }">
      <v-card :elevation="hover ? 10 : 1" class="mx-auto" max-width="1000">
        <!--ローディングされるまで非表示 -->
        <div v-if="(mediaType = 'photo')">
          <v-card shaped elevation="0" tile>
            <div class="box">
              <v-dialog v-model="dialog" max-width="800">
                <template v-slot:activator="{ on, attrs }">
                  <div v-bind="attrs" v-on="on">
                    <v-img
                      :src="mediaUrls[0] + '?format=jpg&name=small'"
                      :lazy-src="mediaUrls[0] + '?format=jpg&name=small'"
                      class="white--text align-end"
                      gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)"
                      light
                      height="300"
                    >
                      <div v-if="mediaUrls.length > 1">
                        <p>
                          <v-icon color="#ffffff"> mdi-image-multiple</v-icon>
                        </p>
                      </div>
                    </v-img>
                  </div>
                </template>
                <v-card>
                  <v-toolbar dark color="primary" elevation="0">
                    <v-btn icon dark @click="dialog = false">
                      <v-icon>mdi-close</v-icon>
                    </v-btn>
                    <v-list-item class="grow">
                      <v-list-item-avatar color="grey darken-3" size="36">
                        <a
                          v-bind:href="'https://twitter.com/' + user.screenName"
                          target="_blank"
                        >
                          <v-img
                            contain
                            max-height="48"
                            max-width="48"
                            class="elevation-6"
                            alt=""
                            :src="profileImgaeUrl"
                          ></v-img>
                        </a>
                      </v-list-item-avatar>

                      <v-list-item-content>
                        <v-list-item-title class="text-subtitle-1">{{
                          user.name
                        }}</v-list-item-title>
                        <v-list-item-subtitle class="text-subtitle-1"
                          >@{{ user.screenName }}
                        </v-list-item-subtitle>
                      </v-list-item-content>
                    </v-list-item>
                  </v-toolbar>

                  <AtomsImageCardDetail v-bind:tweetInfo="tweet" />
                </v-card>
              </v-dialog>

              <v-spacer></v-spacer>
            </div>
          </v-card>

          <v-list-item class="grow">
            <v-list-item-avatar color="grey darken-3" size="32">
              <a
                v-bind:href="'https://twitter.com/' + user.screenName"
                target="_blank"
              >
                <v-img
                  class="elevation-6"
                  alt=""
                  max-height="36"
                  max-width="36"
                  :src="profileImgaeUrl"
                ></v-img>
              </a>
            </v-list-item-avatar>

            <v-list-item-content>
              <v-list-item-title class="mr-1 text-caption">{{
                user.name
              }}</v-list-item-title>
              <v-list-item-subtitle class="mr-1 text-caption"
                >@{{ user.screenName }}</v-list-item-subtitle
              >
            </v-list-item-content>
          </v-list-item>
        </div>

        <div v-if="isNsfw">これはえっちなやつ</div>
        <div v-if="isDrawing">これはイラスト</div>
      </v-card>
    </v-hover>
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

.v-card.on-hover.theme--dark {
  background-color: rgba(#fff, 0.8);
}

.box {
  position: relative;
}
.box p {
  position: absolute;
  top: 0;
  right: 0;
}

.img-header {
  position: absolute;
  top: 0;
  left: 0;
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
import Lottie from '~/components/atoms/lottie.vue'
import * as animationData from '~/assets/like.json'
import * as nsfwjs from 'nsfwjs'
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
      profileImgaeUrl: '',
      favorited: false,
      dialog: false,
      imageMultiple: false,
      isDrawing: false,
      isNsfw: false,
      predictions: null,
      // アニメーション定義
      defaultOptions: { animationData: animationData },
      animationSpeed: 1,
      anim: null,

      model: 3,
      rounded: ['0', 'sm', 'md', 'lg', 'xl', 'pill', 'circle'],
      loading: true,
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
    classifyModel: {
      type: Object,
      default: null,
      required: false,
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
        //console.log(url)
        //console.log(searchParams)

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
  },
  async fetch() {
    this.tweetId = this.tweet.id
    this.retweetdId = this.tweet.retweetdId
    // 短縮URL部分をリネーム
    this.text = this.tweet.text.substring(0, this.tweet.text.indexOf('https:'))
    this.mediaType = this.tweet.media.mediaType
    this.mediaUrls = this.tweet.media.url
    this.user = this.tweet.user
    const tempProfileImgaeUrl = this.user.profileImageUrl
    this.profileImgaeUrl = tempProfileImgaeUrl.replace(
      'normal.jpg',
      '200x200.jpg'
    )
    this.imageMultiple = this.mediaUrls.length > 1
    this.favorited = this.tweet.favorited
  },
  async created() {},

  async mounted(context) {},

  computed: {
    radius() {
      let rounded = 'rounded'
      const value = this.rounded[this.model]

      return rounded
    },
  },
  watch: {},
}
</script>
