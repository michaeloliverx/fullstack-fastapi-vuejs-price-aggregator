import request from '@/utils/request';

export const getUserInfo = (data: any) =>
  request({
    url: '/users/me',
    method: 'post',
    data
  });

export const getUserRoles = (data: any) =>
  request({
    url: '/users/me/roles',
    method: 'post',
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
    url: '/users/logout',
    method: 'post'
  });
