<template>
  <div>
    <v-card elevation="1" color="white" max-width="500" max-height="1000">
      <div v-if="(mediaType = 'photo')">
        <v-list-item class="grow">
          <v-list-item-avatar color="grey darken-3">
            <v-img
              class="elevation-6"
              alt=""
              :src="user.profileImageUrl"
            ></v-img>
          </v-list-item-avatar>

          <v-list-item-content>
            <v-list-item-title class="mr-1">{{ user.name }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-dialog v-model="dialog">
          <template v-slot:activator="{ on, attrs }">
            <div v-bind="attrs" v-on="on">
              <div v-if="!imageMultiple">
                <v-img
                  :src="mediaUrls[0] + '?format=jpg&name=small'"
                  class="white--text align-end"
                  aspect-ratio="1.7"
                  contain
                  max-height="200px"
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
                <p></p>
              </div>
              <div v-else>
                <v-container fluid>
                  <v-row dense>
                    <v-col v-for="(url, i) in mediaUrls" :key="i" cols="6">
                      <v-card color="white" max-width="500" max-height="400">
                        <v-img
                          :src="url + '?format=jpg&name=small'"
                          :lazy-src="url + '?format=jpg&name=small'"
                          class="white--text align-end"
                          gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)"
                          height="50"
                          width="100"
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
                      </v-card>
                      <div v-if="mediaUrls.length < 3">
                        <p></p>
                      </div>
                    </v-col>
                  </v-row>
                  <br />
                </v-container>
              </div>
            </div>
          </template>

          <v-card>
            <v-carousel
              hide-delimiters
              :show-arrows="imageMultiple"
              max-height="600"
              max-width="600"
            >
              <v-carousel-item v-for="(url, i) in mediaUrls" :key="i">
                <a v-bind:href="url + '?format=jpg&name=small'" target="_blank">
                  <v-img
                    :src="url + '?format=jpg&name=small'"
                    :lazy-src="url + '?format=jpg&name=small'"
                    class="white--text align-end"
                    aspect-ratio="1.7"
                    max-height="500"
                    contain
                  >
                  </v-img>
                </a>
              </v-carousel-item>
            </v-carousel>

            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="primary" text @click="dialog = false">
                close
              </v-btn>
            </v-card-actions></v-card
          >
        </v-dialog>
        <v-card-text class="text-body-2 font-weight"> </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>

          <v-btn icon>
            <v-icon>mdi-heart</v-icon>
          </v-btn>

          <v-btn icon>
            <v-icon>mdi-bookmark</v-icon>
          </v-btn>

          <v-btn icon>
            <v-icon>mdi-share-variant</v-icon>
          </v-btn>
          <v-btn
            icon
            v-bind:href="
              'https://twitter.com/' + user.screenName + '/status/' + tweetId
            "
            target="_blank"
          >
            <v-icon large left> mdi-twitter </v-icon>
          </v-btn>
        </v-card-actions>
      </div>
    </v-card>
  </div>
</template>
<script>
import * as nsfwjs from 'nsfwjs'

export default {
  data() {
    return {
      tweetId: '',
      text: '',
      mediaType: '',
      mediaUrls: [],
      user: null,
      dialog: false,
      imageMultiple: false,
      imgElement: null,
      isDrawing: true,
      isNsfw: false,
      predictions: null,
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
      this.dialog = true
      // 逆にfalseにすれば閉じるを実装できる
    },

    async classifyImage(imgEl) {
      //console.log('called calssfy')
      // TODO modelを事前に読み込みするよう修正
      nsfwjs
        .load()
        .then((model) => {
          // Classify the image

          return model.classify(imgEl)
        })
        .then((predictions) => {
          this.predictions = predictions

          predictions.forEach((prediction) => {
            if (prediction.className == 'Hentai') {
              if (prediction.probability > 0.1) {
                this.isNsfw = true
              }
            }
            if (prediction.className == 'Neutral') {
              if (prediction.probability > 0.2) {
                this.isDrawing = false
              }
            }
          })
        })
    },
  },
  async fetch() {
    this.tweetId = this.tweet.id
    // 短縮URL部分をリネーム
    this.text = this.tweet.text.substring(0, this.tweet.text.indexOf('https:'))
    this.mediaType = this.tweet.media.mediaType
    this.mediaUrls = this.tweet.media.url
    this.user = this.tweet.user
    this.imageMultiple = this.mediaUrls.length > 1

    // NSFWJS処理用に作成
    let imgElement = document.createElement('img')
    imgElement.src = this.tweet.media.url[0]
    imgElement.crossOrigin = 'anonymous'
    imgElement.width = 500
    imgElement.height = 500
    this.imgElement = imgElement
  },
  async created() {},

  mounted(context) {
    //this.classifyImage(this.imgElement)
  },
}
</script>
<style>
.SampleEvent {
  background-color: #00a656;
  border-radius: 1em;
  box-shadow: 0 0.2em 0.5em rgba(0, 0, 0, 0.2);
  padding: 1em 2em;
  color: #ffffff;
  font-weight: bold;
  text-decoration: none;
}
</style>
