<template>
  <v-row justify="center">
    <v-col sm="12">
      <v-btn
        block
        class="color-twitter text-capitalize mb-3"
        @click="twitterLogin"
      >
        <v-icon left class="color-twitter__icon" size="22">
          mdi-twitter
        </v-icon>
        Twitterアカウントでログイン
      </v-btn>
    </v-col>
  </v-row>
</template>

<style lang="scss" scoped>
@mixin social_button($brand-color: #999, $text-color: #fff) {
  background-color: $brand-color !important;
  border-color: $brand-color;
  color: $text-color;

  @at-root {
    #{&}__icon {
      position: absolute;
      left: 0;
    }
  }
}

.color-twitter {
  @include social_button(#1da1f2);
}
.color-google {
  @include social_button(#fff, #757575);
  @at-root {
    #{&}__icon > svg {
      position: absolute;
    }
  }
}
</style>

<script lang="ts">
import Vue from 'vue'
import { AuthorizationStore } from '~/store'

export default Vue.extend({
  methods: {
    twitterLogin() {
      AuthorizationStore.signInWithTwitter()
        .then((result) => {
          //console.log('Firebaseログインに成功')
          // Cookieを設定
          if (result) {
            AuthorizationStore.setAccessCookieToken({
              token: result['token'],
              token_secret: result['token_secret'],
            }).then((result) => {
              //console.log('api実行後に処理')
              //homeページに遷移
              this.$router.push({
                name: 'home',
              })
            })
          }
          //console.log('api実行前に処理')
          // Vuexに設定
          AuthorizationStore.setAccessToken({
            token: result['token'],
            secret: ['token_secret'],
          })
        })
        .catch((err) => {
          alert(err)
          this.$router.push({
            name: 'error',
          })
        })
    },
  },
})
</script>
