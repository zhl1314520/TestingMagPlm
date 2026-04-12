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
        </div>
        <div class="header-decoration">
          <div class="deco-blob deco-blob-1"></div>
          <div class="deco-blob deco-blob-2"></div>
        </div>
      </div>

      <div class="report-body">
        <div class="analytics-layout">
          <section class="panel trend-panel">
            <div class="panel-head">
              <div class="panel-title-wrap">
                <span class="panel-kicker">Trend</span>
                <h2 class="panel-title">趋势分析</h2>
              </div>
              <div class="panel-summary">
                <span class="summary-item summary-pass">通过率线</span>
                <span class="summary-item summary-fail">失败率线</span>
              </div>
            </div>

            <div class="chart-shell">
              <canvas ref="trendCanvas"></canvas>
            </div>
          </section>

          <section class="panel list-panel">
            <div class="panel-head">
              <div class="panel-title-wrap">
                <span class="panel-kicker">Forms</span>
                <h2 class="panel-title">报告表单</h2>
              </div>
              <div class="page-meta">
                第 {{ currentPage }} / {{ totalPages }} 页
              </div>
            </div>

            <div class="report-list">
              <article
                v-for="(item, index) in paddedReports"
                :key="item ? item.id : `placeholder-${index}`"
                class="report-card"
                :class="{ placeholder: !item }"
              >
                <template v-if="item">
                  <div class="card-top">
                    <div class="report-title">{{ item.title }}</div>
                    <div class="report-id">#{{ item.id }}</div>
                  </div>

                  <div class="card-grid">
                    <div class="meta-item">项目：{{ item.project_name }}</div>
                    <div class="meta-item">执行：{{ item.execution_name }}</div>
                    <div class="meta-item">创建人：{{ item.created_by_name }}</div>
                    <div class="meta-item">创建时间：{{ formatDate(item.created_at) }}</div>
                  </div>

                  <div class="rate-row">
                    <span>通过 {{ toPercent(item.pass_rate) }}</span>
                    <span>失败 {{ toPercent(item.fail_rate) }}</span>
                    <span>总用例 {{ item.total_cases }}</span>
                  </div>

                  <div class="rate-bar">
                    <span class="rate-fill" :style="{ width: `${Math.max(0, Math.min(100, Number(item.pass_rate) || 0))}%` }"></span>
                  </div>
                </template>

                <template v-else>
                  <div class="placeholder-text">当前页暂无更多报告记录</div>
                </template>
              </article>
            </div>

            <div class="pagination">
              <button class="page-btn" :disabled="currentPage <= 1 || loadingReports" @click="goToPage(currentPage - 1)">
                上一页
              </button>
              <button
                v-for="page in visiblePages"
                :key="page"
                class="page-btn page-number"
                :class="{ active: page === currentPage }"
                :disabled="loadingReports"
                @click="goToPage(page)"
              >
                {{ page }}
              </button>
              <button class="page-btn" :disabled="currentPage >= totalPages || loadingReports" @click="goToPage(currentPage + 1)">
                下一页
              </button>
            </div>
          </section>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import {
  Chart,
  CategoryScale,
  Filler,
  Legend,
  LineController,
  LineElement,
  LinearScale,
  PointElement,
  Tooltip
} from 'chart.js'
import { metricsAPI, reportAPI } from '../api/index.js'

Chart.register(
  LineController,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
  Filler
)

const PAGE_SIZE = 5
const MAX_PAGES = 15

const loadingReports = ref(false)
const reports = ref([])
const total = ref(0)
const currentPage = ref(1)

const trend = ref([])
const trendCanvas = ref(null)
const trendChart = ref(null)

const totalPages = computed(() => {
  const pages = Math.ceil((Number(total.value) || 0) / PAGE_SIZE)
  return Math.max(1, Math.min(MAX_PAGES, pages || 1))
})

const paddedReports = computed(() => {
  const cards = [...reports.value]
  while (cards.length < PAGE_SIZE) {
    cards.push(null)
  }
  return cards
})

const visiblePages = computed(() => {
  const pages = []
  for (let i = 1; i <= totalPages.value; i += 1) {
    pages.push(i)
  }
  return pages
})

