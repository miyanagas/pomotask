<script setup>
import { ref, onMounted, computed } from "vue";
import requestAPI from "./requestAPI";
import { useAuthStore } from "@/auth";
import { timeFormat } from "./Timer";

const authStore = useAuthStore();

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
      params: {
        filter: filtered.value,
      },
      withCredentials: true,
    });

    if (!response.data) return;
    todoList.value = response.data;
  } catch (e) {
    console.error(e);
    error.value = e.response.data.detail;
    alert("Todoリストの取得に失敗しました");
    if (e.response.status === 401) {
      authStore.checkLoginStatus();
    }
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
    if (e.response.status === 401) {
      authStore.checkLoginStatus();
    }
  } finally {
    newTodoTitle.value = "";
  }
};

const updateTodo = async (todo) => {
  try {
    await requestAPI.put(
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
    if (e.response.status === 401) {
      authStore.checkLoginStatus();
    }
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
    if (e.response.status === 401) {
      authStore.checkLoginStatus();
    }
  }

  todoList.value = [];
};
</script>

<template>
  <div class="container">
    <div v-if="error">
      <p>{{ error }}</p>
    </div>
    <form class="input-todo" @submit.prevent="addTodo">
      <input
        type="text"
        v-model="newTodoTitle"
        required
        placeholder="Todoを入力してください"
      />
      <button type="submit">追加</button>
    </form>
    <div class="filter-todo">
      <input class="filter-checkbox" type="checkbox" v-model="filtered" />
      <span>完了したTodoを非表示</span>
    </div>
    <div class="todo-list">
      <ul v-if="todoList.length !== 0">
        <li
          :class="{ 'done-item': todo.is_done }"
          class="todo-item"
          v-for="todo in filteredTodoList"
          :key="todo.id"
        >
          <router-link
            :to="{
              name: 'Todo',
              params: { id: todo.id },
            }"
            id="todo-item-link"
          >
            <span>{{ todo.title }}</span>
            <span v-show="todo.is_done" id="time-to-complete">
              {{ timeFormat(todo.time_to_complete) }}
            </span>
          </router-link>
          <input
            @change="updateTodo(todo)"
            class="status-checkbox"
            type="checkbox"
            v-model="todo.is_done"
          />
        </li>
      </ul>
      <p v-else>Todoがありません</p>
    </div>
    <div class="delete-todo">
      <button @click="deleteTodoList()">Todoを一括削除</button>
    </div>
  </div>
</template>

<style scoped>
.container {
  width: 640px;
  margin: 0 auto;
}

.input-todo {
  display: flex;
  justify-content: center;
}

.input-todo input {
  width: 400px;
  padding: 0.5rem;
  border: 1px solid var(--color-border);
  border-radius: 4px;
  margin: 2rem;
  font-size: 16px;
}

.input-todo button {
  padding: 0.5rem 1rem;
  margin: 2rem;
  border-radius: 4px;
  background-color: var(--color-primary);
  color: var(--color-text-white);
}

@media (hover: hover) {
  .input-todo button:hover {
    background-color: var(--color-primary-hover);
  }
}

.filter-todo {
  display: flex;
  justify-content: flex-end;
  align-items: center;
}

.filter-todo span {
  font-size: small;
  padding: 0.25rem 0.5rem;
}

.filter-checkbox {
  display: block;
  width: 18px;
  height: 18px;
  cursor: pointer;
  accent-color: var(--color-primary-hover);
}

.todo-list {
  padding: 1rem;
  border: none;
  border-radius: 4px;
  background-color: var(--color-gray);
}

.todo-list ul {
  list-style: none;
  padding: 0;
}

.todo-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  margin: 0.25rem 0;
  border-radius: 4px;
  background-color: var(--color-background);
}

@media (hover: hover) {
  .todo-item:hover {
    background-color: var(--color-background-hover);
  }
}

.done-item #todo-item-link {
  pointer-events: none;
}

.done-item,
.done-item:hover {
  background-color: var(--color-primary-dark);
}

#todo-item-link {
  display: block;
  width: 90%;
}

#time-to-complete {
  font-family: "Lucida Console", monospace;
  margin: 0 1em;
}

.status-checkbox {
  display: block;
  width: 25px;
  height: 25px;
  cursor: pointer;
  accent-color: royalblue;
}

.delete-todo {
  display: flex;
  justify-content: flex-end;
}

.delete-todo button {
  margin: 2rem 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  background-color: var(--color-red);
  color: var(--color-text-white);
}

@media (hover: hover) {
  .delete-todo button:hover {
    background-color: var(--color-red-hover);
  }
}
</style>
