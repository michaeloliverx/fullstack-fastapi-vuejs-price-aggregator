import { UserStatus } from './enums';

export interface ITokenData {
  access_token: string
  token_type: string
}

export interface IUserData {
  id: number
  email: string
  first_name: string
  last_name: string
  status: UserStatus
  created_at: Date
  updated_at: Date
}

export interface IUserCreate {
  email: string
  first_name: string
  last_name: string
  password: string
  status?: UserStatus
}

export interface IUserUpdate {
  email?: string
  first_name?: string
  last_name?: string
  password?: string
  status?: UserStatus
}


export interface IRoleData {
  id: number
  name: string
  description: string
  created_at: Date
  updated_at: Date
}

export interface IRoleCreate {
  name?: string
  description: string
}

export interface IRoleUpdate {
  name?: string
  description?: string
}
