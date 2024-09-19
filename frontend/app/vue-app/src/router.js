import { createWebHistory, createRouter } from "vue-router";

import ToDoListView from "./ToDoList.vue";
import ToDoItemView from "./ToDoItem.vue";

const routes = [
  { path: "/", component: ToDoListView },
  { path: "/todo_list/:id", name: "todo_item", component: ToDoItemView },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
