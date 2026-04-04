<template>
  <div class="overview">
    <section class="hero-stage">
      <div class="hero-panel">
        <div class="hero-grid">
          <div class="hero-copy">
            <div class="hero-meta">
              <span class="hero-pill">Overview Console</span>
              <span class="hero-date">{{ todayLabel }}</span>
            </div>

            <h1 class="hero-title">
              <span class="hero-title-small">{{ greetingText }}</span>
              <span class="hero-title-main">{{ userInfo?.username || '伙伴' }}</span>
            </h1>

            <p class="hero-subtitle">
              把项目、测试、执行与缺陷放进同一张质量视图里，让每一次迭代都更可见、更可控。
            </p>

            <div class="hero-highlights">
              <div
                v-for="highlight in heroHighlights"
                :key="highlight.label"
                class="hero-highlight"
              >
                <span class="hero-highlight-label">{{ highlight.label }}</span>
                <strong class="hero-highlight-value">{{ highlight.value }}</strong>
              </div>
            </div>
          </div>

          <div class="hero-visual" aria-hidden="true">
            <div class="visual-aurora aurora-one"></div>
            <div class="visual-aurora aurora-two"></div>
            <div class="visual-core-ring"></div>
            <div class="visual-core"></div>
            <div class="visual-spark spark-one"></div>
            <div class="visual-spark spark-two"></div>
            <div class="visual-spark spark-three"></div>

            <div class="visual-orbit orbit-large">
              <span class="orbit-dot"></span>
            </div>
            <div class="visual-orbit orbit-medium">
              <span class="orbit-dot"></span>
            </div>
            <div class="visual-orbit orbit-small">
              <span class="orbit-dot"></span>
            </div>

            <article class="signal-card signal-primary">
              <span class="signal-kicker">Quality Pulse</span>
              <strong class="signal-value">{{ totalAssets }}</strong>
              <span class="signal-label">当前平台沉淀的质量资产</span>

              <div class="signal-track">
                <span class="signal-track-fill"></span>
              </div>

              <div class="signal-tags">
                <span>项目</span>
                <span>用例</span>
                <span>执行</span>
                <span>缺陷</span>
              </div>
            </article>

            <article class="signal-card signal-secondary signal-secondary-top">
              <span class="signal-mini-label">自动化节奏</span>
              <strong class="signal-mini-value">{{ metrics.total_executions }}</strong>
              <span class="signal-mini-foot">本视图聚焦执行动能</span>
            </article>

            <article class="signal-card signal-secondary signal-secondary-bottom">
              <span class="signal-mini-label">缺陷观察</span>
              <strong class="signal-mini-value">{{ metrics.total_bugs }}</strong>
              <span class="signal-mini-foot">快速定位风险变化</span>
            </article>
          </div>
        </div>
      </div>

      <div class="insight-board">
        <div class="insight-header">
          <div class="header-title">
            <span class="title-badge">Data Insights</span>
            <h2>数据洞察</h2>
            <p>首屏直接看到核心指标，不需要再往下找重点。</p>
          </div>

          <button class="refresh-btn" @click="loadMetrics" :disabled="loading">
            <span class="refresh-icon" :class="{ spinning: loading }">↻</span>
            <span>刷新</span>
          </button>
        </div>

        <div class="insight-grid">
          <article
            v-for="card in insightCards"
            :key="card.key"
            class="insight-card"
            :class="card.theme"
          >
            <div class="insight-card-shine"></div>

            <div class="insight-topline">
              <span class="insight-icon">{{ card.icon }}</span>
              <span class="insight-kicker">{{ card.kicker }}</span>
            </div>

            <div class="insight-number">{{ card.value }}</div>
            <div class="insight-label">{{ card.label }}</div>

            <div class="insight-bottom">
              <div class="insight-trend" :class="card.trendClass">
                <span class="trend-arrow">{{ card.trendIcon }}</span>
                <span>{{ card.trend }}</span>
              </div>

              <div class="insight-ring">
                <svg viewBox="0 0 36 36" aria-hidden="true">
                  <path
                    d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                    fill="none"
                    stroke="rgba(255,255,255,0.18)"
                    stroke-width="3"
                  />
                  <path
                    d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                    fill="none"
                    stroke="white"
                    stroke-width="3"
                    :stroke-dasharray="`${card.progress}, 100`"
                  />
                </svg>
              </div>
            </div>
          </article>
        </div>
      </div>
    </section>

    <section class="overview-lower">
      <div class="quick-actions-section">
        <div class="section-header">
          <div class="header-title">
            <span class="title-badge">Project Progress</span>
            <h2>项目进展</h2>
            <p>实时追踪你参与的项目进度，掌握测试用例完成情况。</p>
          </div>
        </div>

        <div class="project-progress-list" v-if="projectProgress.length > 0">
          <div
            v-for="(project, index) in projectProgress"
            :key="project.project_id"
            class="project-progress-item"
          >
            <div class="project-header" @click="toggleProject(project.project_id)">
              <div class="project-info">
                <div class="project-name">
                  <span class="expand-icon" :class="{ expanded: expandedProjects.includes(project.project_id) }">▶</span>
                  {{ project.project_name }}
                </div>
                <div class="project-stats">
                  <span class="stat-item">
                    <span class="stat-label">总用例</span>
                    <span class="stat-value">{{ project.total_testcases }}</span>
                  </span>
                  <span class="stat-divider">|</span>
                  <span class="stat-item">
                    <span class="stat-label">已完成</span>
                    <span class="stat-value">{{ project.completed_testcases }}</span>
                  </span>
                </div>
              </div>
              <div class="progress-container">
                <div class="progress-bar">
                  <div 
                    class="progress-fill" 
                    :style="{ 
                      width: project.progress_percentage + '%',
                      background: `linear-gradient(90deg, ${getProjectColor(project.project_id, index).start}, ${getProjectColor(project.project_id, index).end})`
                    }"
                  ></div>
                </div>
                <div class="progress-percentage">{{ project.progress_percentage }}%</div>
              </div>
            </div>
            
            <div class="modules-list" v-if="expandedProjects.includes(project.project_id) && project.modules.length > 0">
              <div
                v-for="module in project.modules"
                :key="module.module_name"
                class="module-item"
              >
                <div class="module-info">
                  <div class="module-name">{{ module.module_name }}</div>
                  <div class="module-stats">
                    <span class="stat-item">
                      <span class="stat-label">总用例</span>
                      <span class="stat-value">{{ module.total_testcases }}</span>
                    </span>
                    <span class="stat-divider">|</span>
                    <span class="stat-item">
                      <span class="stat-label">已完成</span>
                      <span class="stat-value">{{ module.completed_testcases }}</span>
                    </span>
                  </div>
                </div>
                <div class="progress-container">
                  <div class="progress-bar module-bar">
                    <div 
                      class="progress-fill" 
                      :style="{ 
                        width: module.progress_percentage + '%',
                        background: `linear-gradient(90deg, ${getProjectColor(project.project_id, index).start}, ${getProjectColor(project.project_id, index).end})`
                      }"
                    ></div>
                  </div>
                  <div class="progress-percentage">{{ module.progress_percentage }}%</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="empty-state" v-else>
          <div class="empty-icon">📊</div>
          <div class="empty-text">暂无项目数据</div>
          <div class="empty-hint">你还没有参与任何项目，请联系管理员添加</div>
        </div>
      </div>

      <div class="activity-section">
        <div class="section-header">
          <div class="header-title">
            <span class="title-badge">Live Feed</span>
            <h2>最近活动</h2>
            <p>把最近发生的关键动作串成一条时间线，方便你快速感知当前节奏。</p>
          </div>

          <router-link to="/dashboard/reports" class="view-all-link">
            查看全部
            <span class="link-arrow">→</span>
          </router-link>
        </div>

        <div class="activity-timeline">
          <div
            v-for="activity in recentActivities"
            :key="`${activity.title}-${activity.time}`"
            class="activity-item"
          >
            <div class="activity-line"></div>
            <div class="activity-dot" :class="activity.type"></div>

            <article class="activity-card">
              <div class="activity-card-head">
                <span class="activity-badge" :class="activity.type">{{ activity.badge }}</span>
                <span class="activity-time">{{ activity.time }}</span>
              </div>

              <div class="activity-title">{{ activity.title }}</div>
              <div class="activity-desc">{{ activity.description }}</div>
            </article>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { metricsAPI } from '../api/index.js'

