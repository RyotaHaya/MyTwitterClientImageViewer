<template>
  <v-app id="inspire">
    <v-container>
      <v-row justify="center">
        <v-col sm="12" md="5">
          <h2 class="text-center subtitle-1 font-weight-bold mb-2">
            topページ
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
              <AtomsPageMoveButton />
              <AtomsTwitterLoginButton />
            </v-col>
          </v-row>
        </v-col>
      </v-row>
    </v-container>
  </v-app>
</template>

<script>
import SocialLogin from '~/components/atoms/SocialLogin.vue'
import store from '@/store'
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
  asyncData() {
    console.log('asyncData / server: ' + process.server)
  },
  fetch() {
    console.log('fetch / server: ' + process.server)
  },
  beforeCreate() {
    console.log('beforeCreate / server: ' + process.server)
  },
  created() {
    console.log('created / server: ' + process.server)
  },
  beforeMount() {
    console.log('beforeMount / server: ' + process.server)
  },
  mounted() {
    console.log('mounted / server: ' + process.server)
  },
}
</script>
