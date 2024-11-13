import { createWebHistory, createRouter } from "vue-router";

import LogInView from "./components/LogIn.vue";
import SignUpView from "./components/SignUp.vue";
import MyPageView from "./components/MyPage.vue";
import ToDoListView from "./components/ToDoList.vue";
import ToDoItemView from "./components/ToDoItem.vue";

const routes = [
  { path: "/login", component: LogInView, meta: { hideHeader: true } },
  { path: "/signup", component: SignUpView, meta: { hideHeader: true } },
  { path: "/my_page", component: MyPageView },
  { path: "/", component: ToDoListView },
  { path: "/todo_list/:id/:title", name: "todo_item", component: ToDoItemView },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