const toPercent = (value) => `${Number(value || 0).toFixed(2)}%`

const formatDate = (value) => {
  if (!value) return '-'
  return new Date(value).toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const loadReports = async () => {
  loadingReports.value = true
  try {
    const response = await reportAPI.getList(currentPage.value, PAGE_SIZE)
    reports.value = response.data?.items || []
    total.value = response.data?.total || 0
    if (currentPage.value > totalPages.value) {
      currentPage.value = totalPages.value
      return loadReports()
    }
  } catch (error) {
    console.error('加载报告失败:', error)
    reports.value = []
    total.value = 0
  } finally {
    loadingReports.value = false
  }
}

const loadTrend = async () => {
  try {
    const response = await metricsAPI.getTrend()
    trend.value = response.data || []
  } catch (error) {
    console.error('加载趋势失败:', error)
    trend.value = []
  }
}

const buildTrendChart = () => {
  if (!trendCanvas.value) return

  if (trendChart.value) {
    trendChart.value.destroy()
  }

  const labels = trend.value.length
    ? trend.value.map((item) => item.date)
    : ['暂无数据']

  const passLine = trend.value.length
    ? trend.value.map((item) => Number(item.pass_rate || 0))
    : [0]

  const failLine = trend.value.length
    ? trend.value.map((item) => Number(item.fail_rate || 0))
    : [0]

  trendChart.value = new Chart(trendCanvas.value, {
    type: 'line',
    data: {
      labels,
      datasets: [
        {
          label: '通过率',
          data: passLine,
          borderColor: '#14b8a6',
          backgroundColor: 'rgba(20, 184, 166, 0.15)',
          borderWidth: 2.5,
          fill: true,
          tension: 0.35,
          pointRadius: 3,
          pointHoverRadius: 5
        },
        {
          label: '失败率',
          data: failLine,
          borderColor: '#e11d48',
          backgroundColor: 'rgba(225, 29, 72, 0.08)',
          borderWidth: 2.5,
          fill: false,
          tension: 0.35,
          pointRadius: 3,
          pointHoverRadius: 5
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: {
        mode: 'index',
        intersect: false
      },
      plugins: {
        legend: {
          labels: {
            usePointStyle: true,
            boxWidth: 8
          }
        }
      },
      scales: {
        x: {
          grid: {
            color: 'rgba(148, 163, 184, 0.16)'
          }
        },
        y: {
          min: 0,
          max: 100,
          ticks: {
            callback: (value) => `${value}%`
          },
          grid: {
            color: 'rgba(148, 163, 184, 0.16)'
          }
        }
      }
    }
  })
}

const goToPage = async (page) => {
  const target = Math.max(1, Math.min(totalPages.value, page))
  if (target === currentPage.value) return
  currentPage.value = target
  await loadReports()
}

watch(
  () => trend.value,
  async () => {
    await nextTick()
    buildTrendChart()
  },
  { deep: true }
)

onMounted(async () => {
  await Promise.all([loadReports(), loadTrend()])
  await nextTick()
  buildTrendChart()
})

onBeforeUnmount(() => {
  if (trendChart.value) {
    trendChart.value.destroy()
    trendChart.value = null
  }
})
</script>

<style scoped>
.reports-page {
  min-height: 100%;
  padding: var(--space-md);
}

.page-content {
  border-radius: var(--radius-xl);
  overflow: hidden;
  box-shadow: var(--shadow-lg);
  border: 1px solid rgba(232, 93, 4, 0.08);
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

.page-subtitle {
  font-size: 1rem;
  opacity: 0.9;
  margin: 0;
}

.report-body {
  padding: var(--space-xl);
  background: linear-gradient(180deg, rgba(232, 93, 4, 0.03), rgba(20, 184, 166, 0.02));
}

.analytics-layout {
  display: grid;
  grid-template-columns: 3fr 2fr;
  gap: var(--space-lg);
  align-items: stretch;
}

.panel {
  background: white;
  border-radius: var(--radius-lg);
  border: 1px solid rgba(232, 93, 4, 0.08);
  box-shadow: var(--shadow-sm);
  padding: var(--space-lg);
  min-height: 700px;
  display: flex;
  flex-direction: column;
}

.panel-head {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: var(--space-md);
  margin-bottom: var(--space-md);
}

.panel-kicker {
  display: inline-flex;
  min-height: 1.6rem;
  align-items: center;
  padding: 2px 10px;
  border-radius: var(--radius-full);
  font-size: 0.68rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--ember-core);
  background: linear-gradient(135deg, rgba(232, 93, 4, 0.12), rgba(250, 163, 7, 0.09));
}

.panel-title {
  margin: var(--space-xs) 0 0;
  font-size: 1.3rem;
  color: var(--ink-primary);
}

.panel-summary {
  display: flex;
  gap: var(--space-sm);
  flex-wrap: wrap;
}

.summary-item {
  padding: 4px 10px;
  border-radius: var(--radius-full);
  font-size: 0.76rem;
  font-weight: 700;
}

.summary-pass {
  color: var(--teal-primary);
  background: rgba(20, 184, 166, 0.12);
}

.summary-fail {
  color: var(--coral-primary);
  background: rgba(225, 29, 72, 0.1);
}

.chart-shell {
  position: relative;
  flex: 1;
  min-height: 580px;
  border-radius: var(--radius-md);
  background: linear-gradient(180deg, rgba(15, 23, 42, 0.01), rgba(20, 184, 166, 0.03));
  border: 1px solid rgba(148, 163, 184, 0.16);
  padding: var(--space-sm);
}

.page-meta {
  font-size: 0.86rem;
  color: var(--ink-soft);
  font-weight: 600;
}

.report-list {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
}

.report-card {
  border-radius: var(--radius-md);
  border: 1px solid rgba(232, 93, 4, 0.08);
  background: linear-gradient(135deg, rgba(232, 93, 4, 0.03), rgba(20, 184, 166, 0.02));
  padding: var(--space-md);
  min-height: 110px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.report-card.placeholder {
  justify-content: center;
  border-style: dashed;
  background: rgba(248, 250, 252, 0.7);
}

.placeholder-text {
  font-size: 0.86rem;
  color: var(--ink-soft);
  text-align: center;
}

.card-top {
  display: flex;
  justify-content: space-between;
  gap: var(--space-sm);
  align-items: center;
}

.report-title {
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--ink-primary);
  line-height: 1.4;
}

.report-id {
  font-size: 0.78rem;
  color: var(--ink-soft);
  background: rgba(148, 163, 184, 0.16);
  border-radius: var(--radius-full);
  padding: 2px 8px;
}

.card-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4px 10px;
}

.meta-item {
  font-size: 0.8rem;
  color: var(--ink-muted);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.rate-row {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-md);
  font-size: 0.78rem;
  color: var(--ink-secondary);
  font-weight: 600;
}

.rate-bar {
  width: 100%;
  height: 6px;
  border-radius: var(--radius-full);
  background: rgba(148, 163, 184, 0.18);
  overflow: hidden;
}

.rate-fill {
  display: block;
  height: 100%;
  border-radius: inherit;
  background: linear-gradient(90deg, var(--teal-primary), var(--teal-bright));
}

.pagination {
  margin-top: var(--space-md);
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-xs);
  justify-content: flex-end;
}

.page-btn {
  border: none;
  border-radius: var(--radius-sm);
  background: rgba(232, 93, 4, 0.06);
  color: var(--ink-secondary);
  min-height: 2rem;
  padding: 0 10px;
  font-size: 0.82rem;
  font-weight: 700;
  cursor: pointer;
}

.page-btn.page-number {
  min-width: 2rem;
}

.page-btn.active {
  background: linear-gradient(135deg, var(--ember-core), var(--ember-glow));
  color: white;
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

@media (max-width: 1200px) {
  .analytics-layout {
    grid-template-columns: 1fr;
  }

  .panel {
    min-height: 560px;
  }

  .chart-shell {
    min-height: 420px;
  }
}

@media (max-width: 768px) {
  .report-body {
    padding: var(--space-md);
  }

  .page-header {
    padding: var(--space-lg);
  }

  .page-title {
    font-size: 1.5rem;
  }

  .card-grid {
    grid-template-columns: 1fr;
  }
}
</style>