const metrics = ref({
  total_projects: 0,
  total_testcases: 0,
  total_bugs: 0,
  total_executions: 0
})

const userInfo = ref(null)
const loading = ref(false)
const projectProgress = ref([])
const expandedProjects = ref([])

const projectColors = [
  { start: '#667eea', end: '#764ba2' },
  { start: '#f093fb', end: '#f5576c' },
  { start: '#4facfe', end: '#00f2fe' },
  { start: '#43e97b', end: '#38f9d7' },
  { start: '#fa709a', end: '#fee140' },
  { start: '#a18cd1', end: '#fbc2eb' },
  { start: '#ff9a9e', end: '#fecfef' },
  { start: '#ffecd2', end: '#fcb69f' },
  { start: '#a1c4fd', end: '#c2e9fb' },
  { start: '#d299c2', end: '#fef9d7' },
  { start: '#89f7fe', end: '#66a6ff' },
  { start: '#cd9cf2', end: '#f6f3ff' },
  { start: '#fddb92', end: '#d1fdff' },
  { start: '#9890e3', end: '#b1f4cf' },
  { start: '#ebc0fd', end: '#d9ded8' }
]

const getProjectColor = (projectId, index) => {
  const colorIndex = (projectId + index) % projectColors.length
  return projectColors[colorIndex]
}

