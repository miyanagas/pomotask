import { createWebHistory, createRouter } from "vue-router";
import { useAuthStore } from "./auth";

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
    meta: { requiresAuth: false },
  },
  {
    path: "/signup",
    component: SignUpView,
    meta: { requiresAuth: false },
  },
  { path: "/mypage", component: MyPageView, meta: { requiresAuth: true } },
  {
    path: "/edit_password",
    component: EditPasswordView,
    meta: { requiresAuth: true },
  },
  {
    path: "/",
    name: "TodoList",
    component: ToDoListView,
    meta: { requiresAuth: true },
  },
  {
    path: "/:id/",
    name: "Todo",
    component: ToDoItemView,
    meta: { requiresAuth: true },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore();
  if (!authStore.initialized) {
    await authStore.initialize();
  }

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: "Login" });
  } else if (!to.meta.requiresAuth && authStore.isAuthenticated) {
    next({ name: "TodoList" });
  } else {
    next();
  }
});

export default router;
