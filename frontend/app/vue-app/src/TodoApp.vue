<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const request = axios.create({
    baseURL: 'http://localhost:8080/api/v1'
})

const todos = ref(null)

const newTodo = ref('')

const error = ref(null)

onMounted(() => {
    fetchTodos()
})

const fetchTodos = async () => {
    try {
        const response = await request.get('/todolist')

        if (!response.data) return
        todos.value = response.data
    } catch (e) {
        console.error(e)
        error.value = e
    }
}

const addTodo = async () => {
    if (!newTodo.value) {
        alert('Todoを入力してください')
        return
    }

    try {
        await request.post('/todolist',
        {
            title: newTodo.value
        })

    } catch (e) {
        console.error(e)
        error.value = e
    }
    finally {
        newTodo.value = ''
    }

    fetchTodos()
}


</script>

<template>
    <div class="container">
        <h1>Todo App</h1>
        <input type="text" v-model="newTodo">
        <button @click="addTodo()">Add</button>
        <div v-if="error">
            <p>{{ error }}</p>
        </div>
        <ul>
            <li v-for="(todo, index) in todos" :key="index">
                <input type="checkbox" v-model="todo.is_done">
                <span>{{ todo.title }}</span>
            </li>
        </ul>
    </div>
</template>

<style>
</style>
