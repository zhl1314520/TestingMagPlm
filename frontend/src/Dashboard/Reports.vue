<template>
  <div class="reports-page">
    <div class="page-content">
      <div class="page-header">
      <div class="header-content">
        <div class="title-section">
          <h1 class="page-title">
            <span class="title-icon">📊</span>
            报告统计
          </h1>
          <p class="page-subtitle">数据驱动质量改进</p>
        </div>
        <button @click="refreshData" class="btn-refresh" :class="{ spinning: loading }">
          <span class="refresh-icon">🔄</span>
          刷新数据
        </button>
      </div>
    </div>

    <div class="metrics-section">
      <div class="metrics-grid">
        <div class="metric-card projects">
          <div class="metric-glow"></div>
          <div class="metric-icon">
            <span class="icon-bg"></span>
            <span class="icon-emoji">📁</span>
          </div>
          <div class="metric-content">
            <div class="metric-value">{{ metrics.total_projects }}</div>
            <div class="metric-label">项目总数</div>
            <div class="metric-trend positive">
              <span class="trend-icon">↑</span>
              <span>12% 增长</span>
            </div>
          </div>
          <div class="metric-ring">
            <svg viewBox="0 0 36 36">
              <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="#e2e8f0" stroke-width="3"/>
              <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="#667eea" stroke-width="3" stroke-dasharray="75, 100"/>
            </svg>
          </div>
        </div>

        <div class="metric-card testcases">
          <div class="metric-glow"></div>
          <div class="metric-icon">
            <span class="icon-bg"></span>
            <span class="icon-emoji">📝</span>
          </div>
          <div class="metric-content">
            <div class="metric-value">{{ metrics.total_testcases }}</div>
            <div class="metric-label">测试用例</div>
            <div class="metric-trend positive">
              <span class="trend-icon">↑</span>
              <span>8% 增长</span>
            </div>
          </div>
          <div class="metric-ring">
            <svg viewBox="0 0 36 36">
              <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="#e2e8f0" stroke-width="3"/>
              <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="#10b981" stroke-width="3" stroke-dasharray="80, 100"/>
            </svg>
          </div>
        </div>

        <div class="metric-card bugs">
          <div class="metric-glow"></div>
          <div class="metric-icon">
            <span class="icon-bg"></span>
            <span class="icon-emoji">🐛</span>
          </div>
          <div class="metric-content">
            <div class="metric-value">{{ metrics.total_bugs }}</div>
            <div class="metric-label">缺陷数量</div>
            <div class="metric-trend negative">
              <span class="trend-icon">↓</span>
              <span>5% 减少</span>
            </div>
          </div>
          <div class="metric-ring">
            <svg viewBox="0 0 36 36">
              <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="#e2e8f0" stroke-width="3"/>
              <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="#f59e0b" stroke-width="3" stroke-dasharray="40, 100"/>
            </svg>
          </div>
        </div>

        <div class="metric-card executions">
          <div class="metric-glow"></div>
          <div class="metric-icon">
            <span class="icon-bg"></span>
            <span class="icon-emoji">▶️</span>
          </div>
          <div class="metric-content">
            <div class="metric-value">{{ metrics.total_executions }}</div>
            <div class="metric-label">执行次数</div>
            <div class="metric-trend positive">
              <span class="trend-icon">↑</span>
              <span>15% 增长</span>
            </div>
          </div>
          <div class="metric-ring">
            <svg viewBox="0 0 36 36">
              <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="#e2e8f0" stroke-width="3"/>
              <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="#764ba2" stroke-width="3" stroke-dasharray="90, 100"/>
            </svg>
          </div>
        </div>
      </div>
    </div>

    <div class="trend-section">
      <div class="section-header">
        <div class="section-title">
          <span class="title-icon">📈</span>
          <h2>趋势分析</h2>
        </div>
        <div class="section-actions">
          <button class="btn-period active">7 天</button>
          <button class="btn-period">30 天</button>
          <button class="btn-period">90 天</button>
        </div>
      </div>

      <div class="trend-chart">
        <div v-for="(item, index) in trendData" :key="index" class="trend-item">
          <div class="trend-date">{{ item.date }}</div>
          <div class="trend-bars">
            <div class="bar-container">
              <div class="trend-bar pass" :style="{ width: item.pass_rate * 100 + '%' }">
                <span class="bar-label">通过率：{{ (item.pass_rate * 100).toFixed(1) }}%</span>
              </div>
            </div>
            <div class="bar-container">
              <div class="trend-bar fail" :style="{ width: item.fail_rate * 100 + '%' }">
                <span class="bar-label">失败率：{{ (item.fail_rate * 100).toFixed(1) }}%</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="reports-section">
      <div class="section-header">
        <div class="section-title">
          <span class="title-icon">📋</span>
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
        <div class="empty-icon">📄</div>
        <h3>暂无报告</h3>
        <p>测试执行后将自动生成报告</p>
      </div>

      <div v-else class="reports-list">
        <div v-for="report in reports" :key="report.id" class="report-card">
          <div class="report-header">
            <div class="report-title">
              <span class="report-icon">📊</span>
              <h3>{{ report.title }}</h3>
            </div>
            <div class="report-date">{{ formatDate(report.created_at) }}</div>
          </div>

          <div class="report-meta">
            <div class="meta-item">
              <span class="meta-icon">📁</span>
              <span>项目ID: {{ report.project_id }}</span>
            </div>
            <div class="meta-item">
              <span class="meta-icon">📝</span>
              <span>总用例: {{ report.total_cases }}</span>
            </div>
          </div>

          <div class="report-stats">
            <div class="stat-item pass">
              <div class="stat-icon">✅</div>
              <div class="stat-content">
                <div class="stat-value">{{ report.passed_cases }}</div>
                <div class="stat-label">通过 ({{ (report.pass_rate * 100).toFixed(1) }}%)</div>
              </div>
              <div class="stat-bar">
                <div class="stat-progress" :style="{ width: report.pass_rate * 100 + '%' }"></div>
              </div>
            </div>

            <div class="stat-item fail">
              <div class="stat-icon">❌</div>
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
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { reportAPI, metricsAPI } from '../api/index.js'

