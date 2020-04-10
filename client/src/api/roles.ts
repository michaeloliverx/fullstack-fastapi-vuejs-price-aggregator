import http from '@/utils/request'
import { IRoleData, IRoleUpdate, IRoleCreate } from './types';

export const getRoles = (params: any) =>
  http.request<IRoleData[]>({
    url: '/roles',
    method: 'get',
    params
  });

export const createRole = (data: IRoleCreate) =>
  http.request<IRoleData>({
    url: '/roles',
    method: 'post',
    data
  });

export const updateRole = (id: number, data: IRoleUpdate) =>
  http.request<IRoleData>({
    url: `/roles/${id}`,
    method: 'put',
    data
  });

export const deleteRole = (id: number) =>
  http.request({
    url: `/roles/${id}`,
    method: 'delete',
  });
