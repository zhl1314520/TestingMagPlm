<template>
  <div class="reports-page">
    <div class="page-content">
      <div class="page-header">
        <div class="header-content">
          <div class="title-section">
            <div class="title-badge">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <line x1="18" y1="20" x2="18" y2="10"/>
                <line x1="12" y1="20" x2="12" y2="4"/>
                <line x1="6" y1="20" x2="6" y2="14"/>
              </svg>
              Reports
            </div>
            <h1 class="page-title">报告统计</h1>
            <p class="page-subtitle">数据驱动质量改进</p>
          </div>
          <button @click="refreshData" class="btn-refresh" :class="{ spinning: loading }">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="23 4 23 10 17 10"/>
              <polyline points="1 20 1 14 7 14"/>
              <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/>
            </svg>
            刷新数据
          </button>
        </div>
        <div class="header-decoration">
          <div class="deco-blob deco-blob-1"></div>
          <div class="deco-blob deco-blob-2"></div>
        </div>
      </div>

      <div class="main-content">
        <div class="left-panel">
          <div class="trend-section">
            <div class="section-header">
              <div class="section-title">
                <svg class="title-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/>
                  <polyline points="17 6 23 6 23 12"/>
                </svg>
                <h2>趋势分析</h2>
              </div>
              <div class="section-actions">
                <button class="btn-period" :class="{ active: period === 7 }" @click="changePeriod(7)">7 天</button>
                <button class="btn-period" :class="{ active: period === 30 }" @click="changePeriod(30)">30 天</button>
                <button class="btn-period" :class="{ active: period === 90 }" @click="changePeriod(90)">90 天</button>
              </div>
            </div>

            <div class="chart-container">
              <canvas ref="chartCanvas"></canvas>
            </div>

            <div v-if="trendData.length === 0" class="empty-chart">
              <div class="empty-visual">
                <div class="empty-icon-wrapper">
                  <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="18" y1="20" x2="18" y2="10"/>
                    <line x1="12" y1="20" x2="12" y2="4"/>
                    <line x1="6" y1="20" x2="6" y2="14"/>
                  </svg>
                </div>
                <div class="empty-glow"></div>
              </div>
              <p>暂无趋势数据</p>
            </div>
          </div>
        </div>

        <div class="right-panel">
          <div class="reports-section">
            <div class="section-header">
              <div class="section-title">
                <svg class="title-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                  <polyline points="14 2 14 8 20 8"/>
                  <line x1="16" y1="13" x2="8" y2="13"/>
                  <line x1="16" y1="17" x2="8" y2="17"/>
                </svg>
                <h2>报告列表</h2>
              </div>
              <div class="section-count">
                共 {{ pagination.total }} 份报告
              </div>
            </div>

            <div v-if="loading" class="loading-state">
              <div class="loading-spinner"></div>
              <p>加载中...</p>
            </div>

            <div v-else-if="reports.length === 0" class="empty-reports">
              <div class="empty-visual">
                <div class="empty-icon-wrapper">
                  <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                    <polyline points="14 2 14 8 20 8"/>
                  </svg>
                </div>
                <div class="empty-glow"></div>
              </div>
              <h3>暂无报告</h3>
              <p>测试执行后将自动生成报告</p>
            </div>

            <div v-else class="reports-list">
              <div v-for="report in reports" :key="report.id" class="report-card">
                <div class="card-glow"></div>
                <div class="report-header">
                  <div class="report-title">
                    <svg class="report-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <line x1="18" y1="20" x2="18" y2="10"/>
                      <line x1="12" y1="20" x2="12" y2="4"/>
                      <line x1="6" y1="20" x2="6" y2="14"/>
                    </svg>
                    <h3>{{ report.title }}</h3>
                  </div>
                  <div class="report-date">{{ formatDate(report.created_at) }}</div>
                </div>

                <div class="report-meta">
                  <div class="meta-item">
                    <svg class="meta-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>
                    </svg>
                    <span>项目ID: {{ report.project_id }}</span>
                  </div>
                  <div class="meta-item">
                    <svg class="meta-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                      <polyline points="14 2 14 8 20 8"/>
                      <line x1="16" y1="13" x2="8" y2="13"/>
                      <line x1="16" y1="17" x2="8" y2="17"/>
                    </svg>
                    <span>总用例: {{ report.total_cases }}</span>
                  </div>
                </div>

                <div class="report-stats">
                  <div class="stat-item pass">
                    <div class="stat-icon">
                      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <polyline points="20 6 9 17 4 12"/>
                      </svg>
                    </div>
                    <div class="stat-content">
                      <div class="stat-value">{{ report.passed_cases }}</div>
                      <div class="stat-label">通过 ({{ (report.pass_rate * 100).toFixed(1) }}%)</div>
                    </div>
                    <div class="stat-bar">
                      <div class="stat-progress" :style="{ width: report.pass_rate * 100 + '%' }"></div>
                    </div>
                  </div>

                  <div class="stat-item fail">
                    <div class="stat-icon">
                      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <line x1="18" y1="6" x2="6" y2="18"/>
                        <line x1="6" y1="6" x2="18" y2="18"/>
                      </svg>
                    </div>
                    <div class="stat-content">
                      <div class="stat-value">{{ report.failed_cases }}</div>
                      <div class="stat-label">失败 ({{ (report.fail_rate * 100).toFixed(1) }}%)</div>
                    </div>
                    <div class="stat-bar">
                      <div class="stat-progress" :style="{ width: report.fail_rate * 100 + '%' }"></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div v-if="reports.length > 0" class="pagination">
              <button 
                class="btn-page" 
                :disabled="pagination.page === 1" 
                @click="changePage(pagination.page - 1)"
              >
                上一页
              </button>
              <span class="page-info">第 {{ pagination.page }} / {{ totalPages }} 页</span>
              <button 
                class="btn-page" 
                :disabled="pagination.page >= totalPages" 
                @click="changePage(pagination.page + 1)"
              >
                下一页
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { reportAPI, metricsAPI } from '../api/index.js'
import { Chart, registerables } from 'chart.js'

