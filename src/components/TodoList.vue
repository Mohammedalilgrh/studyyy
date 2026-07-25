<template>
  <div class="space-y-3">
    <div class="flex justify-between items-center mb-4 flex-wrap gap-2">
      <h2 class="text-xl font-semibold text-gray-800">📋 Your Tasks ({{ todos.length }})</h2>
      <div class="flex gap-2 flex-wrap">
        <button
          v-for="f in filters"
          :key="f"
          @click="activeFilter = f"
          :class="[
            'px-3 py-1 rounded-lg text-sm font-medium',
            activeFilter === f
              ? 'bg-indigo-600 text-white'
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          ]"
        >
          {{ f }}
        </button>
      </div>
    </div>

    <div v-if="filteredTodos.length === 0" class="text-center py-8 bg-white rounded-lg">
      <p class="text-gray-500">No tasks yet. Add one to get started! 🚀</p>
    </div>

    <TodoItem
      v-for="todo in filteredTodos"
      :key="todo.id"
      :todo="todo"
      @update="$emit('updateTodo', $event)"
      @delete="$emit('deleteTodo', $event)"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import TodoItem from './TodoItem.vue'

const props = defineProps<{
  todos: any[]
}>()

defineEmits<{
  updateTodo: [todo: any]
  deleteTodo: [id: string]
}>()

const filters = ['All', 'Active', 'Completed', 'High Priority']
const activeFilter = ref('All')

const filteredTodos = computed(() => {
  let result = props.todos || []

  switch (activeFilter.value) {
    case 'Active':
      result = result.filter(t => !t.completed)
      break
    case 'Completed':
      result = result.filter(t => t.completed)
      break
    case 'High Priority':
      result = result.filter(t => t.priority === 'high' || t.priority === 'urgent')
      break
  }

  return result.sort((a, b) => {
    const priorityOrder = { urgent: 0, high: 1, medium: 2, low: 3 }
    return priorityOrder[a.priority] - priorityOrder[b.priority]
  })
})
</script>