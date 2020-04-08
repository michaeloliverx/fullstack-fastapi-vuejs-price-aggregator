import request from '@/utils/request';

export const getUserMe = (data: any) =>
  request({
    url: '/me',
    method: 'get',
    data
  });

export const getUserRoles = (data: any) =>
  request({
    url: '/me/roles',
    method: 'get',
    data
  });

export const login = (data: any) =>
  request({
    url: '/auth/login',
    method: 'post',
    data
  });

export const logout = () =>
  request({
    url: '/auth/logout',
    method: 'post'
  });
