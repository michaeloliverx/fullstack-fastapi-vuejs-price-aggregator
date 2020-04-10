import http from '@/utils/request'
import { IUserData, IUserCreate, IUserUpdate, IRoleData } from './types';

export const getUsers = (params: any) =>
  http.request<IUserData[]>({
    url: '/users',
    method: 'get',
    params
  });

export const createUser = (data: IUserCreate) =>
  http.request({
    url: `/users`,
    method: 'post',
    data
  });

export const updateUser = (id: number, data: IUserUpdate) =>
  http.request({
    url: `/users/${id}`,
    method: 'put',
    data
  });

export const deleteUser = (id: number) =>
  http.request({
    url: `/users/${id}`,
    method: 'delete',
  });

export const getUserRoles = (id: number) =>
  http.request<IRoleData[]>({
    url: `/users/${id}/roles`,
    method: 'get',
  });

export const updateUserRoles = (id: number) =>
  http.request<IRoleData[]>({
    url: `/users/${id}/roles`,
    method: 'get',
  });
