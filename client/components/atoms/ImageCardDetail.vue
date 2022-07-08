<template>
  <div>
    <div v-if="!imageMultiple">
      <v-img
        :src="mediaUrls[0] + '?format=jpg&name=large'"
        class="white--text align-end v-img-radius"
        contain
        height="500"
      >
        <template v-slot:placeholder>
          <v-row class="fill-height ma-0" align="center" justify="center">
            <v-progress-circular
              indeterminate
              color="blue lighten-5"
            ></v-progress-circular>
          </v-row>
        </template>
      </v-img>
    </div>
    <div v-else>
      <v-carousel :show-arrows="imageMultiple" touchlesstrue="true">
        <v-carousel-item v-for="(url, i) in mediaUrls" :key="i">
          <a v-bind:href="url + '?format=jpg&name=small'" target="_blank">
            <v-img
              :src="url + '?format=jpg&name=small'"
              :lazy-src="url + '?format=jpg&name=small'"
              class="white--text align-end"
              contain
              height="500"
            >
            </v-img>
          </a>
        </v-carousel-item>
      </v-carousel>
    </div>

    <v-card-title> </v-card-title>

    <v-card-text class="text-justify">
      {{ text }}
    </v-card-text>
    <v-card-actions>
      <v-list-item class="grow">
        <v-row align="center" justify="end">
          <v-btn
            icon
            x-large
            v-bind:href="
              'https://twitter.com/' + user.screenName + '/status/' + tweetId
            "
            target="_blank"
          >
            <v-icon> mdi-twitter </v-icon>
          </v-btn>

          <v-btn icon x-large @click="like">
            <lottie
              :options="defaultOptions"
              :height="80"
              :width="80"
              v-on:animCreated="handleAnimation"
              class="like"
            />
          </v-btn>
          <v-btn icon x-large @click="downloadImages">
            <v-icon>mdi-download</v-icon>
          </v-btn>
        </v-row>
      </v-list-item>
    </v-card-actions>
    <br />
  </div>
</template>
<style scoped>
.like {
  padding-top: 0.2em;
  padding-right: 0.2em;
  display: inline-block;
  text-align: left;
}
</style>
<script>
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
      profileImgaeUrl: '',
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
    tweetInfo: {
      type: Object,
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
      console.log(this.mediaUrls)
      for (const [index, url] of this.mediaUrls.entries()) {
        let charIndex = url.indexOf('.')
        // png or jpg
        const extension = url.slice(-3)

        this.downloadImage(
          `${url}?format=${extension}&name=orig`,
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
    this.tweetId = this.tweetInfo.id
    this.retweetdId = this.tweetInfo.retweetdId
    // 短縮URL部分をリネーム
    console.log(this.tweetInfo.text)
    this.text = this.tweetInfo.text.substring(
      0,
      this.tweetInfo.text.indexOf('https:')
    )

    console.log(this.text)
    this.mediaType = this.tweetInfo.media.mediaType
    this.mediaUrls = this.tweetInfo.media.url
    this.user = this.tweetInfo.user
    const tempProfileImgaeUrl = this.user.profileImageUrl
    this.profileImgaeUrl = tempProfileImgaeUrl.replace(
      'normal.jpg',
      '200x200.jpg'
    )

    this.imageMultiple = this.mediaUrls.length > 1
    this.favorited = this.tweetInfo.favorited
    console.log(this.user)
  },
  async created() {},
}
</script>
