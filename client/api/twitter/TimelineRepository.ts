import { NuxtAxiosInstance } from '@nuxtjs/axios'

type queryData = {
  q: string | null
}

const resourse = 'api/twitter/timeline'

export class TimelineRepository {
  private readonly axios: NuxtAxiosInstance
  constructor($axios: NuxtAxiosInstance) {
    this.axios = $axios
  }

  createResource(entity: string) {
    return `${resourse}/${entity}`
  }

  get(data: any, entity: string, id = '') {
    let uri: string

    if (id === '') {
      uri = `${this.createResource(entity)}`
    } else {
      uri = `${this.createResource(entity)}/${id}`
    }

    return this.axios.$get(uri, {
      params: { ...data },
    })
  }
}
