import { TimelineRepository } from '~/api/twitter/TimelineRepository'
import { UserListRepository } from '~/api/twitter/UserListRepository'
import { Authentication } from '~/api/core/Authentication'
import { Plugin } from '@nuxt/types'

let $repositories: Repositories
export interface Repositories {
  twitterTimeline: TimelineRepository
  userListRepository: UserListRepository
  authentication: Authentication
}

const repositories: Plugin = (context, inject) => {
  const twitterTimeline = new TimelineRepository(context.$axios)
  const userListRepository = new UserListRepository(context.$axios)
  const authentication = new Authentication(context.$axios)

  const repositories: Repositories = {
    twitterTimeline,
    userListRepository,
    authentication,
  }

  $repositories = repositories

  inject('repositories', repositories)
}

export default repositories
export { $repositories }
