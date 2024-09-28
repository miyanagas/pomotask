import { createWebHistory, createRouter } from "vue-router";

import ToDoListView from "./components/ToDoList.vue";
import ToDoItemView from "./components/ToDoItem.vue";

const routes = [
  { path: "/", component: ToDoListView },
  { path: "/todo_list/:id/:title", name: "todo_item", component: ToDoItemView },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
