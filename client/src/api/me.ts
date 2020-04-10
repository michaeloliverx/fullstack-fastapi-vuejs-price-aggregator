import http from '@/utils/request'
import { IUserData, IRoleData } from './types';

export const getUserMe = (data?: any) =>
  http.request<IUserData>({
    url: '/me',
    method: 'get',
    data
  });

export const getUserMeRoles = (data?: any) =>
  http.request<IRoleData[]>({
    url: '/me/roles',
    method: 'get',
    data
  });


export const updateUserMe = (data: any) =>
  http.request<IUserData>({
    url: '/me',
    method: 'put',
    data
  });
