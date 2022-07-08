import { Module, VuexModule, Mutation, Action } from 'vuex-module-decorators'
import { $axios } from '~/utils/api'
@Module({
  name: 'disp-settings',
  stateFactory: true,
  namespaced: true,
})
export default class DispSettings extends VuexModule {
  dispContent: String = '0'
  inputText: String = ''

  public get getDispContent() {
    return this.dispContent
  }

  public get getInputText() {
    return this.inputText
  }

  @Action({ rawError: true })
  public async testActionCall() {
    console.log('testActionCall')
  }

  @Mutation
  setDispContent(content: String) {
    this.dispContent = content
  }

  // @Action({ rawError: true })
  // public async createTodo(payload: Todo) {
  //   const { data } = await $axios.post<Todo>('/api/todo', payload)
  //   this.add(data)
  // }

  // @Action({ rawError: true })
  // async deleteTodo(id: Number) {
  //   await $axios.delete(`/api/todo/${id}`)
  //   this.remove(id)
  // }
}