Chart.register(...registerables)

const loading = ref(false)
const period = ref(7)
const chartCanvas = ref(null)
let chartInstance = null

const trendData = ref([])

const reports = ref([])
const pagination = ref({
  page: 1,
  pageSize: 10,
  total: 0
})

const totalPages = computed(() => {
  return Math.ceil(pagination.value.total / pagination.value.pageSize) || 1
})

onMounted(async () => {
  await Promise.all([loadTrendData(), loadReports()])
})

onUnmounted(() => {
  if (chartInstance) {
    chartInstance.destroy()
  }
})

const loadTrendData = async () => {
  try {
    const response = await metricsAPI.getTrend()
    trendData.value = response.data
    await nextTick()
    renderChart()
  } catch (error) {
    console.error('获取趋势数据失败:', error)
  }
}

const renderChart = () => {
  if (!chartCanvas.value || trendData.value.length === 0) return

  if (chartInstance) {
    chartInstance.destroy()
  }

  const ctx = chartCanvas.value.getContext('2d')
  const labels = trendData.value.map(item => item.date)
  const passRates = trendData.value.map(item => (item.pass_rate * 100).toFixed(1))
  const failRates = trendData.value.map(item => (item.fail_rate * 100).toFixed(1))

  chartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [
        {
          label: '通过率 (%)',
          data: passRates,
          borderColor: '#10b981',
          backgroundColor: 'rgba(16, 185, 129, 0.1)',
          borderWidth: 3,
          fill: true,
          tension: 0.4,
          pointBackgroundColor: '#10b981',
          pointBorderColor: '#fff',
          pointBorderWidth: 2,
          pointRadius: 5,
          pointHoverRadius: 7
        },
        {
          label: '失败率 (%)',
          data: failRates,
          borderColor: '#ef4444',
          backgroundColor: 'rgba(239, 68, 68, 0.1)',
          borderWidth: 3,
          fill: true,
          tension: 0.4,
          pointBackgroundColor: '#ef4444',
          pointBorderColor: '#fff',
          pointBorderWidth: 2,
          pointRadius: 5,
          pointHoverRadius: 7
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'top',
          labels: {
            usePointStyle: true,
            padding: 20,
            font: {
              size: 13,
              weight: '600'
            }
          }
        },
        tooltip: {
          backgroundColor: 'rgba(255, 255, 255, 0.95)',
          titleColor: '#1f2937',
          bodyColor: '#6b7280',
          borderColor: '#e5e7eb',
          borderWidth: 1,
          padding: 12,
          cornerRadius: 8,
          displayColors: true,
          callbacks: {
            label: function(context) {
              return `${context.dataset.label}: ${context.parsed.y}%`
            }
          }
        }
      },
      scales: {
        x: {
          grid: {
            display: false
          },
          ticks: {
            color: '#6b7280',
            font: {
              size: 12
            }
          }
        },
        y: {
          beginAtZero: true,
          max: 100,
          grid: {
            color: 'rgba(0, 0, 0, 0.05)'
          },
          ticks: {
            color: '#6b7280',
            font: {
              size: 12
            },
            callback: function(value) {
              return value + '%'
            }
          }
        }
      },
      interaction: {
        intersect: false,
        mode: 'index'
      }
    }
  })
}

