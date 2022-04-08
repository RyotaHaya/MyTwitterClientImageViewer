import { NuxtAxiosInstance } from '@nuxtjs/axios'

type queryData = {
  q: string | null
}

const resourse = 'api'

export class Authentication {
  private readonly axios: NuxtAxiosInstance
  constructor($axios: NuxtAxiosInstance) {
    this.axios = $axios
  }

  createResource(entity: string) {
    return `${resourse}/${entity}`
  }

  get(data: any, entity: string, id = '') {
    let uri: string
    uri = `${this.createResource(entity)}`

    return this.axios.$get(uri, {})
  }

  post(data: any, entity: string) {
    let uri: string
    uri = `${this.createResource(entity)}`
    return this.axios.$post(uri, data)
  }
}
