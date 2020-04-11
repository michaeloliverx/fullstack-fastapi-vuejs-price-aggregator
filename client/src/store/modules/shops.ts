import {
  Action,
  getModule,
  Module,
  Mutation,
  VuexModule
} from "vuex-module-decorators";
import store from "@/store";
import { getShops, createShop, updateShop, deleteShop } from "@/api/shops";
import { IShopData, IShopCreate, IShopUpdate } from "@/api/types";

export interface IShopsState {
  shops?: IShopData[];
}

@Module({ dynamic: true, store, name: "shops" })
class Shops extends VuexModule implements IShopsState {
  public shops: IShopData[] = [];

  @Mutation
  private SET_SHOPS(payload: IShopData[]) {
    this.shops = payload;
  }

  @Mutation
  private SET_SHOP(payload: IShopData) {
    const shops = this.shops.filter(
      (shop: IShopData) => shop.id !== payload.id
    );
    shops.push(payload);
    this.shops = shops;
  }

  @Mutation
  private DELETE_SHOP(id: number) {
    this.shops = this.shops.filter((shop: IShopData) => shop.id !== id);
  }

  @Action
  public async GetShops(params: any) {
    const { data } = await getShops(params);
    this.SET_SHOPS(data);
  }

  @Action
  public async CreateShop(createData: IShopCreate) {
    const { data } = await createShop(createData);
    this.SET_SHOP(data);
  }

  @Action
  public async UpdateShop(id: number, updateData: IShopUpdate) {
    const { data } = await updateShop(id, updateData);
    this.SET_SHOP(data);
  }

  @Action
  public async DeleteShop(id: number) {
    await deleteShop(id);
    this.DELETE_SHOP(id);
  }
}

export const ShopsModule = getModule(Shops);
