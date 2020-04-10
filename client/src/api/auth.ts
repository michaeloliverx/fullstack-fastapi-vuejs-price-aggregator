import http from '@/utils/request';
import {IUserData, ITokenData} from "@/api/types";

export const login = (data: any) =>
  http.request<ITokenData>({
    url: '/auth/login',
    method: 'post',
    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
    data,
  });

export const logout = (data?: any) =>
  http.request({
    url: '/auth/logout',
    method: 'post',
    data
  });

export const register = (data?: any) =>
  http.request({
    url: '/auth/register',
    method: 'post',
    data
  });
