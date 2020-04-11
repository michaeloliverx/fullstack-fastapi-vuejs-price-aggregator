import { RouteConfig } from "vue-router";
import Layout from "@/layout/index.vue";

const shopsRouter: RouteConfig = {
  path: "/shops",
  component: Layout,
  redirect: "list",
  name: "shops",
  meta: {
    title: "Shops",
    icon: "shopping",
    roles: ["admin"]
  },
  children: [
    {
      path: "list",
      component: () =>
        import(/* webpackChunkName: "shop-list" */ "@/views/shops/ListShops.vue"),
      name: "Listshops",
      meta: { title: "List shops", icon: "list" }
    },
    {
      path: "create",
      component: () =>
        import(
          /* webpackChunkName: "shop-create" */ "@/views/shops/CreateShop.vue"
        ),
      name: "Createshop",
      meta: { title: "Create shop", icon: "form" }
    },
    {
      path: "edit/:id",
      component: () =>
        import(/* webpackChunkName: "shop-edit" */ "@/views/shops/EditShop.vue"),
      name: "Editshop",
      meta: { title: "Edit shop", icon: "form", hidden: true }
    }
  ]
};

export default shopsRouter;