const loadReports = async () => {
  loading.value = true
  try {
    const response = await reportAPI.getList(pagination.value.page, pagination.value.pageSize)
    reports.value = response.data.items
    pagination.value.total = response.data.total
  } catch (error) {
    console.error('加载报告列表失败:', error)
  } finally {
    loading.value = false
  }
}

const changePage = (page) => {
  pagination.value.page = page
  loadReports()
}

const changePeriod = (days) => {
  period.value = days
}

const refreshData = async () => {
  loading.value = true
  await Promise.all([loadTrendData(), loadReports()])
  loading.value = false
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>

<style scoped>
.reports-page {
  min-height: 100%;
  background: #f8fafc;
  padding: 24px;
}

.page-content {
  background: white;
  border-radius: 2rem;
  padding: 0;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.page-header {
  position: relative;
  padding: var(--space-xl);
  background: linear-gradient(145deg, var(--ink-primary) 0%, var(--ink-deep) 100%);
  overflow: hidden;
}

.header-decoration {
  position: absolute;
  inset: 0;
  pointer-events: none;
  overflow: hidden;
}

.deco-blob {
  position: absolute;
  border-radius: 50%;
  pointer-events: none;
}

.deco-blob-1 {
  width: 200px;
  height: 200px;
  top: -50%;
  right: -5%;
  background: 
    radial-gradient(circle at 50% 50%, rgba(217, 119, 6, 0.25) 0%, rgba(217, 119, 6, 0.15) 30%, rgba(217, 119, 6, 0.08) 50%, transparent 70%);
}

.deco-blob-2 {
  width: 150px;
  height: 150px;
  bottom: -40%;
  left: 10%;
  background: 
    radial-gradient(circle at 50% 50%, rgba(251, 191, 36, 0.2) 0%, rgba(251, 191, 36, 0.12) 30%, rgba(251, 191, 36, 0.06) 50%, transparent 70%);
}

.title-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  min-height: 1.75rem;
  padding: 4px 12px;
  border-radius: var(--radius-full);
  font-size: 0.7rem;
  font-weight: 800;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  background: linear-gradient(135deg, rgba(217, 119, 6, 0.25), rgba(251, 191, 36, 0.15));
  color: var(--amber-soft);
  border: 1px solid rgba(217, 119, 6, 0.3);
  margin-bottom: var(--space-sm);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
  z-index: 1;
}

.title-section {
  color: white;
}

.page-title {
  font-size: 2rem;
  font-weight: 700;
  margin: 0 0 8px 0;
  display: flex;
  align-items: center;
  gap: 12px;
}

.title-icon {
  font-size: 2.5rem;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

.page-subtitle {
  font-size: 1rem;
  opacity: 0.9;
  margin: 0;
}

.btn-refresh {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 2px solid rgba(255, 255, 255, 0.3);
  padding: 10px 20px;
  border-radius: 12px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  backdrop-filter: blur(10px);
  transition: all 0.3s;
}

.btn-refresh:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: translateY(-2px);
}

.btn-refresh.spinning .refresh-icon {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.refresh-icon {
  font-size: 1.1rem;
}

.main-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  padding: 24px;
}

.left-panel,
.right-panel {
  min-width: 0;
}

.trend-section,
.reports-section {
  background: white;
  padding: 24px;
  border-radius: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  height: 100%;
  display: flex;
  flex-direction: column;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  flex-shrink: 0;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 12px;
}

.section-title .title-icon {
  font-size: 1.5rem;
  animation: none;
}

.section-title h2 {
  margin: 0;
  font-size: 1.25rem;
  color: #1f2937;
}

.section-actions {
  display: flex;
  gap: 8px;
}

.btn-period {
  padding: 8px 16px;
  border: 2px solid #e5e7eb;
  border-radius: 10px;
  background: white;
  color: #6b7280;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-period:hover {
  border-color: #667eea;
  color: #667eea;
}

.btn-period.active {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border-color: transparent;
}

.section-count {
  font-size: 0.9rem;
  color: #6b7280;
  font-weight: 500;
}

.chart-container {
  flex: 1;
  min-height: 300px;
  position: relative;
}

.empty-chart {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #6b7280;
  min-height: 300px;
}

.empty-chart .empty-icon {
  font-size: 4rem;
  margin-bottom: 16px;
  opacity: 0.5;
}

.empty-chart p {
  margin: 0;
  font-size: 0.95rem;
}

.reports-list {
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.report-card {
  background: white;
  border-radius: 16px;
  padding: 20px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid #e2e8f0;
  position: relative;
  overflow: hidden;
  flex-shrink: 0;
}

.report-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(102, 126, 234, 0.12);
  border-color: #667eea;
}

.card-glow {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #667eea, #764ba2);
  opacity: 0;
  transition: opacity 0.3s;
}

.report-card:hover .card-glow {
  opacity: 1;
}

.report-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.report-title {
  display: flex;
  align-items: center;
  gap: 10px;
}

.report-icon {
  font-size: 1.3rem;
}

.report-title h3 {
  margin: 0;
  font-size: 1rem;
  color: #1f2937;
}

.report-date {
  font-size: 0.8rem;
  color: #9ca3af;
}

.report-meta {
  display: flex;
  gap: 16px;
  margin-bottom: 12px;
  padding-bottom: 10px;
  border-bottom: 1px solid #f3f4f6;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.85rem;
  color: #6b7280;
}

.meta-icon {
  font-size: 0.9rem;
}

.report-stats {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  background: #f9fafb;
  border-radius: 10px;
}

.stat-icon {
  font-size: 1.3rem;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 1.1rem;
  font-weight: 700;
  color: #1f2937;
}

.stat-label {
  font-size: 0.75rem;
  color: #6b7280;
}

.stat-item.pass .stat-value {
  color: #10b981;
}

.stat-item.fail .stat-value {
  color: #ef4444;
}

.stat-bar {
  width: 50px;
  height: 5px;
  background: #e5e7eb;
  border-radius: 3px;
  overflow: hidden;
}

.stat-progress {
  height: 100%;
  border-radius: 3px;
  transition: width 0.5s ease;
}

.stat-item.pass .stat-progress {
  background: linear-gradient(90deg, #10b981, #059669);
}

.stat-item.fail .stat-progress {
  background: linear-gradient(90deg, #ef4444, #dc2626);
}

.empty-reports {
  text-align: center;
  padding: 40px 20px;
  color: #6b7280;
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.empty-reports .empty-icon {
  font-size: 4rem;
  margin-bottom: 16px;
  opacity: 0.5;
}

.empty-reports h3 {
  font-size: 1.2rem;
  color: #374151;
  margin: 0 0 8px 0;
}

.empty-reports p {
  margin: 0;
  color: #9ca3af;
  font-size: 0.9rem;
}

.loading-state {
  text-align: center;
  padding: 40px 20px;
  color: #6b7280;
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.loading-spinner {
  width: 36px;
  height: 36px;
  border: 3px solid #e5e7eb;
  border-top-color: #667eea;
  border-radius: 50%;
  margin-bottom: 12px;
  animation: spin 1s linear infinite;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #e5e7eb;
  flex-shrink: 0;
}

.btn-page {
  padding: 8px 16px;
  border: 2px solid #e5e7eb;
  border-radius: 10px;
  background: white;
  color: #374151;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-page:hover:not(:disabled) {
  border-color: #667eea;
  color: #667eea;
}

.btn-page:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-info {
  font-size: 0.85rem;
  color: #6b7280;
  font-weight: 500;
}

@media (max-width: 1200px) {
  .main-content {
    grid-template-columns: 1fr;
  }

  .chart-container {
    min-height: 250px;
  }
}

@media (max-width: 768px) {
  .reports-page {
    padding: 16px;
  }

  .page-header {
    padding: 24px;
  }

  .header-content {
    flex-direction: column;
    gap: 16px;
  }

  .page-title {
    font-size: 1.5rem;
  }

  .main-content {
    padding: 16px;
    gap: 16px;
  }

  .trend-section,
  .reports-section {
    padding: 16px;
  }

  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .report-stats {
    grid-template-columns: 1fr;
  }
}
</style>
