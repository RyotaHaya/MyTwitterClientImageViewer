<template>
  <v-row justify="center">
    <v-col sm="2">
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

      <v-btn
        block
        class="color-google text-capitalize mb-3"
        @click="googleLogin"
      >
        <span
          class="color-google__icon v-icon notranslate v-icon--left mdi theme--light"
        >
          <svg
            enable-background="new 0 0 46 46"
            viewBox="0 0 46 46"
            xmlns="http://www.w3.org/2000/svg"
          >
            <g transform="translate(14 14)">
              <g clip-rule="evenodd" fill-rule="evenodd">
                <path
                  d="m31.1 9.5c0-1.6-.1-3.2-.4-4.7h-21.7v8.9h12.4c-.5 2.9-2.2 5.3-4.6 6.9v5.8h7.4c4.4-4 6.9-9.9 6.9-16.9z"
                  fill="#4285f4"
                />
                <path
                  d="m9 32c6.2 0 11.4-2.1 15.2-5.6l-7.4-5.8c-2.1 1.4-4.7 2.2-7.8 2.2-6 0-11.1-4-12.9-9.5h-7.7v6c3.8 7.5 11.6 12.7 20.6 12.7z"
                  fill="#34a853"
                />
                <path
                  d="m-3.9 13.4c-.4-1.4-.7-2.9-.7-4.4s.3-3 .7-4.4v-6h-7.7c-1.5 3.2-2.4 6.7-2.4 10.4s.9 7.2 2.4 10.3z"
                  fill="#fbbc05"
                />
                <path
                  d="m9-4.9c3.4 0 6.4 1.2 8.8 3.4l6.6-6.5c-4-3.7-9.2-6-15.4-6-9 0-16.8 5.2-20.6 12.7l7.7 6c1.8-5.5 6.9-9.6 12.9-9.6z"
                  fill="#ea4335"
                />
              </g>
              <path d="m-14-14h46v46h-46z" fill="none" />
            </g>
          </svg>
        </span>
        Googleアカウントでログイン
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
    twitterLogin: function (err: any) {
      AuthorizationStore.signInWithTwitter()
        .then((result) => {
          if (result) {
            AuthorizationStore.setAccessCookieToken({
              token: result['token'],
              token_secret: result['token_secret'],
            })
          }

          let auth_token: CookieParam = {
            key: 'auth_token',
            value: 'auth_token_value',
          }
          AuthorizationStore.setCookieHttpOnly(auth_token)
          window.location.href = 'http://localhost:3000'
          // this.$router.push({
          //   name: 'index',
          // })
        })
        .catch((err) => {
          this.$router.push({
            name: 'error',
          })
        })
    },
    googleLogin: function (err: any) {
      alert('Googlelogin called')
      AuthorizationStore.signInWithGoogle()
        .then(() => {
          window.location.href = 'http://localhost:3000'
          // this.$router.push({
          //   name: 'index',
          // })
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
