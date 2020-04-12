import { VuexModule, Module, Action, Mutation, getModule } from 'vuex-module-decorators'
import {getUserMe, getUserMeRoles, getUserMeShops, updateUserMe, updateUserMeShops} from '@/api/me';
import { login, logout, register } from '@/api/auth';
import { getToken, setToken, removeToken } from '@/utils/cookies'
import router, { resetRouter } from '@/router'
import { TagsViewModule } from './tags-view'
import store from '@/store'
import { IRoleData, IUserData, IUserUpdate, IShopData } from '@/api/types';

export interface IUserMeState {
  user: IUserData;
  token: string
  roles: IRoleData[]
}

@Module({ dynamic: true, store, name: 'me' })
class UserMe extends VuexModule implements IUserMeState {
  public token = getToken() || '';
  public user: IUserData = {} as IUserData;
  public roles: IRoleData[] = [];
  public shops: IShopData[] = [];

  // Returns an array of the current roles
  get role_names() {
    return this.roles.map(a => a.name);
  }

  // Returns array of shop ids
  get shop_ids() {
    return this.shops.map(a => a.id)
  }

  @Mutation
  private SET_TOKEN(token: string) {
    this.token = token
  }

  @Mutation
  private SET_USER(user: IUserData) {
    this.user = user;
  }

  @Mutation
  private SET_USER_ROLES(roles: IRoleData[]) {
    this.roles = roles
  }

  @Mutation
  private SET_USER_SHOPS(shops: IShopData[]) {
    this.shops = shops
  }

  @Action({ rawError: true })
  public async Login(userInfo: { username: string, password: string }) {
    const { username, password } = userInfo;

    const params = new URLSearchParams({
     'grant_type': 'password',
      'username': username.trim(),
      'password': password
    });

    const resp = await login(params);
    setToken(resp.data.access_token);
    this.SET_TOKEN(resp.data.access_token);
  }

  @Action
  public async LogOut() {
    if (this.token === '') {
      throw Error('LogOut: token is undefined!')
    }
    await logout();
    removeToken();
    resetRouter();

    // Reset visited views and cached views
    TagsViewModule.delAllViews();
    this.SET_TOKEN('');
    this.SET_USER_ROLES([])
  }

  @Action
  public ResetToken() {
    removeToken();
    this.SET_TOKEN('');
    this.SET_USER_ROLES([])
  }

  @Action
  public async GetUserMe() {
    if (this.token === '') {
      throw Error('GetUserInfo: token is undefined!')
    }
    const { data } = await getUserMe();
    if (!data) {
      throw Error('Verification failed, please Login again.')
    }
    this.SET_USER(data);
  }

  @Action
  public async GetUserMeRoles() {
    const { data } = await getUserMeRoles({});
    if (!data || data.length <= 0) {
      throw Error('GetUserMeRoles: roles must be a non-null array!');
    }
    this.SET_USER_ROLES(data);
  }

  @Action({ rawError: true })
  public async UpdateUserMe(updateData: IUserUpdate) {
    const { data } = await updateUserMe(updateData);
    this.SET_USER(data)
  }

  @Action
  public async GetUserMeShops() {
    const { data } = await getUserMeShops({});
    this.SET_USER_SHOPS(data)
  }

  @Action
  public async UpdateUserMeShops(shopIds: Array<number>) {
    const { data } = await updateUserMeShops(shopIds);
    this.SET_USER_SHOPS(data)
  }

}

export const UserMeModule = getModule(UserMe);
