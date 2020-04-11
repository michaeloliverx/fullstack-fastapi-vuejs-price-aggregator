import http from '@/utils/request'
import {IShopData, IShopUpdate, IShopCreate, IShopListings} from './types';

export const getShops = (params: any) =>
  http.request<IShopData[]>({
    url: '/shops',
    method: 'get',
    params
  });

export const createShop = (data: IShopCreate) =>
  http.request<IShopData>({
    url: '/shops',
    method: 'post',
    data
  });

export const updateShop = (id: number, data: IShopUpdate) =>
  http.request<IShopData>({
    url: `/shops/${id}`,
    method: 'put',
    data
  });

export const deleteShop = (id: number) =>
  http.request({
    url: `/shops/${id}`,
    method: 'delete',
  });

export const getShopListings = (params: any) =>
  http.request<IShopListings[]>({
    url: '/shops/listings/',
    method: 'get',
    params
  });
