<template>
  <v-btn class="color-twitter text-capitalize mb-3" @click="twitterLogout">
    <v-icon left class="color-twitter__icon" size="22"> mdi-twitter </v-icon>
    ログアウト
  </v-btn>
</template>

<script lang="ts">
import Vue from 'vue'
import { AuthorizationStore } from '~/store'

export default Vue.extend({
  methods: {
    twitterLogout() {
      AuthorizationStore.signOut()
        .then((result) => {
          // Cookieをクリアする
          alert('ログアウトしました。')
          this.$router.push({
            name: 'index',
          })
        })
        .catch((err) => {
          console.log(err)
          alert(err)
          this.$router.push({
            name: 'error',
          })
        })
    },
  },
})
</script>