const todayLabel = computed(() => {
  return new Intl.DateTimeFormat('zh-CN', {
    month: 'long',
    day: 'numeric',
    weekday: 'long'
  }).format(new Date())
})

const greetingText = computed(() => {
  const hour = new Date().getHours()

  if (hour < 12) {
    return '早上好'
  }

  if (hour < 18) {
    return '下午好'
  }

  return '晚上好'
})

const totalAssets = computed(() => {
  return (
    metrics.value.total_projects +
    metrics.value.total_testcases +
    metrics.value.total_bugs +
    metrics.value.total_executions
  )
})

const heroHighlights = computed(() => [
  {
    label: '项目轨道',
    value: `${metrics.value.total_projects} 个活跃项目`
  },
  {
    label: '用例储备',
    value: `${metrics.value.total_testcases} 条测试资产`
  },
  {
    label: '执行动能',
    value: `${metrics.value.total_executions} 次运行记录`
  }
])

const insightCards = computed(() => {
  // 计算每个指标的百分比（基于总数）
  const total = totalAssets.value || 1
  return [
    {
      key: 'projects',
      theme: 'theme-violet',
      icon: '📁',
      kicker: 'Project Scope',
      label: '项目总数',
      value: metrics.value.total_projects,
      trend: '12% 增长',
      trendClass: 'positive',
      trendIcon: '↑',
      progress: Math.round((metrics.value.total_projects / total) * 100) || 0
    },
    {
      key: 'testcases',
      theme: 'theme-rose',
      icon: '📝',
      kicker: 'Coverage Base',
      label: '测试用例',
      value: metrics.value.total_testcases,
      trend: '8% 增长',
      trendClass: 'positive',
      trendIcon: '↑',
      progress: Math.round((metrics.value.total_testcases / total) * 100) || 0
    },
    {
      key: 'bugs',
      theme: 'theme-cyan',
      icon: '🐛',
      kicker: 'Risk Signals',
      label: '缺陷数量',
      value: metrics.value.total_bugs,
      trend: '5% 减少',
      trendClass: 'negative',
      trendIcon: '↓',
      progress: Math.round((metrics.value.total_bugs / total) * 100) || 0
    },
    {
      key: 'executions',
      theme: 'theme-green',
      icon: '▶️',
      kicker: 'Automation Pace',
      label: '执行次数',
      value: metrics.value.total_executions,
      trend: '15% 增长',
      trendClass: 'positive',
      trendIcon: '↑',
      progress: Math.round((metrics.value.total_executions / total) * 100) || 0
    }
  ]
})

const toggleProject = (projectId) => {
  const index = expandedProjects.value.indexOf(projectId)
  if (index > -1) {
    expandedProjects.value.splice(index, 1)
  } else {
    expandedProjects.value.push(projectId)
  }
}

const recentActivities = [
  {
    type: 'success',
    badge: '完成',
    time: '2 小时前',
    title: '测试执行完成',
    description: '项目 A 的接口回归已结束，当前通过率稳定在 95%。'
  },
  {
    type: 'warning',
    badge: '新增',
    time: '5 小时前',
    title: '发现新缺陷',
    description: '项目 B 的登录模块出现高优先级问题，已进入跟踪流程。'
  },
  {
    type: 'info',
    badge: '创建',
    time: '1 天前',
    title: '项目创建',
    description: '新项目 C 已建立，团队开始补充基础测试用例。'
  },
  {
    type: 'success',
    badge: '更新',
    time: '2 天前',
    title: '测试用例更新',
    description: '项目 A 新增 10 条核心路径验证，用于下一轮回归。'
  }
]

onMounted(async () => {
  const storedUserInfo = localStorage.getItem('user_info')
  if (storedUserInfo) {
    userInfo.value = JSON.parse(storedUserInfo)
  }

  await loadMetrics()
  await loadProjectProgress()
})

const loadMetrics = async () => {
  loading.value = true
  try {
    const response = await metricsAPI.getOverview()
    metrics.value = response.data
  } catch (error) {
    console.error('获取概览数据失败:', error)
  } finally {
    loading.value = false
  }
}

const loadProjectProgress = async () => {
  try {
    const response = await metricsAPI.getProjectProgress()
    projectProgress.value = response.data.projects || []
  } catch (error) {
    console.error('获取项目进展失败:', error)
  }
}
</script>

<style scoped>
.overview {
  --page-ink: #10203a;
  --page-muted: #62718d;
  --page-soft: #edf2ff;
  --panel-bg: rgba(255, 255, 255, 0.92);
  --panel-border: rgba(255, 255, 255, 0.36);
  --shadow-strong: 0 22px 50px rgba(16, 32, 58, 0.14);
  --shadow-soft: 0 10px 28px rgba(16, 32, 58, 0.08);
  padding: 0;
}

.hero-stage {
  position: relative;
  margin-bottom: 2.25rem;
}

