import {
  Action,
  getModule,
  Module,
  Mutation,
  VuexModule
} from "vuex-module-decorators";
import store from "@/store";
import { getRoles, updateRole, deleteRole, createRole } from "@/api/roles";
import { IRoleData, IRoleCreate, IRoleUpdate } from "@/api/types";

export interface IRolesState {
  roles?: IRoleData[];
}

@Module({ dynamic: true, store, name: "roles" })
class Roles extends VuexModule implements IRolesState {
  public roles: IRoleData[] = [];

  @Mutation
  private SET_ROLES(payload: IRoleData[]) {
    this.roles = payload;
  }

  @Mutation
  private SET_ROLE(payload: IRoleData) {
    const roles = this.roles.filter(
      (role: IRoleData) => role.id !== payload.id
    );
    roles.push(payload);
    this.roles = roles;
  }

  @Mutation
  private DELETE_ROLE(id: number) {
    this.roles = this.roles.filter((user: IRoleData) => user.id !== id);
  }

  @Action
  public async GetRoles(params: any) {
    const { data } = await getRoles(params);
    this.SET_ROLES(data);
  }

  @Action
  public async CreateRole(createData: IRoleCreate) {
    const { data } = await createRole(createData);
    this.SET_ROLE(data);
  }

  @Action
  public async UpdateRole(id: number, updateData: IRoleUpdate) {
    const { data } = await updateRole(id, updateData);
    this.SET_ROLE(data);
  }

  @Action
  public async DeleteRole(id: number) {
    await deleteRole(id);
    this.DELETE_ROLE(id);
  }
}

export const RolesModule = getModule(Roles);
