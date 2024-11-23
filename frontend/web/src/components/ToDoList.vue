<script setup>
import { ref, onMounted, computed } from "vue";
import requestAPI from "./requestAPI";
import { timeFormat } from "./time";
import { useLoadingStore } from "./loading";

import LoadingView from "./Loading.vue";

const loadingStore = useLoadingStore();

const todoList = ref([]);
const newTodoTitle = ref("");
const filtered = ref(false);

const error = ref(null);

// Todoリストのフィルタリング
const filteredTodoList = computed(() => {
  if (filtered.value) {
    return todoList.value.filter((todo) => {
      return !todo.is_done;
    });
  } else {
    return todoList.value;
  }
});

// Todoリストの取得
onMounted(async () => {
  try {
    const response = await requestAPI.get("/todo-list/", {
      withCredentials: true,
    });

    if (!response.data) return;
    todoList.value = response.data;
  } catch (e) {
    console.error(e);
    error.value = e.response.data.detail;
    alert("Todoリストの取得に失敗しました");
  }
});

const addTodo = async () => {
  if (!newTodoTitle.value) return;

  try {
    const response = await requestAPI.post(
      "/todo-list/",
      {
        title: newTodoTitle.value,
      },
      {
        withCredentials: true,
      }
    );
    const newTodo = response.data;
    todoList.value.push(newTodo);
  } catch (e) {
    console.error(e);
    error.value = e.response.data.detail;
    alert("Todoの追加に失敗しました");
  } finally {
    newTodoTitle.value = "";
  }
};

const updateTodo = async (todo) => {
  try {
    await requestAPI.patch(
      `/todo-list/${todo.id}`,
      {
        is_done: todo.is_done,
      },
      {
        withCredentials: true,
      }
    );
  } catch (e) {
    console.error(e);
    error.value = e.response.data.detail;
    alert("Todoの更新に失敗しました");
  }
};

const deleteTodoList = async () => {
  try {
    await requestAPI.delete("/todo-list/", {
      withCredentials: true,
    });
  } catch (e) {
    console.error(e);
    error.value = e.response.data.detail;
    alert("Todoリストの削除に失敗しました");
  }

  todoList.value = [];
};
</script>

<template>
  <div class="container" v-if="!loadingStore.isLoading">
    <div v-if="error" class="error-message">
      <p>{{ error }}</p>
    </div>
    <form class="single-input-form" @submit.prevent="addTodo">
      <input
        class="text-input"
        type="text"
        v-model="newTodoTitle"
        required
        placeholder="Todoを入力してください"
      />
      <button style="margin-left: 2rem" class="primary-button" type="submit">
        追加
      </button>
    </form>
    <div style="font-size: 12px" class="flex-end-container">
      <input id="filter-checkbox" type="checkbox" v-model="filtered" />
      <span>完了したTodoを非表示</span>
    </div>
    <div id="todo-list">
      <ul v-if="filteredTodoList.length !== 0">
        <li
          class="todo"
          :class="{ 'completed-todo': todo.is_done }"
          v-for="todo in filteredTodoList"
          :key="todo.id"
        >
          <router-link
            :to="{
              name: 'Todo',
              params: { id: todo.id },
            }"
          >
            <span class="todo-title">{{ todo.title }}</span>
            <span v-if="todo.is_done" class="todo-complete-time">
              {{ timeFormat(todo.time_to_complete) }}
            </span>
          </router-link>
          <input
            class="todo-checkbox"
            type="checkbox"
            v-model="todo.is_done"
            @change="updateTodo(todo)"
          />
        </li>
      </ul>
      <p v-else>Todoがありません</p>
    </div>
    <div style="display: flex; justify-content: flex-end">
      <button
        style="margin: 2rem 0.5rem"
        class="danger-button"
        @click="deleteTodoList()"
      >
        Todoを全て削除
      </button>
    </div>
  </div>
  <LoadingView v-else />
</template>

<style scoped>
#filter-checkbox {
  margin-right: 0.5rem;
  display: block;
  width: 16px;
  height: 16px;
  cursor: pointer;
  accent-color: var(--color-primary);
}

#todo-list {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  background-color: var(--color-gray);
}

#todo-list ul {
  list-style: none;
  padding: 0;
}

.todo {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  margin: 0.5rem 0;
  border-radius: 4px;
  background-color: var(--color-background);
  font-size: 18px;
}

@media (hover: hover) {
  .todo:hover {
    background-color: var(--color-background-hover);
  }
}

.todo a {
  display: block;
  width: 90%;
}

.completed-todo {
  background-color: var(--color-checkbox);
}

.completed-todo a {
  pointer-events: none;
  color: var(--color-text-white);
}

.completed-todo .todo-title {
  text-decoration: line-through;
}

@media (hover: hover) {
  .completed-todo:hover {
    background-color: var(--color-checkbox);
  }
}

.todo-complete-time {
  font-family: "Lucida Console", monospace;
  margin-left: 2rem;
}

.todo-checkbox {
  display: block;
  width: 25px;
  height: 25px;
  cursor: pointer;
  accent-color: var(--color-checkbox);
}
</style>
