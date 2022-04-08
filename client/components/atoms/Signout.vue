<template>
  <v-row justify="center">
    <v-btn color="primary" dark @click.stop="dialog = true"> Sign Out </v-btn>

    <v-dialog v-model="dialog" max-width="290">
      <v-card>
        <v-card-title class="text-h5"> ログアウトしますか？ </v-card-title>

        <v-card-text>
          このアカウントにのみ適用されます。他のアカウントにはログインしたままです。
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>

          <v-btn color="green darken-1" text @click="dialog = false">
            いいえ
          </v-btn>

          <v-btn color="green darken-1" text @click="signOut"> はい </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>
<script lang="ts">
import Vue from 'vue'
import { AuthorizationStore, TwitterStore } from '~/store'
export default Vue.extend({
  data() {
    return {
      dialog: false,
    }
  },
  methods: {
    signOut: function () {
      //redirect('/todo')
      AuthorizationStore.signOut()
        .then(() => {
          // 再リロードしてSSR時のmiddlewareを呼び出しする。
          //location.reload()
        })
        .catch((err) => {
          console.log('login falild')
          this.$router.push({
            name: 'error',
          })
        })
    },
  },
})
</script>
