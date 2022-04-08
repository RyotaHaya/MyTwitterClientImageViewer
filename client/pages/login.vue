<template>
  <v-app id="inspire">
    <v-container>
      <v-row justify="center">
        <v-col sm="12" md="5">
          <h2 class="text-center subtitle-1 font-weight-bold mb-2">
            ログイン画面
          </h2>
          <v-row>
            <v-col>
              <v-divider class="my-8" />
              <v-alert
                v-if="socialLoginErrorMsg"
                dense
                text
                type="error"
                dismissible
              >
                {{ socialLoginErrorMsg }}
              </v-alert>
              <SocialLogin />
            </v-col>
          </v-row>
        </v-col>
      </v-row>
    </v-container>
  </v-app>
</template>

<script>
import SocialLogin from '~/components/atoms/SocialLogin.vue'
import { AuthorizationStore } from '~/store'

export default {
  layout: 'dummy',
  components: {
    SocialLogin,
  },
  data: function () {
    return {
      tab: null,
      login_valid: true,
      login_email: '',
      login_password: '',
      show_loginpassword: false,
      loginErrorMsg: '',
      socialLoginErrorMsg: '',
    }
  },
  beforeCreate: function () {
    console.log('login breforeCreate')
    console.log(AuthorizationStore.isAuthenticated)

    if (AuthorizationStore.isAuthenticated) {
      console.log('login aaaaaaa')
      // this.$router.push({
      //   name: 'index',
      // })
    }
  },
}
</script>
