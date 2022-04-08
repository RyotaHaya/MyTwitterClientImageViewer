<template>
  <v-container>
    <v-row justify="center">
      <v-col sm="12" md="5">
        <h2 class="text-center subtitle-1 font-weight-bold mb-2">
          ログイン画面
        </h2>
        <v-row>
          <v-col>
            <!-- <v-divider class="my-8" />
            <v-alert
              v-if="socialLoginErrorMsg"
              dense
              text
              type="error"
              dismissible
            >
              {{ socialLoginErrorMsg }}
            </v-alert> -->
            <SocialLogin />
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import SocialLogin from '~/components/atoms/SocialLogin.vue'
//import SocialLoginava from "~/components/Avatar.vue"
import Vue from 'vue'

export default Vue.extend({
  data() {
    return {
      text: '',
    }
  },
  components: {
    SocialLogin,
  },
  created() {
    console.log('created')

    const age = this.$accessor.age.age
    console.log(age)
    this.$accessor.age.hoge()
  },
})
</script>
