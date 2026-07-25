<template>
  <div class="bg-white rounded-lg shadow-md p-6 mb-6">
    <h2 class="text-xl font-semibold text-gray-800 mb-4">✨ Add New To-Do</h2>
    <form @submit.prevent="handleSubmit" class="space-y-4">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Task Title</label>
        <input
          v-model="title"
          type="text"
          placeholder="What needs to be done?"
          class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
          required
        />
      </div>

      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Category</label>
          <select
            v-model="category"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
          >
            <option value="">Auto-detect</option>
            <option value="Work">Work</option>
            <option value="Personal">Personal</option>
            <option value="Shopping">Shopping</option>
            <option value="Health">Health</option>
            <option value="Other">Other</option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Priority</label>
          <select
            v-model="priority"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
          >
            <option value="low">Low</option>
            <option value="medium" selected>Medium</option>
            <option value="high">High</option>
            <option value="urgent">Urgent</option>
          </select>
        </div>
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Due Date (Optional)</label>
        <input
          v-model="dueDate"
          type="date"
          class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
        />
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Description (Optional)</label>
        <textarea
          v-model="description"
          placeholder="Add details..."
          rows="3"
          class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
        />
      </div>

      <div class="flex gap-3">
        <button
          type="submit"
          class="flex-1 bg-indigo-600 text-white py-2 rounded-lg hover:bg-indigo-700 font-medium"
        >
          Add To-Do
        </button>
        <button
          type="button"
          @click="useAI"
          :disabled="!title || loading"
          class="flex-1 bg-purple-600 text-white py-2 rounded-lg hover:bg-purple-700 font-medium disabled:opacity-50"
        >
          {{ loading ? '✨ AI...' : '✨ AI Help' }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ClaudeService } from '@/services/claude'

const emit = defineEmits<{
  addTodo: [todo: any]
}>()

const title = ref('')
const description = ref('')
const category = ref('')
const priority = ref('medium')
const dueDate = ref('')
const loading = ref(false)

const claude = new ClaudeService()

const handleSubmit = () => {
  if (!title.value.trim()) return

  emit('addTodo', {
    title: title.value,
    description: description.value,
    category: category.value,
    priority: priority.value,
    dueDate: dueDate.value,
    completed: false,
    createdAt: new Date().toISOString()
  })

  title.value = ''
  description.value = ''
  category.value = ''
  priority.value = 'medium'
  dueDate.value = ''
}

const useAI = async () => {
  loading.value = true
  try {
    const expansion = await claude.expandDescription(title.value)
    description.value = expansion
  } catch (error) {
    console.error('AI error:', error)
  }
  loading.value = false
}
</script>