<template>
  <div
    :class="[
      'bg-white rounded-lg shadow-sm p-4 border-l-4 transition-all hover:shadow-md',
      todo.completed ? 'border-l-gray-300 opacity-60' : priorityBorder
    ]"
  >
    <div class="flex items-start gap-3">
      <input
        type="checkbox"
        :checked="todo.completed"
        @change="$emit('update', { ...todo, completed: !todo.completed })"
        class="mt-1 h-5 w-5 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
      />
      <div class="flex-1 min-w-0">
        <h3
          :class="[
            'font-semibold text-gray-900',
            todo.completed && 'line-through text-gray-500'
          ]"
        >
          {{ todo.title }}
        </h3>
        <p v-if="todo.description" class="text-sm text-gray-600 mt-1 line-clamp-2">
          {{ todo.description }}
        </p>
        <div class="flex flex-wrap gap-2 mt-2">
          <span v-if="todo.category" class="inline-block bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded">
            {{ todo.category }}
          </span>
          <span :class="['inline-block text-xs px-2 py-1 rounded', priorityBgClass]">
            {{ todo.priority.toUpperCase() }}
          </span>
          <span v-if="todo.dueDate" class="inline-block bg-orange-100 text-orange-800 text-xs px-2 py-1 rounded">
            📅 {{ formatDate(todo.dueDate) }}
          </span>
        </div>
      </div>
      <button
        @click="$emit('delete', todo.id)"
        class="text-red-600 hover:text-red-800 font-semibold"
      >
        🗑️
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  todo: any
}>()

defineEmits<{
  update: [todo: any]
  delete: [id: string]
}>()

const priorityBorder = computed(() => {
  const borders = {
    urgent: 'border-l-red-500',
    high: 'border-l-orange-500',
    medium: 'border-l-yellow-500',
    low: 'border-l-green-500'
  }
  return borders[props.todo.priority] || 'border-l-gray-500'
})

const priorityBgClass = computed(() => {
  const colors = {
    urgent: 'bg-red-100 text-red-800',
    high: 'bg-orange-100 text-orange-800',
    medium: 'bg-yellow-100 text-yellow-800',
    low: 'bg-green-100 text-green-800'
  }
  return colors[props.todo.priority] || 'bg-gray-100 text-gray-800'
})

const formatDate = (date: string) => {
  return new Date(date).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric'
  })
}
</script>