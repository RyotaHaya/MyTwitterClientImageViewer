import { NuxtAxiosInstance } from '@nuxtjs/axios'

type queryData = {
  q: string | null
}

const resourse = 'api/twitter/lists'

export class UserListRepository {
  private readonly axios: NuxtAxiosInstance
  constructor($axios: NuxtAxiosInstance) {
    this.axios = $axios
  }

  createResource(entity: string) {
    return `${resourse}/${entity}`
  }

  get(data: any, entity: string) {
    let uri: string
    uri = `${this.createResource(entity)}`

    return this.axios.$get(uri, {})
  }
}