.hero-panel {
  position: relative;
  overflow: hidden;
  border-radius: 2rem;
  padding: 2rem 2rem 8.75rem;
  background:
    radial-gradient(circle at 12% 18%, rgba(255, 255, 255, 0.26), transparent 28%),
    radial-gradient(circle at 82% 28%, rgba(255, 201, 216, 0.24), transparent 24%),
    radial-gradient(circle at 74% 78%, rgba(121, 214, 255, 0.18), transparent 20%),
    linear-gradient(135deg, #4f6cf3 0%, #6c58eb 38%, #8f4ec9 100%);
  box-shadow: var(--shadow-strong);
}

.hero-panel::before,
.hero-panel::after {
  content: '';
  position: absolute;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.08);
  filter: blur(1px);
}

.hero-panel::before {
  width: 280px;
  height: 280px;
  right: -80px;
  top: -50px;
}

.hero-panel::after {
  width: 180px;
  height: 180px;
  left: -40px;
  bottom: 26px;
}

.hero-grid {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: minmax(0, 1.05fr) minmax(300px, 0.95fr);
  gap: 2rem;
  align-items: center;
}

.hero-copy {
  color: white;
}

.hero-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  align-items: center;
  margin-bottom: 1.25rem;
}

.hero-pill,
.hero-date {
  display: inline-flex;
  align-items: center;
  min-height: 2.25rem;
  padding: 0.45rem 0.9rem;
  border-radius: 999px;
  font-size: 0.85rem;
  font-weight: 700;
  letter-spacing: 0.04em;
}

.hero-pill {
  color: #fff;
  background: rgba(255, 255, 255, 0.18);
  border: 1px solid rgba(255, 255, 255, 0.24);
  backdrop-filter: blur(16px);
}

.hero-date {
  color: rgba(255, 255, 255, 0.9);
  background: rgba(7, 17, 43, 0.18);
  border: 1px solid rgba(255, 255, 255, 0.12);
}

.hero-title {
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.hero-title-small {
  font-size: 1.35rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.88);
}

.hero-title-main {
  font-size: clamp(3.2rem, 5vw, 4.8rem);
  line-height: 0.95;
  letter-spacing: -0.06em;
  font-weight: 800;
  color: #fff;
  text-shadow: 0 10px 30px rgba(15, 23, 42, 0.24);
}

.hero-subtitle {
  max-width: 38rem;
  margin: 1.25rem 0 0;
  font-size: 1.05rem;
  line-height: 1.85;
  color: rgba(255, 255, 255, 0.9);
}

.hero-highlights {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.9rem;
  margin-top: 1.75rem;
}

.hero-highlight {
  padding: 1rem 1.05rem;
  border-radius: 1.25rem;
  background: rgba(255, 255, 255, 0.14);
  border: 1px solid rgba(255, 255, 255, 0.14);
  backdrop-filter: blur(16px);
}

.hero-highlight-label {
  display: block;
  font-size: 0.78rem;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: rgba(255, 255, 255, 0.72);
}

.hero-highlight-value {
  display: block;
  margin-top: 0.45rem;
  font-size: 0.98rem;
  line-height: 1.45;
  color: white;
}

.hero-visual {
  position: relative;
  min-height: 320px;
  isolation: isolate;
}

.visual-aurora,
.visual-core-ring,
.visual-core,
.visual-spark,
.visual-orbit {
  position: absolute;
}

.visual-aurora {
  border-radius: 50%;
  filter: blur(10px);
  opacity: 0.75;
  z-index: 0;
  animation: auroraDrift 16s ease-in-out infinite;
}

.aurora-one {
  width: 220px;
  height: 220px;
  right: 36px;
  top: 18px;
  background: radial-gradient(circle, rgba(255, 228, 236, 0.24), rgba(255, 255, 255, 0));
}

.aurora-two {
  width: 164px;
  height: 164px;
  right: 112px;
  bottom: 34px;
  background: radial-gradient(circle, rgba(127, 228, 255, 0.22), rgba(255, 255, 255, 0));
  animation-duration: 18s;
  animation-delay: -6s;
}

.visual-core {
  width: 112px;
  height: 112px;
  right: 112px;
  top: 96px;
  border-radius: 50%;
  z-index: 1;
  background:
    radial-gradient(circle at 35% 35%, rgba(255, 255, 255, 0.84), rgba(255, 255, 255, 0.16) 34%, rgba(255, 255, 255, 0.02) 72%),
    linear-gradient(145deg, rgba(255, 219, 235, 0.44), rgba(121, 214, 255, 0.18));
  box-shadow:
    0 0 0 1px rgba(255, 255, 255, 0.16),
    0 24px 42px rgba(13, 21, 48, 0.18);
  animation: coreFloat 10s ease-in-out infinite;
}

.visual-core-ring {
  width: 172px;
  height: 172px;
  right: 82px;
  top: 66px;
  border-radius: 50%;
  z-index: 1;
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow:
    inset 0 0 0 14px rgba(255, 255, 255, 0.035),
    0 0 24px rgba(255, 255, 255, 0.08);
  animation: haloSpin 24s linear infinite;
}

