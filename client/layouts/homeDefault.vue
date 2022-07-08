<template>
  <v-app>
    <!-- インターネット接続チェック-->
    <div v-if="$nuxt.isOffline"><!-- オフライン時の処理--></div>
    <!--
    <v-navigation-drawer app>
     
    </v-navigation-drawer>
    -->

    <v-app-bar color="primary" dense dark elevate-on-scroll>
      <v-app-bar-nav-icon></v-app-bar-nav-icon>
      <div class="ml-5"><AtomsAvatar /></div>
      <v-spacer></v-spacer>

      <div><v-toolbar-title></v-toolbar-title></div>

      <v-spacer></v-spacer>

      <v-spacer></v-spacer>

      <v-btn icon>
        <v-icon>mdi-heart</v-icon>
      </v-btn>

      <v-btn icon>
        <v-icon>mdi-magnify</v-icon>
      </v-btn>
      <AtomsLogoutButton />
    </v-app-bar>
    <!-- アプリケーションのコンポーネントに基づいてコンテンツのサイズを決定 -->

    <v-main>
      <v-container>
        <Nuxt />
      </v-container>
    </v-main>

    <v-footer app>
      <!-- -->
    </v-footer>
  </v-app>
</template>
<style></style>
>
<script>
import { AuthorizationStore } from '~/store'
export default {
  data() {
    return {
      clipped: false,
      drawer: false,
      fixed: false,
      items: [
        {
          icon: 'mdi-apps',
          title: 'Welcome',
          to: '/',
        },
        {
          icon: 'mdi-chart-bubble',
          title: 'Inspire',
          to: '/inspire',
        },
      ],
      miniVariant: false,
      right: true,
      rightDrawer: false,
      title: 'Vuetify.js',
    }
  },
  methods: {
    alertOffLine: function () {
      alert('インターネットに接続されていません')
    },
  },

  beforeCreate: function () {
    // Cookie送信必須
    if (process.client) {
      // ログイン済みかCookieの内容からチェックする
      AuthorizationStore.loginCheck()
        .then((result) => {
          if (result == undefined) {
            AuthorizationStore.clearCookie()
            // this.$router.push({
            //   name: 'login',
            // })
          }
        })
        .catch((err) => {
          console.log('not login falild')
          // this.$router.push({
          //   name: 'login',
          // })
        })
    }
  },
}
</script>
