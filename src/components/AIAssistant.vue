<template>
  <div class="bg-white rounded-lg shadow-md p-6">
    <h2 class="text-xl font-semibold text-gray-800 mb-4">🤖 FREE AI Assistant</h2>
    <p class="text-xs text-gray-500 mb-4">Powered by Puter (unlimited free)</p>

    <div class="space-y-3">
      <button
        @click="getSuggestions"
        :disabled="loading || todos.length === 0"
        class="w-full bg-purple-600 text-white py-2 rounded-lg hover:bg-purple-700 disabled:opacity-50 font-medium"
      >
        {{ loading ? '⏳ Analyzing...' : '💡 Get Suggestions' }}
      </button>

      <button
        @click="prioritizeTasks"
        :disabled="loading || todos.length === 0"
        class="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50 font-medium"
      >
        {{ loading ? '⏳ Prioritizing...' : '📊 Prioritize Tasks' }}
      </button>

      <button
        @click="categorizeTasks"
        :disabled="loading || todos.length === 0"
        class="w-full bg-indigo-600 text-white py-2 rounded-lg hover:bg-indigo-700 disabled:opacity-50 font-medium"
      >
        {{ loading ? '⏳ Categorizing...' : '🏷️ Auto-Categorize' }}
      </button>
    </div>

    <div v-if="suggestions.length > 0" class="mt-6 p-4 bg-purple-50 rounded-lg">
      <h3 class="font-semibold text-purple-900 mb-3">✨ AI Suggestions:</h3>
      <ul class="space-y-2">
        <li v-for="(s, i) in suggestions" :key="i" class="text-sm text-purple-800">
          • {{ s }}
        </li>
      </ul>
    </div>

    <div v-if="error" class="mt-4 p-3 bg-red-100 text-red-800 rounded-lg text-sm">
      ⚠️ {{ error }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ClaudeService } from '@/services/claude'

const props = defineProps<{
  todos: any[]
}>()

const emit = defineEmits<{
  applySuggestions: [suggestions: any]
}>()

const loading = ref(false)
const suggestions = ref<string[]>([])
const error = ref('')
const claude = new ClaudeService()

const getSuggestions = async () => {
  loading.value = true
  error.value = ''
  try {
    const sug = await claude.suggestTasks(props.todos)
    suggestions.value = sug
  } catch (err) {
    error.value = 'Failed to get suggestions. Make sure Free Claude is running.'
    console.error(err)
  }
  loading.value = false
}

const prioritizeTasks = async () => {
  loading.value = true
  error.value = ''
  try {
    const prioritized = await claude.prioritizeTasks(props.todos)
    suggestions.value = ['Tasks prioritized! Check your list for updated priorities']
    emit('applySuggestions', prioritized)
  } catch (err) {
    error.value = 'Failed to prioritize. Make sure Free Claude is running.'
    console.error(err)
  }
  loading.value = false
}

const categorizeTasks = async () => {
  loading.value = true
  error.value = ''
  try {
    const categorized = await claude.categorizeTasks(props.todos)
    suggestions.value = ['Tasks categorized automatically!']
    emit('applySuggestions', categorized)
  } catch (err) {
    error.value = 'Failed to categorize. Make sure Free Claude is running.'
    console.error(err)
  }
  loading.value = false
}
</script>