import http from '@/utils/request'
import {IUserData, IRoleData, IShopData} from './types';

export const getUserMe = (data?: any) =>
  http.request<IUserData>({
    url: '/me',
    method: 'get',
    data
  });

export const updateUserMe = (data: any) =>
  http.request<IUserData>({
    url: '/me',
    method: 'put',
    data
  });

export const getUserMeRoles = (data?: any) =>
  http.request<IRoleData[]>({
    url: '/me/roles',
    method: 'get',
    data
  });

export const getUserMeShops = (data?: any) =>
  http.request<IShopData[]>({
    url: '/me/shops',
    method: 'get',
    data
  });

export const updateUserMeShops = (data?: any) =>
  http.request<IShopData[]>({
    url: '/me/shops',
    method: 'put',
    data
  });
