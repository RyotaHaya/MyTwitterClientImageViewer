<template>
  <v-btn block class="color-twitter text-capitalize mb-3" @click="pageMove">
    ユーザ専用ページへ遷移します
  </v-btn>
</template>

<script lang="ts">
import Vue from 'vue'
import { AuthorizationStore, TwitterStore } from '~/store'
export default Vue.extend({
  methods: {
    pageMove({ redirect }: any) {
      //this.$router.push({ path: `/home` })
      // 暫定的にこれで
      window.location.href = 'http://localhost:3000/home'
    },
  },
})
</script>
