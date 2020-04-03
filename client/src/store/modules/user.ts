import { Action, getModule, Module, Mutation, VuexModule } from 'vuex-module-decorators';
import { getUserMe, getUserRoles, login, logout } from '@/api/users';
import { getToken, removeToken, setToken } from '@/utils/cookies';
import store from '@/store';
import { IUser, IRole } from '@/api/types';

export interface IUserState {
  token: string
  user: IUser | undefined;
  roles: IRole[] | [];
}

@Module({ dynamic: true, store, name: 'user' })
class User extends VuexModule implements IUserState {
  public token = getToken() || '';
  public user: IUser | undefined;
  public roles: IRole[] = [];

  @Mutation
  private SET_TOKEN(token: string) {
    this.token = token;
  }

  @Mutation
  private SET_USER(user: IUser) {
    this.user = user;
  }

  @Mutation
  private SET_ROLES(roles: IRole[]) {
    this.roles = roles;
  }

  @Action
  public async Login(userInfo: { username: string, password: string }) {
    let { username, password } = userInfo;
    username = username.trim();
    const params = new URLSearchParams();
    params.append('username', username);
    params.append('password', password);
    const { data } = await login(params);
    setToken(data.access_token);
    this.SET_TOKEN(data.access_token);
  }

  @Action
  public ResetToken() {
    removeToken();
    this.SET_TOKEN('');
    this.SET_ROLES([]);
  }

  @Action
  public async GetUserMe() {
    if (this.token === '') {
      throw Error('GetUserMe: token is undefined!');
    }
    const { data } = await getUserMe({});
    if (!data) {
      throw Error('Verification failed, please Login again.');
    }
    this.SET_USER(data);
  }

  @Action
  public async GetUserRoles() {
    if (this.token === '') {
      throw Error('GetUserRoles: token is undefined!');
    }
    const { data } = await getUserRoles({});
    if (!data || data.length <= 0) {
      throw Error('GetUserRoles: roles must be a non-null array!');
    }
    this.SET_ROLES(data);
  }

  @Action
  public async LogOut() {
    if (this.token === '') {
      throw Error('LogOut: token is undefined!');
    }
    await logout();
    removeToken();
    this.SET_TOKEN('');
    this.SET_ROLES([]);
  }
}

export const UserModule = getModule(User);
