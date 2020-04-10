import { RouteConfig } from "vue-router";
import Layout from "@/layout/index.vue";

const usersRouter: RouteConfig = {
  path: "/users",
  component: Layout,
  redirect: "list",
  name: "Users",
  meta: {
    title: "Users",
    icon: "user",
    roles: ["admin"]
  },
  children: [
    {
      path: "list",
      component: () =>
        import(/* webpackChunkName: "user-list" */ "@/views/users/ListUsers.vue"),
      name: "ListUsers",
      meta: { title: "List Users", icon: "list" }
    },
    {
      path: "create",
      component: () =>
        import(
          /* webpackChunkName: "user-create" */ "@/views/users/CreateUser.vue"
        ),
      name: "CreateUser",
      meta: { title: "Create User", icon: "form" }
    },
    {
      path: "edit/:id",
      component: () =>
        import(/* webpackChunkName: "user-edit" */ "@/views/users/EditUser.vue"),
      name: "EditUser",
      meta: { title: "Edit User", icon: "form", hidden: true }
    }
  ]
};

export default usersRouter;
