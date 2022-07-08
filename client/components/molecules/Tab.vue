<template>
  <div>
    <v-card elevation="0">
      <v-tabs grow show-arrows>
        <v-tab
          v-for="list in listArray"
          :key="list.id"
          @click="changeTab(list.id)"
        >
          {{ list.name }}
        </v-tab>

        <v-menu v-if="listArray.length" bottom left>
          <template v-slot:activator="{ on, attrs }">
            <v-btn text class="align-self-center mr-4" v-bind="attrs" v-on="on">
              <v-icon right> mdi-menu-down </v-icon>
            </v-btn>
          </template>
        </v-menu>

        <v-tab-item v-for="list in listArray" :key="list.id">
          <!-- style="verflow-y: scroll; overflow-x: hidden; height: 800px" -->
          <MoleculesImageList
            v-bind:dispListId="list.id"
            v-bind:classifyModel="classifyModel"
            v-bind:dispContent="dispContent"
          />
        </v-tab-item>
      </v-tabs>
    </v-card>
  </div>
</template>

<script>
import { TwitterStore } from '~/store'
import ImageList from './ImageList.vue'
import * as nsfwjs from 'nsfwjs'
export default {
  data() {
    return {
      currentSelectListId: 'home',
      listArray: [],
      userList: [],
      classifyModel: null,
    }
  },
  components: {
    ImageList,
  },
  props: {
    dispContent: {
      type: String,
      default: '0',
      required: true,
    },
  },

  methods: {
    changeTab: function (tabId) {
      this.currentSelectListId = tabId
    },
    async initNSFWJS() {
      console.log('called calssfy')
      // TODO modelを事前に読み込みするよう修正
      console.log('load model  classifyImgae')
      const model = await nsfwjs.load()
      this.classifyModel = model
      console.log('load end model  classifyImgae')
    },
  },

  asyncData() {
    //console.log('asyncData')
  },

  async fetch() {
    await TwitterStore.updateLists({ user_name: '' })
  },

  // watch プロパティ
  watch: {
    currentSelectListId: function (newVal, oldVal) {
      TwitterStore.setCurrentDispList(newVal)
    },
  },

  async created() {
    if (process.client) {
      TwitterStore.setCurrentDispList(this.currentSelectListId)
      this.initNSFWJS()
    }
  },

  mounted() {
    //ハイドレーションエラー回避のためmountedで実行
    //this.listArray.push({ id: 'home', name: 'home' })
    const lists = TwitterStore.getLists
    lists.forEach((list) => {
      // TODO localStoragにある表示設定を見て画面表示対象のみ
      const listId = list['ID']
      const listName = list['Name']
      if (
        listId == '1115171542042734592' ||
        listId == 'ss' ||
        listId == 'ssss'
      ) {
        //this.listArray.push({ id: listId, name: listName })
      }
      this.listArray.push({ id: listId, name: listName })
    })
  },
}
</script>
