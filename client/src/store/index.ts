import Vue from 'vue'
import Vuex from 'vuex'
import { IAppState } from './modules/app'
import { IUserMeState } from './modules/me'
import { ITagsViewState } from './modules/tags-view'
import { IErrorLogState } from './modules/error-log'
import { IPermissionState } from './modules/permission'
import { ISettingsState } from './modules/settings'
import { IUsersState } from "@/store/modules/users"
import { IRolesState } from "@/store/modules/roles"

Vue.use(Vuex);

export interface IRootState {
  app: IAppState
  userMe: IUserMeState
  tagsView: ITagsViewState
  errorLog: IErrorLogState
  permission: IPermissionState
  settings: ISettingsState
  users: IUsersState
  roles: IRolesState
}

// Declare empty store first, dynamically register all modules later.
export default new Vuex.Store<IRootState>({})
