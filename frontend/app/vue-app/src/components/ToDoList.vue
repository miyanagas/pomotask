<script setup>
import { ref, onMounted } from "vue";
import requestAPI from "./requestAPI";
import { useAuthStore } from "@/auth";

const authStore = useAuthStore();

const toDoList = ref([]);
const newToDo = ref("");
const isToDoFilter = ref(true);

const error = ref(null);

onMounted(() => {
  fetchToDoList();
});

const fetchToDoList = async () => {
  try {
    const response = await requestAPI.get("/todo-list/", {
      params: {
        filter: isToDoFilter.value,
      },
      withCredentials: true,
    });

    if (!response.data) return;
    toDoList.value = response.data;
  } catch (e) {
    console.error(e);
    error.value = e.response.data.detail;
    alert("Todoリストの取得に失敗しました");
    if (e.response.status === 401) {
      authStore.checkLoginStatus();
    }
  }
};

const addToDo = async () => {
  if (!newToDo.value) {
    alert("Todoを入力してください");
    return;
  }

  try {
    await requestAPI.post(
      "/todo-list/",
      {
        title: newToDo.value,
      },
      {
        withCredentials: true,
      }
    );
  } catch (e) {
    console.error(e);
    error.value = e.response.data.detail;
    alert("Todoの追加に失敗しました");
    if (e.response.status === 401) {
      authStore.checkLoginStatus();
    }
  } finally {
    newToDo.value = "";
  }

  fetchToDoList();
};

const updateToDo = async (toDo) => {
  try {
    await requestAPI.put(
      `/todo-list/${toDo.id}`,
      {
        is_done: toDo.is_done,
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

  fetchToDoList();
};

const deleteToDoList = async () => {
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

  toDoList.value = [];
};

const timeFormatter = (time) => {
  const hours = Math.floor(time / 60 / 60);
  const minutes = String(Math.floor(time / 60) % 60).padStart(2, "0");
  const seconds = String(time % 60).padStart(2, "0");
  if (hours === 0) {
    return `${minutes}:${seconds}`;
  }
  return `${hours}:${minutes}:${seconds}`;
};
</script>

<template>
  <div class="container">
    <div v-if="error">
      <p>{{ error }}</p>
    </div>
    <div class="input-todo">
      <input
        type="text"
        v-model="newToDo"
        placeholder="ToDoを入力してください"
      />
      <button @click="addToDo()">追加</button>
    </div>
    <div class="filter-todo">
      <input
        @change="fetchToDoList()"
        class="filter-checkbox"
        type="checkbox"
        v-model="isToDoFilter"
      />
      <span>完了したToDoを非表示</span>
    </div>
    <div class="todo-list">
      <ul v-if="toDoList.length !== 0">
        <li
          :class="{ 'done-item': toDo.is_done }"
          class="todo-item"
          v-for="(toDo, index) in toDoList"
          :key="index"
        >
          <router-link
            :to="{
              name: 'todo_item',
              params: { id: toDo.id, title: toDo.title },
            }"
            id="todo-item-link"
          >
            <span>{{ toDo.title }}</span>
            <span v-show="toDo.is_done" id="time-to-complete">
              {{ timeFormatter(toDo.time_to_complete) }}
            </span>
          </router-link>
          <input
            @change="updateToDo(toDo)"
            class="status-checkbox"
            type="checkbox"
            v-model="toDo.is_done"
          />
        </li>
      </ul>
      <p v-else>ToDoがありません</p>
    </div>
    <div class="delete-todo">
      <button @click="deleteToDoList()">ToDoを一括削除</button>
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
