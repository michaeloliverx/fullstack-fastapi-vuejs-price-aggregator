/* eslint camelcase: 0 */

import { UserStatus } from './enums';

export interface IArticleData {
  id: number
  status: string
  title: string
  abstractContent: string
  fullContent: string
  sourceURL: string
  imageURL: string
  timestamp: string | number
  platforms: string[]
  disableComment: boolean
  importance: number
  author: string
  reviewer: string
  type: string
  pageviews: number
}

export interface IUser {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  status: UserStatus;
  created_at: Date;
  updated_at: Date;
}

export interface IRole {
  id: number,
  name: string,
  description: string,
  created_at: Date;
  updated_at: Date;
}
