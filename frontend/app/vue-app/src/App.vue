<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios';

const request = axios.create({
  baseURL: 'http://localhost:8080/api/v1'
});

const error = ref(null);
const toDoList = ref([]);
const newToDo = ref('');

onMounted(() => {
    fetchToDoList()
})

const fetchToDoList = async () => {
    try {
        const response = await request.get('/todolist')

        if (!response.data) return
        toDoList.value = response.data
    } catch (e) {
        error.value = e
        alert('エラーが発生しました')
    }
}

const addToDo = async () => {
    if (!newToDo.value) {
        alert('Todoを入力してください')
        return
    }

    try {
        await request.post('/todolist',
        {
            title: newToDo.value
        })

    } catch (e) {
        error.value = e
        alert('エラーが発生しました')
    }
    finally {
        newToDo.value = ''
    }

    fetchToDoList()
}

const deleteToDoList = async () => {
    try {
        await request.delete('/todolist')
    } catch (e) {
        error.value = e
        alert('エラーが発生しました')
    }

    toDoList.value = []
}
</script>

<template>
  <header>
    <h1 class="title">今日のToDo</h1>
    <img alt="App logo" class="logo" src="./assets/todo-logo.svg" width="35" height="35" />
  </header>
  <div class="container">
    <div v-if="error">
      <p>{{ error }}</p>
    </div>
    <div class="input-todo">
      <input type="text" v-model="newToDo" placeholder="ToDoを入力してください">
      <button @click="addToDo()">追加</button>
    </div>
    <div class="todo-list">
          <ul  v-if="toDoList.length!==0">
              <li class="todo-item" v-for="(toDo, index) in toDoList" :key="index">
                  <span>{{ toDo.title }}</span>
                  <span><input class="status-checkbox" type="checkbox" v-model="toDo.is_done"></span>
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
/* header {
  line-height: 1.5;
}*/

.logo {
  display: block;
  /* margin: 0 auto 2rem; */
}

header {
  background-color: hsla(160, 100%, 37%, 1);
  color: white;
  padding: 1rem;
  display: flex;
  justify-content: flex-start;
  align-items: center;
  flex-direction: row;
}

.title {
  margin: 0;
  padding: 0.5rem 1rem 0.5rem 2rem;
}

.container {
  margin: 5%;
  padding: 0 5%;
}

.input-todo {
  display: flex;
  justify-content: center;
}

.input-todo input {
  width: 35%;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  margin: 2rem;
}

.input-todo button {
  padding: 0.5rem 1rem;
  margin: 2rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  background-color: hsla(160, 100%, 37%, 1);
  color: white;
  cursor: pointer;
}

.todo-list {
  width: 55%;
  margin: 0 auto;
  padding: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
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
  margin: 0.5rem 0;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.status-checkbox {
  display: block;
  width: 25px;
  height: 25px;
  cursor: pointer;
  accent-color: hsla(160, 100%, 37%, 1);
}

.delete-todo {
  display: flex;
  justify-content: flex-end;
  width: 55%;
  margin: 0 auto;
}

.delete-todo button {
  margin: 2rem 0.5rem;
  padding: 0.5rem 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  background-color: hsla(160, 100%, 37%, 1);
  color: white;
  cursor: pointer;
}

/*
@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }
} */
</style>