.visual-spark {
  border-radius: 50%;
  z-index: 2;
  background: rgba(255, 255, 255, 0.82);
  box-shadow: 0 0 14px rgba(255, 255, 255, 0.55);
}

.spark-one {
  width: 8px;
  height: 8px;
  right: 92px;
  top: 54px;
  animation: sparkPulse 4.4s ease-in-out infinite;
}

.spark-two {
  width: 6px;
  height: 6px;
  right: 34px;
  top: 154px;
  animation: sparkPulse 5.8s ease-in-out infinite -1.4s;
}

.spark-three {
  width: 5px;
  height: 5px;
  right: 192px;
  bottom: 52px;
  animation: sparkPulse 4.8s ease-in-out infinite -2.1s;
}

.visual-orbit {
  border-radius: 50%;
  border: 1px solid rgba(255, 255, 255, 0.18);
  background: rgba(255, 255, 255, 0.045);
  box-shadow:
    inset 0 0 0 1px rgba(255, 255, 255, 0.04),
    0 10px 32px rgba(18, 26, 58, 0.08);
  z-index: 1;
  animation: orbitalFloat 14s ease-in-out infinite;
}

.orbit-dot {
  position: absolute;
  inset: -1px;
  animation: orbitDotSpin 18s linear infinite;
}

.orbit-dot::before {
  content: '';
  position: absolute;
  top: -4px;
  left: 50%;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  transform: translateX(-50%);
  background: rgba(255, 255, 255, 0.96);
  box-shadow:
    0 0 0 5px rgba(255, 255, 255, 0.08),
    0 0 18px rgba(255, 255, 255, 0.48);
}

.orbit-large {
  width: 250px;
  height: 250px;
  right: 8px;
  top: 8px;
  animation-duration: 17s;
}

.orbit-medium {
  width: 148px;
  height: 148px;
  right: 132px;
  bottom: 16px;
  animation-duration: 13s;
  animation-delay: -4s;
}

.orbit-small {
  width: 92px;
  height: 92px;
  right: 0;
  bottom: 36px;
  animation-duration: 11s;
  animation-delay: -7s;
}

.orbit-large .orbit-dot {
  animation-duration: 24s;
}

.orbit-medium .orbit-dot {
  animation-duration: 16s;
}

.orbit-small .orbit-dot {
  animation-duration: 11s;
}

.signal-card {
  position: absolute;
  border-radius: 1.6rem;
  backdrop-filter: blur(18px);
  box-shadow: 0 16px 36px rgba(15, 23, 42, 0.16);
  z-index: 3;
}

.signal-primary {
  left: 20px;
  top: 46px;
  width: min(100%, 300px);
  padding: 1.25rem 1.25rem 1.1rem;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.22), rgba(255, 255, 255, 0.08));
  border: 1px solid rgba(255, 255, 255, 0.24);
  color: white;
  animation: cardFloatPrimary 9s ease-in-out infinite;
}

.signal-kicker {
  display: inline-block;
  font-size: 0.78rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: rgba(255, 255, 255, 0.74);
}

.signal-value {
  display: block;
  margin-top: 0.7rem;
  font-size: 3.2rem;
  line-height: 1;
  font-weight: 800;
}

.signal-label {
  display: block;
  margin-top: 0.6rem;
  font-size: 0.92rem;
  line-height: 1.6;
  color: rgba(255, 255, 255, 0.84);
}

.signal-track {
  width: 100%;
  height: 0.6rem;
  margin-top: 1rem;
  overflow: hidden;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.16);
}

.signal-track-fill {
  display: block;
  width: 72%;
  height: 100%;
  border-radius: inherit;
  background: linear-gradient(90deg, #ffffff, #ffd1db);
}

.signal-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.45rem;
  margin-top: 1rem;
}

.signal-tags span {
  padding: 0.35rem 0.7rem;
  border-radius: 999px;
  font-size: 0.76rem;
  background: rgba(255, 255, 255, 0.12);
  color: rgba(255, 255, 255, 0.9);
}

.signal-secondary {
  width: 180px;
  padding: 1rem;
  background: rgba(11, 21, 48, 0.24);
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: white;
  animation: cardFloatSecondary 10s ease-in-out infinite;
}

.signal-secondary-top {
  top: 22px;
  right: 24px;
}

.signal-secondary-bottom {
  right: 56px;
  bottom: 26px;
  animation-delay: -3.2s;
}

.signal-mini-label {
  display: block;
  font-size: 0.78rem;
  color: rgba(255, 255, 255, 0.72);
}

.signal-mini-value {
  display: block;
  margin-top: 0.55rem;
  font-size: 2rem;
  line-height: 1;
  font-weight: 800;
}

.signal-mini-foot {
  display: block;
  margin-top: 0.45rem;
  font-size: 0.82rem;
  line-height: 1.55;
  color: rgba(255, 255, 255, 0.82);
}