const loading = ref(false)
const metrics = ref({
  total_projects: 0,
  total_testcases: 0,
  total_bugs: 0,
  total_executions: 0
})

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
  await Promise.all([loadMetrics(), loadTrendData(), loadReports()])
})

const loadMetrics = async () => {
  try {
    const response = await metricsAPI.getOverview()
    metrics.value = response.data
  } catch (error) {
    console.error('获取概览数据失败:', error)
  }
}

const loadTrendData = async () => {
  try {
    const response = await metricsAPI.getTrend()
    trendData.value = response.data
  } catch (error) {
    console.error('获取趋势数据失败:', error)
  }
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

const refreshData = async () => {
  loading.value = true
  await Promise.all([loadMetrics(), loadTrendData(), loadReports()])
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
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  margin: -24px -24px 32px -24px;
  padding: 32px;
  position: relative;
  overflow: hidden;
  border-radius: 2rem 2rem 0 0;
}

.page-header::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -10%;
  width: 300px;
  height: 300px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  animation: float 6s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-20px) rotate(5deg); }
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

.metrics-section {
  padding: 0 24px 32px;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 24px;
}

.metric-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  position: relative;
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid #e2e8f0;
}

.metric-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
}

.metric-glow {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  opacity: 0;
  transition: opacity 0.3s;
}

.metric-card:hover .metric-glow {
  opacity: 1;
}

