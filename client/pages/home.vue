<template>
  <v-app>
    <div v-if="mounted">
      <v-toolbar elevation="0" class="ma-0">
        <v-text-field
          class="mx-9 pt-7"
          placeholder="キーワード検索"
          clearable
          filled
          prepend-inner-icon="mdi-magnify"
          rounded
        ></v-text-field>

        <v-radio-group class="pt-4" mandatory v-model="dispContent" row>
          <v-radio label="全て" value="0"></v-radio>
          <v-radio label="イラスト" value="1"></v-radio>
          <v-radio label="写真" value="2"></v-radio>
        </v-radio-group>

        <v-checkbox class="pt-4" v-model="checkbox" :label="``"></v-checkbox>

        <v-menu bottom left>
          <template v-slot:activator="{ on, attrs }">
            <v-btn icon v-bind="attrs" v-on="on">
              <v-icon>mdi-dots-vertical</v-icon>
            </v-btn>
          </template>

          <v-list>
            <v-list-item v-for="(item, i) in items" :key="i">
              <v-list-item-title>{{ item.title }}</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </v-toolbar>
    </div>

    <MoleculesTab v-bind:dispContent="dispContent" />
  </v-app>
</template>
<style></style>

<script lang="ts">
import Vue from 'vue'
import { DispSettingsStore } from '~/store'
export default Vue.extend({
  layout: 'homeDefault',
  data: () => ({
    items: [
      { title: 'Click Me' },
      { title: 'Click Me' },
      { title: 'Click Me' },
      { title: 'Click Me 2' },
    ],
    mounted: false,
    dispContent: '0',
    checkbox: true,
  }),
  methods: {
    apiTest: function (context: any) {},
    pagemove: function () {
      this.$router.push({ path: `/todo` })
    },
  },
  watch: {
    dispContent: function (content: number) {
      //DispSettingsStore.setDispContent(content)
    },
  },

  created: function () {},
  async asyncData({ app }) {},
  async mounted() {
    this.mounted = true
  },
})
</script>
