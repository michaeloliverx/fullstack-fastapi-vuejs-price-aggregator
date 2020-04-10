import { RouteConfig } from "vue-router";
import Layout from "@/layout/index.vue";

const rolesRouter: RouteConfig = {
  path: "/roles",
  component: Layout,
  redirect: "list",
  name: "Roles",
  meta: {
    title: "Roles",
    icon: "password",
    roles: ["admin"]
  },
  children: [
    {
      path: "list",
      component: () =>
        import(/* webpackChunkName: "role-list" */ "@/views/roles/ListRoles.vue"),
      name: "ListRoles",
      meta: { title: "List Roles", icon: "list" }
    },
    {
      path: "create",
      component: () =>
        import(
          /* webpackChunkName: "role-create" */ "@/views/roles/CreateRole.vue"
        ),
      name: "CreateRole",
      meta: { title: "Create Role", icon: "form" }
    },
    {
      path: "edit/:id",
      component: () =>
        import(/* webpackChunkName: "role-edit" */ "@/views/roles/ListRoles.vue"),
      name: "EditRole",
      meta: { title: "Edit Role", icon: "form", hidden: true }
    }
  ]
};

export default rolesRouter;
