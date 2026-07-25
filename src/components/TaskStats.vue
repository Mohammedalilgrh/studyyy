<template>
  <div class="bg-white rounded-lg shadow-md p-6">
    <h2 class="text-xl font-semibold text-gray-800 mb-4">📊 Statistics</h2>

    <div class="space-y-3">
      <StatCard label="Total Tasks" :value="stats.total" icon="📋" />
      <StatCard label="Completed" :value="stats.completed" icon="✅" color="green" />
      <StatCard label="Active" :value="stats.active" icon="⚡" color="blue" />
      <StatCard label="High Priority" :value="stats.highPriority" icon="🔥" color="red" />
      <StatCard label="Completion Rate" :value="stats.completionRate + '%'" icon="📈" color="purple" />
    </div>

    <div class="mt-6 p-4 bg-blue-50 rounded-lg">
      <p class="text-sm text-blue-900">
        <strong>💡 Tip:</strong> Use AI Assistant to get FREE suggestions!
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import StatCard from './StatCard.vue'

const props = defineProps<{
  todos: any[]
}>()

const stats = computed(() => {
  const todos = props.todos || []
  const completed = todos.filter(t => t.completed).length
  const total = todos.length
  const active = total - completed
  const highPriority = todos.filter(t => t.priority === 'high' || t.priority === 'urgent').length
  const completionRate = total === 0 ? 0 : Math.round((completed / total) * 100)

  return { total, completed, active, highPriority, completionRate }
})
</script>