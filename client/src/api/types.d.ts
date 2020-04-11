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
  name: string
  description: string
}

export interface IRoleUpdate {
  name?: string
  description?: string
}

export interface IShopData {
  id: number
  created_at: Date
  updated_at: Date
  name: string
  url: string
  query_url: string
  render_javascript: boolean
  listing_page_selector: Object
}

export interface IShopCreate {
  name: string
  url: string
  query_url: string
  render_javascript: boolean
  listing_page_selector: Object
}

export interface IShopUpdate {
  name?: string
  url?: string
  query_url?: string
  render_javascript?: boolean
  listing_page_selector?: Object
}

export interface ScrapedItem {
  name: string
  url: string
  price: string
  price_per_unit: string
  image_url: string
}

export interface IShopListings {
  id: number
  name: string
  listings: ScrapedItem[]
}
