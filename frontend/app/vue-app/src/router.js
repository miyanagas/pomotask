import { createWebHistory, createRouter } from "vue-router";
import isAuthenticated from "./auth";

import LogInView from "./components/LogIn.vue";
import SignUpView from "./components/SignUp.vue";
import MyPageView from "./components/MyPage.vue";
import ToDoListView from "./components/ToDoList.vue";
import ToDoItemView from "./components/ToDoItem.vue";
import EditPasswordView from "./components/EditPassword.vue";

const routes = [
  {
    path: "/login",
    name: "Login",
    component: LogInView,
    meta: { hideHeader: true },
  },
  {
    path: "/signup",
    component: SignUpView,
    meta: { hideHeader: true },
  },
  { path: "/my_page", component: MyPageView, meta: { requiresAuth: true } },
  {
    path: "/edit_password",
    component: EditPasswordView,
    meta: { requiresAuth: true },
  },
  {
    path: "/",
    name: "ToDoList",
    component: ToDoListView,
    meta: { requiresAuth: true },
  },
  {
    path: "/todo_list/:id/:title",
    name: "todo_item",
    component: ToDoItemView,
    meta: { requiresAuth: true },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !isAuthenticated()) {
    console.log(isAuthenticated());
    next({ name: "Login" });
  } else {
    next();
  }
});

export default router;