.metric-card.projects .metric-glow {
  background: linear-gradient(90deg, #667eea, #764ba2);
}

.metric-card.testcases .metric-glow {
  background: linear-gradient(90deg, #10b981, #059669);
}

.metric-card.bugs .metric-glow {
  background: linear-gradient(90deg, #f59e0b, #d97706);
}

.metric-card.executions .metric-glow {
  background: linear-gradient(90deg, #764ba2, #667eea);
}

.metric-icon {
  width: 56px;
  height: 56px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  margin-bottom: 16px;
}

.metric-card.projects .metric-icon {
  background: linear-gradient(135deg, #667eea, #764ba2);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
}

.metric-card.testcases .metric-icon {
  background: linear-gradient(135deg, #10b981, #059669);
  box-shadow: 0 8px 20px rgba(16, 185, 129, 0.3);
}

.metric-card.bugs .metric-icon {
  background: linear-gradient(135deg, #f59e0b, #d97706);
  box-shadow: 0 8px 20px rgba(245, 158, 11, 0.3);
}

.metric-card.executions .metric-icon {
  background: linear-gradient(135deg, #764ba2, #667eea);
  box-shadow: 0 8px 20px rgba(118, 75, 162, 0.3);
}

.icon-bg {
  position: absolute;
  inset: -2px;
  background: inherit;
  border-radius: 14px;
  opacity: 0.3;
  animation: rotate 3s linear infinite;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.icon-emoji {
  font-size: 1.8rem;
  position: relative;
  z-index: 1;
}

.metric-content {
  margin-bottom: 16px;
}

.metric-value {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 4px;
}

.metric-label {
  font-size: 0.9rem;
  color: #6b7280;
  margin-bottom: 8px;
}

.metric-trend {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 0.85rem;
  font-weight: 600;
}

.metric-trend.positive {
  color: #10b981;
}

.metric-trend.negative {
  color: #ef4444;
}

.trend-icon {
  font-size: 1rem;
}

.metric-ring {
  position: absolute;
  top: 20px;
  right: 20px;
  width: 60px;
  height: 60px;
}

.metric-ring svg {
  transform: rotate(-90deg);
}

.trend-section,
.reports-section {
  background: white;
  margin: 0 24px 24px;
  padding: 24px;
  border-radius: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 12px;
}

.title-icon {
  font-size: 1.5rem;
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

.trend-chart {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.trend-item {
  display: flex;
  align-items: center;
  gap: 16px;
}

.trend-date {
  width: 60px;
  font-size: 0.85rem;
  font-weight: 500;
  color: #6b7280;
}

.trend-bars {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.bar-container {
  height: 28px;
  background: #f3f4f6;
  border-radius: 8px;
  overflow: hidden;
  position: relative;
}

.trend-bar {
  height: 100%;
  display: flex;
  align-items: center;
  padding: 0 12px;
  transition: width 0.5s ease;
  position: relative;
}

.trend-bar.pass {
  background: linear-gradient(90deg, #10b981, #059669);
}

.trend-bar.fail {
  background: linear-gradient(90deg, #ef4444, #dc2626);
}

.bar-label {
  font-size: 0.75rem;
  color: white;
  font-weight: 600;
  white-space: nowrap;
}

.reports-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.report-card {
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 20px;
  transition: all 0.3s;
}

.report-card:hover {
  border-color: #667eea;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.1);
}

.report-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.report-title {
  display: flex;
  align-items: center;
  gap: 12px;
}

.report-icon {
  font-size: 1.5rem;
}

.report-title h3 {
  margin: 0;
  font-size: 1.1rem;
  color: #1f2937;
}

.report-date {
  font-size: 0.85rem;
  color: #9ca3af;
}

.report-stats {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: #f9fafb;
  border-radius: 10px;
}

.stat-icon {
  font-size: 1.5rem;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1f2937;
}

.stat-label {
  font-size: 0.8rem;
  color: #6b7280;
}

.stat-item.pass .stat-value {
  color: #10b981;
}

.stat-item.fail .stat-value {
  color: #ef4444;
}

.stat-bar {
  width: 60px;
  height: 6px;
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
  padding: 60px 20px;
  color: #6b7280;
}

.empty-reports .empty-icon {
  font-size: 5rem;
  margin-bottom: 24px;
  opacity: 0.5;
}

.empty-reports h3 {
  font-size: 1.5rem;
  color: #374151;
  margin: 0 0 8px 0;
}

.empty-reports p {
  margin: 0;
  color: #9ca3af;
}

.loading-state {
  text-align: center;
  padding: 60px 20px;
  color: #6b7280;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #e5e7eb;
  border-top-color: #667eea;
  border-radius: 50%;
  margin: 0 auto 16px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.report-meta {
  display: flex;
  gap: 24px;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid #f3f4f6;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.9rem;
  color: #6b7280;
}

.meta-icon {
  font-size: 1rem;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid #e5e7eb;
}

.btn-page {
  padding: 10px 20px;
  border: 2px solid #e5e7eb;
  border-radius: 10px;
  background: white;
  color: #374151;
  font-size: 0.9rem;
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
  font-size: 0.9rem;
  color: #6b7280;
  font-weight: 500;
}

@media (max-width: 768px) {
  .page-header {
    padding: 24px;
    margin: -16px -16px 24px -16px;
  }

  .header-content {
    flex-direction: column;
    gap: 16px;
  }

  .page-title {
    font-size: 1.5rem;
  }

  .metrics-grid {
    grid-template-columns: 1fr;
    padding: 0 16px 16px;
  }

  .trend-section,
  .reports-section {
    margin: 0 16px 16px;
    padding: 16px;
  }

  .report-stats {
    grid-template-columns: 1fr;
  }
}
</style>
