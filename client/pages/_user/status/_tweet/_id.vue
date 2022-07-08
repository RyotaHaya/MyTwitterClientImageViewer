<template>
  <v-app>
    <div>
      <v-container>
        <v-text-field
          class="mx-4"
          placeholder="キーワード検索"
          clearable
          filled
          prepend-inner-icon="mdi-magnify"
          rounded
        >
        </v-text-field>
      </v-container>
    </div>

    ここに詳細なツイート情報を掲載します
    <nuxt-link to="/home">戻る-linkのリンク</nuxt-link>
    <button @click="$router.back()">ボタン</button>
  </v-app>
</template>
<style></style>

<script>
import { AuthorizationStore, TwitterStore } from '~/store'
export default {
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
    }
  },

  methods: {
    SampleEvent() {
      alert(`Hello `)
    },
  },
  async fetch() {},
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