.insight-board {
  position: relative;
  z-index: 2;
  margin: -6.25rem 1.5rem 0;
  padding: 1.5rem;
  border-radius: 1.8rem;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.92), rgba(255, 255, 255, 0.88));
  border: 1px solid rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(20px);
  box-shadow: var(--shadow-strong);
}

.insight-header,
.section-header {
  display: flex;
  justify-content: space-between;
  gap: 1.5rem;
  align-items: flex-start;
}

.header-title h2 {
  margin: 0.35rem 0 0;
  font-size: 1.7rem;
  font-weight: 800;
  color: var(--page-ink);
  letter-spacing: -0.03em;
}

.header-title p {
  margin: 0.55rem 0 0;
  max-width: 34rem;
  font-size: 0.96rem;
  line-height: 1.75;
  color: var(--page-muted);
}

.title-badge {
  display: inline-flex;
  align-items: center;
  min-height: 2rem;
  padding: 0.35rem 0.8rem;
  border-radius: 999px;
  background: linear-gradient(135deg, #eef2ff, #f7ebff);
  color: #5d67e6;
  font-size: 0.76rem;
  font-weight: 800;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.refresh-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  min-height: 3rem;
  padding: 0.75rem 1.15rem;
  border: none;
  border-radius: 1rem;
  background: linear-gradient(135deg, #edf1ff, #e9f7ff);
  color: #5066ea;
  font-size: 0.94rem;
  font-weight: 800;
  cursor: pointer;
  box-shadow: inset 0 0 0 1px rgba(92, 114, 238, 0.08);
  transition: transform 0.25s ease, box-shadow 0.25s ease;
}

.refresh-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 22px rgba(80, 102, 234, 0.14);
}

.refresh-btn:disabled {
  cursor: wait;
  opacity: 0.85;
}

.refresh-icon {
  font-size: 1.1rem;
}

.refresh-icon.spinning {
  animation: spin 1s linear infinite;
}

.insight-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 1rem;
  margin-top: 1.35rem;
}

.insight-card {
  position: relative;
  overflow: hidden;
  min-height: 210px;
  padding: 1.2rem;
  border-radius: 1.55rem;
  color: white;
  box-shadow: var(--shadow-soft);
  transition: transform 0.28s ease, box-shadow 0.28s ease;
}

.insight-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 18px 36px rgba(16, 32, 58, 0.16);
}

.insight-card-shine {
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.18), rgba(255, 255, 255, 0.03));
}

.theme-violet {
  background: linear-gradient(160deg, #798dff 0%, #7a5ce5 100%);
}

.theme-rose {
  background: linear-gradient(160deg, #f3a7f1 0%, #ef668a 100%);
}

.theme-cyan {
  background: linear-gradient(160deg, #68c4ff 0%, #27c9e8 100%);
}

.theme-green {
  background: linear-gradient(160deg, #62e79a 0%, #41dccf 100%);
}

.insight-topline,
.insight-bottom {
  position: relative;
  z-index: 1;
}

.insight-topline {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
}

.insight-icon {
  font-size: 2rem;
  line-height: 1;
}

.insight-kicker {
  font-size: 0.76rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: rgba(255, 255, 255, 0.74);
}

.insight-number {
  position: relative;
  z-index: 1;
  margin-top: 1.35rem;
  font-size: 3rem;
  line-height: 1;
  font-weight: 800;
}

.insight-label {
  position: relative;
  z-index: 1;
  margin-top: 0.8rem;
  font-size: 1.05rem;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.96);
}

.insight-bottom {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: 1rem;
  margin-top: 1.25rem;
}

.insight-trend {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.84rem;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.92);
}

.trend-arrow {
  font-size: 0.95rem;
}

.insight-ring {
  width: 60px;
  height: 60px;
}

.insight-ring svg {
  transform: rotate(-90deg);
}

.overview-lower {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(360px, 0.95fr);
  gap: 1.5rem;
}

.quick-actions-section,
.activity-section {
  position: relative;
  overflow: hidden;
  padding: 1.55rem;
  border-radius: 1.8rem;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.95), rgba(255, 255, 255, 0.9));
  border: 1px solid rgba(255, 255, 255, 0.6);
  box-shadow: var(--shadow-soft);
}

.project-progress-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: 1.4rem;
}

