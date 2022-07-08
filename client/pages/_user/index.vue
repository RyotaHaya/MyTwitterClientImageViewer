<template>
  <v-app>
    <div>
      ユーザシングル表示
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
  </v-app>
</template>
<style></style>

<script>
import { AuthorizationStore, TwitterStore } from '~/store'
export default {
  layout: 'homeDefault',
  data: () => ({}),
  methods: {
    apiTest: function (context) {
      TwitterStore.fetchListTweets()
    },
    pagemove: function () {
      //redirect('/todo')
      this.$router.push({ path: `/todo` })
    },
  },

  created: function () {},
  async asyncData({ app }) {},
}
</script>
