import router from "./router";
import NProgress from "nprogress";
import "nprogress/nprogress.css";
import { Message } from "element-ui";
import { Route } from "vue-router";
import { UserMeModule } from "@/store/modules/me";
import { PermissionModule } from "@/store/modules/permission";
import settings from "./settings";

NProgress.configure({ showSpinner: false });

const whiteList = [
  "/login",
  "/register",
  "/forgot-password",
  "/reset-password"
];

router.beforeEach(async (to: Route, _: Route, next: any) => {
  // Start progress bar
  NProgress.start();

  // Determine whether the user has logged in
  if (UserMeModule.token) {
    if (to.path === "/login") {
      // If is logged in, redirect to the home page
      next({ path: "/" });
      NProgress.done();
    } else {
      // Check whether the user has obtained their permission roles
      if (UserMeModule.roles.length === 0) {
        try {
          // Note: roles must be a object array! such as: ['admin'] or ['developer', 'editor']
          await UserMeModule.GetUserMe();
          await UserMeModule.GetUserMeRoles();

          const roleNames = UserMeModule.role_names;
          // Generate accessible routes map based on role
          PermissionModule.GenerateRoutes(roleNames);
          // Dynamically add accessible routes
          router.addRoutes(PermissionModule.dynamicRoutes);
          // Hack: ensure addRoutes is complete
          // Set the replace: true, so the navigation will not leave a history record
          next({ ...to, replace: true });
        } catch (err) {
          // Remove token and redirect to login page
          UserMeModule.ResetToken();
          Message.error(err || "Has Error");
          next(`/login?redirect=${to.path}`);
          NProgress.done();
        }
      } else {
        next();
      }
    }
  } else {
    // Has no token
    if (whiteList.indexOf(to.path) !== -1) {
      // In the free login whitelist, go directly
      next();
    } else {
      // Other pages that do not have permission to access are redirected to the login page.
      next(`/login?redirect=${to.path}`);
      NProgress.done();
    }
  }
});

router.afterEach((to: Route) => {
  // Finish progress bar
  NProgress.done();

  // set page title
  document.title = `${to.meta.title} - ${settings.title}`;
});