.project-progress-item {
  padding: 1.25rem;
  border-radius: 1.2rem;
  background: linear-gradient(180deg, #fbfcff, #f3f7ff);
  border: 1px solid rgba(96, 108, 232, 0.08);
  transition: transform 0.25s ease, box-shadow 0.25s ease;
}

.project-progress-item:hover {
  transform: translateX(4px);
  box-shadow: 0 14px 28px rgba(16, 32, 58, 0.08);
}

.project-header {
  cursor: pointer;
  user-select: none;
}

.project-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.project-name {
  font-size: 1.05rem;
  font-weight: 800;
  color: var(--page-ink);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.expand-icon {
  font-size: 0.75rem;
  color: #6175ec;
  transition: transform 0.3s ease;
  display: inline-block;
}

.expand-icon.expanded {
  transform: rotate(90deg);
}

.project-stats {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 0.85rem;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 0.35rem;
}

.stat-label {
  color: var(--page-muted);
}

.stat-value {
  font-weight: 700;
  color: var(--page-ink);
}

.stat-divider {
  color: rgba(96, 108, 232, 0.2);
}

.progress-container {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.progress-bar {
  flex: 1;
  height: 0.75rem;
  background: rgba(96, 108, 232, 0.1);
  border-radius: 999px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  border-radius: inherit;
  transition: width 0.6s ease;
}

.progress-percentage {
  min-width: 50px;
  text-align: right;
  font-size: 0.95rem;
  font-weight: 800;
  color: var(--page-ink);
}

.modules-list {
  margin-top: 1rem;
  margin-left: 1.5rem;
  padding-left: 1rem;
  border-left: 3px solid rgba(96, 108, 232, 0.15);
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.module-item {
  padding: 0.75rem 0.875rem;
  border-radius: 0.6rem;
  background: rgba(255, 255, 255, 0.4);
  border: 1px solid rgba(96, 108, 232, 0.04);
  transition: all 0.2s ease;
  position: relative;
}

.module-item::before {
  content: '';
  position: absolute;
  left: -1rem;
  top: 50%;
  width: 0.5rem;
  height: 1px;
  background: rgba(96, 108, 232, 0.15);
}

.module-item:hover {
  background: rgba(255, 255, 255, 0.7);
  border-color: rgba(96, 108, 232, 0.08);
  transform: translateX(2px);
}

.module-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.module-name {
  font-size: 0.85rem;
  font-weight: 600;
  color: rgba(16, 32, 58, 0.85);
}

.module-stats {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.75rem;
}

.module-stats .stat-label {
  color: rgba(98, 113, 141, 0.8);
}

.module-stats .stat-value {
  color: rgba(16, 32, 58, 0.75);
  font-weight: 600;
}

.module-bar {
  height: 0.5rem;
  background: rgba(96, 108, 232, 0.06);
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 1rem;
  margin-top: 1.4rem;
  text-align: center;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  opacity: 0.5;
}

.empty-text {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--page-ink);
  margin-bottom: 0.5rem;
}

.empty-hint {
  font-size: 0.9rem;
  color: var(--page-muted);
}

.view-all-link {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  color: #6175ec;
  font-size: 0.92rem;
  font-weight: 800;
  text-decoration: none;
  transition: color 0.25s ease;
}

.link-arrow {
  transition: transform 0.25s ease;
}

.view-all-link:hover .link-arrow {
  transform: translateX(4px);
}

.activity-timeline {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: 1.4rem;
}

.activity-item {
  position: relative;
  padding-left: 1.5rem;
}

.activity-line {
  position: absolute;
  top: 1.4rem;
  left: 0.35rem;
  bottom: -1rem;
  width: 2px;
  background: linear-gradient(180deg, rgba(95, 118, 238, 0.28), rgba(95, 118, 238, 0));
}

.activity-item:last-child .activity-line {
  display: none;
}

.activity-dot {
  position: absolute;
  top: 1.1rem;
  left: 0;
  width: 0.8rem;
  height: 0.8rem;
  border-radius: 50%;
  box-shadow: 0 0 0 6px rgba(98, 117, 236, 0.08);
}

.activity-dot.success {
  background: #10b981;
}

.activity-dot.warning {
  background: #f59e0b;
}

.activity-dot.info {
  background: #3b82f6;
}

.activity-card {
  padding: 1rem 1.05rem;
  border-radius: 1.2rem;
  background: linear-gradient(180deg, #fbfcff, #f3f7ff);
  border: 1px solid rgba(96, 108, 232, 0.08);
  transition: transform 0.25s ease, box-shadow 0.25s ease;
}

.activity-card:hover {
  transform: translateX(4px);
  box-shadow: 0 14px 28px rgba(16, 32, 58, 0.08);
}

.activity-card-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

.activity-badge {
  display: inline-flex;
  align-items: center;
  min-height: 2rem;
  padding: 0.25rem 0.7rem;
  border-radius: 999px;
  font-size: 0.76rem;
  font-weight: 800;
}

.activity-badge.success {
  background: #daf6ea;
  color: #0f7a57;
}

.activity-badge.warning {
  background: #fdf0c9;
  color: #9a6700;
}

.activity-badge.info {
  background: #deebff;
  color: #2159d5;
}

.activity-time {
  font-size: 0.8rem;
  color: #8b97ad;
}

.activity-title {
  margin-top: 0.9rem;
  color: var(--page-ink);
  font-size: 1rem;
  font-weight: 800;
}

.activity-desc {
  margin-top: 0.45rem;
  color: var(--page-muted);
  font-size: 0.9rem;
  line-height: 1.7;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }

  to {
    transform: rotate(360deg);
  }
}

@keyframes auroraDrift {
  0%,
  100% {
    transform: translate3d(0, 0, 0) scale(1);
    opacity: 0.68;
  }

  50% {
    transform: translate3d(12px, -10px, 0) scale(1.08);
    opacity: 0.92;
  }
}

@keyframes coreFloat {
  0%,
  100% {
    transform: translate3d(0, 0, 0) scale(1);
  }

  50% {
    transform: translate3d(8px, -12px, 0) scale(1.04);
  }
}

@keyframes haloSpin {
  from {
    transform: rotate(0deg);
  }

  to {
    transform: rotate(360deg);
  }
}

@keyframes orbitalFloat {
  0%,
  100% {
    transform: translate3d(0, 0, 0) scale(1);
  }

  25% {
    transform: translate3d(10px, -8px, 0) scale(1.02);
  }

  50% {
    transform: translate3d(-8px, 10px, 0) scale(0.985);
  }

  75% {
    transform: translate3d(6px, 6px, 0) scale(1.015);
  }
}

@keyframes orbitDotSpin {
  from {
    transform: rotate(0deg);
  }

  to {
    transform: rotate(360deg);
  }
}

@keyframes sparkPulse {
  0%,
  100% {
    transform: scale(0.85);
    opacity: 0.46;
  }

  50% {
    transform: scale(1.35);
    opacity: 1;
  }
}

@keyframes cardFloatPrimary {
  0%,
  100% {
    transform: translate3d(0, 0, 0);
  }

  50% {
    transform: translate3d(0, -10px, 0);
  }
}

@keyframes cardFloatSecondary {
  0%,
  100% {
    transform: translate3d(0, 0, 0);
  }

  50% {
    transform: translate3d(0, -7px, 0);
  }
}

@media (prefers-reduced-motion: reduce) {
  .visual-aurora,
  .visual-core,
  .visual-core-ring,
  .visual-spark,
  .visual-orbit,
  .orbit-dot,
  .signal-card,
  .refresh-icon.spinning {
    animation: none !important;
  }
}

@media (max-width: 1220px) {
  .hero-grid,
  .overview-lower {
    grid-template-columns: 1fr;
  }

  .hero-panel {
    padding-bottom: 9.5rem;
  }

  .hero-visual {
    min-height: 280px;
  }

  .visual-core {
    right: 88px;
  }

  .visual-core-ring {
    right: 58px;
  }

  .signal-primary {
    left: 0;
  }

  .insight-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 768px) {
  .hero-panel {
    padding: 1.25rem 1.25rem 1.5rem;
    border-radius: 1.6rem;
  }

  .hero-grid {
    gap: 1.5rem;
  }

  .hero-title-main {
    font-size: 2.85rem;
  }

  .hero-highlights,
  .insight-grid,
  .actions-grid,
  .overview-lower {
    grid-template-columns: 1fr;
  }

  .hero-visual {
    min-height: 260px;
  }

  .aurora-one {
    width: 170px;
    height: 170px;
    right: 24px;
  }

  .aurora-two {
    width: 128px;
    height: 128px;
    right: 88px;
    bottom: 42px;
  }

  .visual-core {
    width: 88px;
    height: 88px;
    right: 90px;
    top: 92px;
  }

  .visual-core-ring {
    width: 136px;
    height: 136px;
    right: 66px;
    top: 68px;
  }

  .orbit-large {
    width: 200px;
    height: 200px;
    right: 12px;
    top: 24px;
  }

  .orbit-medium {
    width: 120px;
    height: 120px;
    right: 114px;
    bottom: 24px;
  }

  .orbit-small {
    width: 74px;
    height: 74px;
    right: 10px;
    bottom: 48px;
  }

  .spark-one {
    right: 74px;
    top: 58px;
  }

  .spark-two {
    right: 26px;
    top: 138px;
  }

  .spark-three {
    right: 168px;
    bottom: 54px;
  }

  .signal-primary,
  .signal-secondary,
  .signal-secondary-top,
  .signal-secondary-bottom {
    position: absolute;
  }

  .signal-primary {
    width: calc(100% - 1.5rem);
    left: 0;
    top: 12px;
  }

  .signal-secondary-top {
    top: auto;
    right: auto;
    left: 0;
    bottom: 0;
    width: 46%;
  }

  .signal-secondary-bottom {
    right: 0;
    bottom: 0;
    width: 46%;
  }

  .insight-board,
  .quick-actions-section,
  .activity-section {
    margin: 1rem 0 0;
    padding: 1.2rem;
    border-radius: 1.45rem;
  }

  .insight-header,
  .section-header,
  .activity-card-head {
    flex-direction: column;
    align-items: flex-start;
  }

  .action-content {
    min-height: 140px;
  }
}
</style>
