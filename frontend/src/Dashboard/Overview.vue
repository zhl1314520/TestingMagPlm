<template>
  <div class="overview">
    <section class="hero-stage">
      <div class="hero-panel">
        <div class="hero-grid">
          <div class="hero-copy">
            <div class="hero-meta">
              <span class="hero-pill">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="3" y="3" width="7" height="7"/>
                  <rect x="14" y="3" width="7" height="7"/>
                  <rect x="14" y="14" width="7" height="7"/>
                  <rect x="3" y="14" width="7" height="7"/>
                </svg>
                Overview Console
              </span>
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
              <div class="hero-highlight hero-highlight-ember">
                <div class="highlight-icon">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>
                  </svg>
                </div>
                <span class="hero-highlight-label">项目轨道</span>
                <strong class="hero-highlight-value">{{ metrics.total_projects }} 个活跃项目</strong>
              </div>
              
              <div class="hero-highlight hero-highlight-teal">
                <div class="highlight-icon">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                    <polyline points="14 2 14 8 20 8"/>
                    <line x1="16" y1="13" x2="8" y2="13"/>
                    <line x1="16" y1="17" x2="8" y2="17"/>
                  </svg>
                </div>
                <span class="hero-highlight-label">用例储备</span>
                <strong class="hero-highlight-value">{{ metrics.total_testcases }} 条测试资产</strong>
              </div>
              
              <div class="hero-highlight hero-highlight-coral">
                <div class="highlight-icon">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polygon points="5 3 19 12 5 21 5 3"/>
                  </svg>
                </div>
                <span class="hero-highlight-label">执行动能</span>
                <strong class="hero-highlight-value">{{ metrics.total_executions }} 次运行记录</strong>
              </div>
            </div>
          </div>

          <div class="hero-visual" aria-hidden="true">
            <div class="visual-blob blob-one"></div>
            <div class="visual-blob blob-two"></div>
            <div class="visual-blob blob-three"></div>
            
            <div class="visual-grid-pattern"></div>
            
            <div class="visual-core-ring"></div>
            <div class="visual-core"></div>

            <article class="signal-card signal-primary">
              <span class="signal-kicker">Quality Pulse</span>
              <strong class="signal-value">{{ totalAssets }}</strong>
              <span class="signal-label">当前平台沉淀的质量资产</span>

              <div class="signal-track">
                <span class="signal-track-fill" :style="{ width: assetProgress + '%' }"></span>
              </div>

              <div class="signal-tags">
                <span>项目</span>
                <span>用例</span>
                <span>执行</span>
                <span>缺陷</span>
              </div>
            </article>

            <article class="signal-card signal-secondary signal-secondary-top">
              <div class="signal-mini-icon">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <polygon points="5 3 19 12 5 21 5 3"/>
                </svg>
              </div>
              <span class="signal-mini-label">自动化节奏</span>
              <strong class="signal-mini-value">{{ metrics.total_executions }}</strong>
              <span class="signal-mini-foot">本视图聚焦执行动能</span>
            </article>

            <article class="signal-card signal-secondary signal-secondary-bottom">
              <div class="signal-mini-icon signal-mini-icon-coral">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="12" r="10"/>
                  <line x1="12" y1="8" x2="12" y2="12"/>
                  <line x1="12" y1="16" x2="12.01" y2="16"/>
                </svg>
              </div>
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
            <span class="title-badge title-badge-ember">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
              </svg>
              Data Insights
            </span>
            <h2>数据洞察</h2>
            <p>首屏直接看到核心指标，不需要再往下找重点。</p>
          </div>

          <button class="refresh-btn" :class="{ spinning: loading }" @click="loadInsightMetrics">
            <svg class="refresh-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="23 4 23 10 17 10"/>
              <polyline points="1 20 1 14 7 14"/>
              <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/>
            </svg>
            <span>刷新</span>
          </button>
        </div>

        <div class="insight-grid" :class="{ 'stagger-animation': showInsightAnimation }">
          <article
            v-for="card in insightCards"
            :key="card.key"
            class="insight-card"
            :class="card.theme"
            @click="createRipple($event); navigateToPanel(card.route)"
          >
            <div class="insight-card-shine"></div>

            <div class="insight-topline">
              <div class="insight-icon" v-html="card.icon"></div>
              <span class="insight-kicker">{{ card.kicker }}</span>
            </div>

            <div class="insight-number">{{ card.value }}</div>
            <div class="insight-label">{{ card.label }}</div>

            <div class="insight-bottom">
              <div class="insight-trend" :class="card.trendClass">
                <span class="trend-arrow" v-html="card.trendIcon"></span>
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

    <section class="overview-lower asymmetric-grid">
      <div class="quick-actions-section">
        <div class="section-header">
          <div class="header-title">
            <span class="title-badge title-badge-teal">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>
              </svg>
              Project Progress
            </span>
            <h2>项目进展</h2>
            <p>实时追踪你参与的项目进度，掌握测试用例完成情况。</p>
          </div>
        </div>

        <div class="project-progress-list" v-if="projectProgress.length > 0">
          <div
            v-for="(project, index) in paginatedProjects"
            :key="project.project_id"
            class="project-progress-item"
          >
            <div class="project-header" @click="toggleProject(project.project_id)">
              <div class="project-info">
                <div class="project-name">
                  <span class="expand-icon" :class="{ expanded: expandedProjects.includes(project.project_id) }">
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                      <polyline points="9 18 15 12 9 6"/>
                    </svg>
                  </span>
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
                      background: getProjectGradient(index)
                    }"
                  ></div>
                </div>
                <div class="progress-percentage">{{ project.progress_percentage }}%</div>
              </div>
            </div>
            
            <Transition name="expand">
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
                          background: getProjectGradient(index)
                        }"
                      ></div>
                    </div>
                    <div class="progress-percentage">{{ module.progress_percentage }}%</div>
                  </div>
                </div>
              </div>
            </Transition>
          </div>
        </div>

        <div class="empty-state" v-else>
          <div class="empty-icon">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="20" x2="18" y2="10"/>
              <line x1="12" y1="20" x2="12" y2="4"/>
              <line x1="6" y1="20" x2="6" y2="14"/>
            </svg>
          </div>
          <div class="empty-text">暂无项目数据</div>
          <div class="empty-hint">你还没有参与任何项目，请联系管理员添加</div>
        </div>
      </div>

      <div class="activity-section">
        <div class="section-header">
          <div class="header-title">
            <span class="title-badge title-badge-coral">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
              </svg>
              Recent Activities
            </span>
            <h2>最近活动</h2>
            <p>把最近发生的关键动作串成一条时间线，方便你快速感知当前节奏。</p>
          </div>

          <router-link to="/dashboard/reports" class="view-all-link">
            查看全部
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="5" y1="12" x2="19" y2="12"/>
              <polyline points="12 5 19 12 12 19"/>
            </svg>
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
import { computed, onMounted, ref, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { metricsAPI } from '../api/index.js'

const router = useRouter()

const metrics = ref({
  total_projects: 0,
  total_testcases: 0,
  total_bugs: 0,
  total_executions: 0
})

const insightMetrics = ref({
  total_projects: 0,
  total_testcases: 0,
  total_bugs: 0,
  total_executions: 0,
  projects_growth: 0,
  projects_growth_positive: true,
  testcases_growth: 0,
  testcases_growth_positive: true,
  bugs_growth: 0,
  bugs_growth_positive: true,
  executions_growth: 0,
  executions_growth_positive: true
})

const userInfo = ref(null)
const loading = ref(false)
const showInsightAnimation = ref(true)
const projectProgress = ref([])
const expandedProjects = ref([])
const projectCurrentPage = ref(1)
const projectPageSize = ref(12)

const projectGradients = [
  'linear-gradient(90deg, var(--ember-core), var(--ember-soft))',
  'linear-gradient(90deg, var(--teal-primary), var(--teal-bright))',
  'linear-gradient(90deg, var(--coral-primary), var(--coral-bright))',
  'linear-gradient(90deg, var(--forest-primary), var(--forest-bright))',
  'linear-gradient(90deg, var(--amber-primary), var(--amber-soft))',
  'linear-gradient(90deg, var(--ember-glow), var(--amber-soft))',
  'linear-gradient(90deg, var(--teal-deep), var(--teal-soft))',
  'linear-gradient(90deg, var(--coral-deep), var(--coral-soft))'
]

const getProjectGradient = (index) => {
  return projectGradients[index % projectGradients.length]
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
    return '早上好 ！'
  }

  if (hour < 18) {
    return '下午好 ！'
  }

  return '晚上好 ！'
})

const totalAssets = computed(() => {
  return (
    metrics.value.total_projects +
    metrics.value.total_testcases +
    metrics.value.total_bugs +
    metrics.value.total_executions
  )
})

const assetProgress = computed(() => {
  const progress = (totalAssets.value / 100) * 100
  return Math.min(progress, 100)
})

const insightCards = computed(() => {
  const formatTrend = (growth, isPositive) => {
    const value = growth ?? 0
    const label = isPositive ? '增长' : '减少'
    return `${label} ${value}%`
  }
  
  const getGrowth = (key) => insightMetrics.value[`${key}_growth`] ?? 0
  const isGrowthPositive = (key) => insightMetrics.value[`${key}_growth_positive`] ?? true
  
  return [
    {
      key: 'projects',
      theme: 'theme-teal',
      icon: '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg>',
      kicker: 'Project Scope',
      label: '项目总数',
      value: insightMetrics.value.total_projects,
      trend: formatTrend(getGrowth('projects'), isGrowthPositive('projects')),
      trendClass: isGrowthPositive('projects') ? 'positive' : 'negative',
      trendIcon: isGrowthPositive('projects') ? '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="19" x2="12" y2="5"/><polyline points="5 12 12 5 19 12"/></svg>' : '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><polyline points="19 12 12 19 5 12"/></svg>',
      progress: Math.min(insightMetrics.value.total_projects, 100),
      route: '/dashboard/projects'
    },
    {
      key: 'testcases',
      theme: 'theme-teal',
      icon: '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>',
      kicker: 'Coverage Base',
      label: '测试用例',
      value: insightMetrics.value.total_testcases,
      trend: formatTrend(getGrowth('testcases'), isGrowthPositive('testcases')),
      trendClass: isGrowthPositive('testcases') ? 'positive' : 'negative',
      trendIcon: isGrowthPositive('testcases') ? '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="19" x2="12" y2="5"/><polyline points="5 12 12 5 19 12"/></svg>' : '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><polyline points="19 12 12 19 5 12"/></svg>',
      progress: Math.min(insightMetrics.value.total_testcases, 100),
      route: '/dashboard/testcases'
    },
    {
      key: 'bugs',
      theme: 'theme-teal',
      icon: '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>',
      kicker: 'Risk Signals',
      label: '缺陷数量',
      value: insightMetrics.value.total_bugs,
      trend: formatTrend(getGrowth('bugs'), !isGrowthPositive('bugs')),
      trendClass: isGrowthPositive('bugs') ? 'negative' : 'positive',
      trendIcon: isGrowthPositive('bugs') ? '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><polyline points="19 12 12 19 5 12"/></svg>' : '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="19" x2="12" y2="5"/><polyline points="5 12 12 5 19 12"/></svg>',
      progress: Math.min(insightMetrics.value.total_bugs, 100),
      route: '/dashboard/bugs'
    },
    {
      key: 'executions',
      theme: 'theme-teal',
      icon: '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="5 3 19 12 5 21 5 3"/></svg>',
      kicker: 'Automation Pace',
      label: '执行次数',
      value: insightMetrics.value.total_executions,
      trend: formatTrend(getGrowth('executions'), isGrowthPositive('executions')),
      trendClass: isGrowthPositive('executions') ? 'positive' : 'negative',
      trendIcon: isGrowthPositive('executions') ? '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="19" x2="12" y2="5"/><polyline points="5 12 12 5 19 12"/></svg>' : '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><polyline points="19 12 12 19 5 12"/></svg>',
      progress: Math.min(insightMetrics.value.total_executions, 100),
      route: '/dashboard/executions'
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

const navigateToPanel = (route) => {
  if (route) {
    router.push(route)
  }
}

const createRipple = (event) => {
  const card = event.currentTarget
  
  const circle = document.createElement("span")
  const diameter = Math.max(card.clientWidth, card.clientHeight)
  const radius = diameter / 2
  
  circle.style.width = circle.style.height = `${diameter}px`
  circle.style.left = `${event.clientX - card.getBoundingClientRect().left - radius}px`
  circle.style.top = `${event.clientY - card.getBoundingClientRect().top - radius}px`
  circle.classList.add("ripple")
  
  const ripple = card.getElementsByClassName("ripple")[0]
  if (ripple) {
    ripple.remove()
  }
  
  card.appendChild(circle)
}

const totalProjectPages = computed(() => {
  return Math.ceil(projectProgress.value.length / projectPageSize.value)
})

const visiblePages = computed(() => {
  const total = totalProjectPages.value
  const pages = []
  for (let i = 1; i <= Math.min(3, total); i++) {
    pages.push(i)
  }
  return pages
})

const paginatedProjects = computed(() => {
  const start = (projectCurrentPage.value - 1) * projectPageSize.value
  const end = start + projectPageSize.value
  return projectProgress.value.slice(start, end)
})

const goToProjectPage = (page) => {
  if (page >= 1 && page <= totalProjectPages.value) {
    projectCurrentPage.value = page
  }
}

const recentActivities = ref([])

onMounted(async () => {
  const storedUserInfo = localStorage.getItem('user_info')
  if (storedUserInfo) {
    userInfo.value = JSON.parse(storedUserInfo)
  }

  await Promise.all([
    loadMetrics(),
    loadInsightMetrics(),
    loadProjectProgress(),
    loadRecentActivities()
  ])
})

const loadMetrics = async () => {
  try {
    const response = await metricsAPI.getOverview()
    metrics.value = {
      total_projects: response.data.total_projects,
      total_testcases: response.data.total_testcases,
      total_bugs: response.data.total_bugs,
      total_executions: response.data.total_executions
    }
  } catch (error) {
    console.error('获取概览数据失败:', error)
  }
}

const loadInsightMetrics = async () => {
  showInsightAnimation.value = false
  loading.value = true
  try {
    const response = await metricsAPI.getOverview({ _t: Date.now() })
    insightMetrics.value = response.data
  } catch (error) {
    console.error('获取数据洞察失败:', error)
  } finally {
    loading.value = false
    await nextTick()
    showInsightAnimation.value = true
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

const loadRecentActivities = async () => {
  try {
    const response = await metricsAPI.getRecentActivities(10)
    recentActivities.value = response.data.activities || []
  } catch (error) {
    console.error('获取最近活动失败:', error)
  }
}
</script>

<style scoped>
.overview {
  --page-ink: var(--ink-primary);
  --page-muted: var(--ink-soft);
  --page-soft: var(--paper-muted);
  padding: 0;
  will-change: scroll-position;
  -webkit-overflow-scrolling: touch;
}

.hero-stage {
  position: relative;
  margin-bottom: var(--space-2xl);
}

.hero-panel {
  position: relative;
  overflow: hidden;
  border-radius: var(--radius-xl);
  padding: var(--space-2xl) var(--space-2xl) 10rem;
  background: 
    radial-gradient(ellipse at 15% 20%, rgba(232, 93, 4, 0.12), transparent 45%),
    radial-gradient(ellipse at 85% 30%, rgba(20, 184, 166, 0.1), transparent 40%),
    radial-gradient(ellipse at 70% 85%, rgba(244, 63, 94, 0.08), transparent 35%),
    linear-gradient(145deg, #1a1f2e 0%, #0f1419 50%, #141b2d 100%);
  box-shadow: var(--shadow-xl);
  will-change: auto;
  contain: layout style;
}

.hero-grid {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: 1.15fr 0.85fr;
  gap: var(--space-2xl);
  align-items: center;
}

.hero-copy {
  color: white;
}

.hero-meta {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-sm);
  align-items: center;
  margin-bottom: var(--space-lg);
}

.hero-pill,
.hero-date {
  display: inline-flex;
  align-items: center;
  gap: var(--space-xs);
  min-height: 2.25rem;
  padding: 0.45rem 0.9rem;
  border-radius: var(--radius-full);
  font-size: 0.8rem;
  font-weight: 700;
  letter-spacing: 0.04em;
}

.hero-pill {
  color: #fff;
  background: linear-gradient(135deg, rgba(232, 93, 4, 0.25), rgba(250, 163, 7, 0.15));
  border: 1px solid rgba(232, 93, 4, 0.3);
}

.hero-date {
  color: rgba(255, 255, 255, 0.85);
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.hero-title {
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.hero-title-small {
  font-size: 1.25rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.75);
}

.hero-title-main {
  font-size: clamp(2.8rem, 5vw, 4.5rem);
  line-height: 0.95;
  letter-spacing: -0.05em;
  font-weight: 800;
  color: #fff;
  background: linear-gradient(135deg, #fff 0%, rgba(255, 255, 255, 0.85) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-subtitle {
  max-width: 36rem;
  margin: var(--space-lg) 0 0;
  font-size: 1rem;
  line-height: 1.8;
  color: rgba(255, 255, 255, 0.7);
}

.hero-highlights {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: var(--space-sm);
  margin-top: var(--space-xl);
}

.hero-highlight {
  padding: var(--space-md);
  border-radius: var(--radius-lg);
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  transition: all 0.25s var(--ease-smooth);
  will-change: transform;
  transform: translateZ(0);
  backface-visibility: hidden;
}

.hero-highlight:hover {
  background: rgba(255, 255, 255, 0.08);
  transform: translateY(-2px);
}

.highlight-icon {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: var(--space-sm);
}

.hero-highlight-ember .highlight-icon {
  background: linear-gradient(135deg, rgba(232, 93, 4, 0.2), rgba(250, 163, 7, 0.15));
  color: var(--ember-soft);
}

.hero-highlight-teal .highlight-icon {
  background: linear-gradient(135deg, rgba(20, 184, 166, 0.2), rgba(94, 234, 212, 0.15));
  color: var(--teal-soft);
}

.hero-highlight-coral .highlight-icon {
  background: linear-gradient(135deg, rgba(244, 63, 94, 0.2), rgba(253, 164, 175, 0.15));
  color: var(--coral-soft);
}

.hero-highlight-label {
  display: block;
  font-size: 0.72rem;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: rgba(255, 255, 255, 0.5);
  margin-bottom: 4px;
}

.hero-highlight-value {
  display: block;
  font-size: 0.9rem;
  line-height: 1.4;
  color: white;
  font-weight: 600;
}

.hero-visual {
  position: relative;
  min-height: 340px;
  isolation: isolate;
  contain: layout style;
  transform: translateZ(0);
  backface-visibility: hidden;
}

.visual-blob {
  position: absolute;
  border-radius: 50%;
  z-index: 0;
  transition: transform 0.6s var(--ease-smooth);
  will-change: transform;
  transform: translateZ(0);
  backface-visibility: hidden;
}

.blob-one {
  width: 200px;
  height: 200px;
  right: 40px;
  top: 20px;
  background: 
    radial-gradient(circle at 50% 50%, rgba(232, 93, 4, 0.35) 0%, rgba(232, 93, 4, 0.2) 30%, rgba(232, 93, 4, 0.08) 50%, transparent 70%);
}

.blob-two {
  width: 150px;
  height: 150px;
  right: 120px;
  bottom: 40px;
  background: 
    radial-gradient(circle at 50% 50%, rgba(20, 184, 166, 0.32) 0%, rgba(20, 184, 166, 0.18) 30%, rgba(20, 184, 166, 0.06) 50%, transparent 70%);
}

.blob-three {
  width: 100px;
  height: 100px;
  right: 200px;
  top: 80px;
  background: 
    radial-gradient(circle at 50% 50%, rgba(244, 63, 94, 0.28) 0%, rgba(244, 63, 94, 0.15) 30%, rgba(244, 63, 94, 0.05) 50%, transparent 70%);
}

.hero-visual:hover .blob-one {
  transform: translate(10px, -10px);
}

.hero-visual:hover .blob-two {
  transform: translate(-8px, 8px);
}

.hero-visual:hover .blob-three {
  transform: translate(6px, -6px);
}

.visual-grid-pattern {
  position: absolute;
  inset: 0;
  background-image: 
    linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
  background-size: 40px 40px;
  opacity: 0.5;
}

.visual-core {
  position: absolute;
  width: 100px;
  height: 100px;
  right: 120px;
  top: 100px;
  border-radius: 50%;
  z-index: 1;
  background:
    radial-gradient(circle at 35% 35%, rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0.2) 40%, rgba(255, 255, 255, 0.05) 70%),
    linear-gradient(145deg, rgba(232, 93, 4, 0.5), rgba(20, 184, 166, 0.3));
  box-shadow:
    0 0 0 1px rgba(255, 255, 255, 0.15),
    0 20px 40px rgba(0, 0, 0, 0.3),
    0 0 60px rgba(232, 93, 4, 0.2);
  transition: transform 0.5s var(--ease-bounce), box-shadow 0.5s var(--ease-smooth);
  will-change: transform, box-shadow;
  transform: translateZ(0);
  backface-visibility: hidden;
}

.hero-visual:hover .visual-core {
  transform: scale(1.05);
  box-shadow:
    0 0 0 1px rgba(255, 255, 255, 0.2),
    0 25px 50px rgba(0, 0, 0, 0.35),
    0 0 80px rgba(232, 93, 4, 0.3);
}

.visual-core-ring {
  position: absolute;
  width: 160px;
  height: 160px;
  right: 90px;
  top: 70px;
  border-radius: 50%;
  z-index: 1;
  border: 1px solid rgba(255, 255, 255, 0.12);
  box-shadow:
    inset 0 0 0 12px rgba(255, 255, 255, 0.02),
    0 0 30px rgba(255, 255, 255, 0.05);
  transition: transform 0.6s var(--ease-smooth);
  will-change: transform;
  transform: translateZ(0);
  backface-visibility: hidden;
}

.hero-visual:hover .visual-core-ring {
  transform: rotate(15deg);
}

.signal-card {
  position: absolute;
  border-radius: var(--radius-lg);
  background: rgba(20, 27, 45, 0.92);
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.25);
  z-index: 3;
  border: 1px solid rgba(255, 255, 255, 0.08);
  will-change: auto;
  transform: translateZ(0);
  backface-visibility: hidden;
}

.signal-primary {
  left: 0;
  top: 50px;
  width: min(100%, 280px);
  padding: var(--space-lg);
  color: white;
}

.signal-kicker {
  display: inline-block;
  font-size: 0.72rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: rgba(255, 255, 255, 0.6);
}

.signal-value {
  display: block;
  margin-top: var(--space-sm);
  font-size: 3rem;
  line-height: 1;
  font-weight: 800;
  background: linear-gradient(135deg, #fff, rgba(255, 255, 255, 0.85));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.signal-label {
  display: block;
  margin-top: var(--space-sm);
  font-size: 0.88rem;
  line-height: 1.5;
  color: rgba(255, 255, 255, 0.75);
}

.signal-track {
  width: 100%;
  height: 5px;
  margin-top: var(--space-md);
  overflow: hidden;
  border-radius: var(--radius-full);
  background: rgba(255, 255, 255, 0.1);
}

.signal-track-fill {
  display: block;
  height: 100%;
  border-radius: inherit;
  background: linear-gradient(90deg, var(--ember-core), var(--ember-soft));
  transition: width 0.4s var(--ease-smooth);
  will-change: width;
  transform: translateZ(0);
  backface-visibility: hidden;
}

.signal-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-top: var(--space-md);
}

.signal-tags span {
  padding: 4px 10px;
  border-radius: var(--radius-full);
  font-size: 0.7rem;
  background: rgba(255, 255, 255, 0.08);
  color: rgba(255, 255, 255, 0.8);
}

.signal-secondary {
  width: 170px;
  padding: var(--space-md);
  color: white;
}

.signal-secondary-top {
  top: 20px;
  right: 20px;
}

.signal-secondary-bottom {
  right: 50px;
  bottom: 30px;
}

.signal-mini-icon {
  width: 28px;
  height: 28px;
  border-radius: var(--radius-sm);
  background: linear-gradient(135deg, rgba(20, 184, 166, 0.2), rgba(94, 234, 212, 0.15));
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--teal-soft);
  margin-bottom: var(--space-sm);
}

.signal-mini-icon-coral {
  background: linear-gradient(135deg, rgba(244, 63, 94, 0.2), rgba(253, 164, 175, 0.15));
  color: var(--coral-soft);
}

.signal-mini-label {
  display: block;
  font-size: 0.72rem;
  color: rgba(255, 255, 255, 0.6);
}

.signal-mini-value {
  display: block;
  margin-top: 6px;
  font-size: 1.8rem;
  line-height: 1;
  font-weight: 800;
}

.signal-mini-foot {
  display: block;
  margin-top: 6px;
  font-size: 0.78rem;
  line-height: 1.5;
  color: rgba(255, 255, 255, 0.7);
}

.insight-board {
  position: relative;
  z-index: 2;
  margin: -7rem var(--space-xl) 0;
  padding: var(--space-xl);
  border-radius: var(--radius-xl);
  background: rgba(255, 255, 255, 0.85);
  border: 1px solid rgba(232, 93, 4, 0.08);
  box-shadow: var(--shadow-xl);
  will-change: auto;
  contain: layout style;
}

.insight-header,
.section-header {
  display: flex;
  justify-content: space-between;
  gap: var(--space-lg);
  align-items: flex-start;
}

.header-title h2 {
  margin: 8px 0 0;
  font-size: 1.6rem;
  font-weight: 800;
  color: var(--page-ink);
  letter-spacing: -0.02em;
}

.header-title p {
  margin: var(--space-sm) 0 0;
  max-width: 32rem;
  font-size: 0.92rem;
  line-height: 1.7;
  color: var(--page-muted);
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
}

.title-badge-ember {
  background: linear-gradient(135deg, rgba(232, 93, 4, 0.08), rgba(250, 163, 7, 0.06));
  color: var(--ember-core);
}

.title-badge-teal {
  background: linear-gradient(135deg, rgba(20, 184, 166, 0.08), rgba(94, 234, 212, 0.06));
  color: var(--teal-primary);
}

.title-badge-coral {
  background: linear-gradient(135deg, rgba(244, 63, 94, 0.08), rgba(253, 164, 175, 0.06));
  color: var(--coral-primary);
}

.refresh-btn {
  display: inline-flex;
  align-items: center;
  gap: var(--space-sm);
  min-height: 2.75rem;
  padding: var(--space-sm) var(--space-md);
  border: none;
  border-radius: var(--radius-md);
  background: linear-gradient(135deg, rgba(232, 93, 4, 0.06), rgba(250, 163, 7, 0.04));
  color: var(--ember-core);
  font-size: 0.9rem;
  font-weight: 700;
  cursor: pointer;
  border: 1px solid rgba(232, 93, 4, 0.1);
  transition: all 0.25s var(--ease-smooth);
  will-change: transform;
  transform: translateZ(0);
  backface-visibility: hidden;
}

.refresh-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
  background: linear-gradient(135deg, rgba(232, 93, 4, 0.1), rgba(250, 163, 7, 0.08));
}

.refresh-btn.spinning {
  cursor: wait;
  opacity: 0.7;
}

.refresh-btn.spinning .refresh-icon {
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.insight-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: var(--space-md);
  margin-top: var(--space-lg);
  perspective: 1000px;
}

.insight-card {
  position: relative;
  overflow: hidden;
  min-height: 200px;
  padding: var(--space-lg);
  border-radius: var(--radius-lg);
  color: white;
  box-shadow: 
    0 10px 20px rgba(0,0,0,0.15),
    0 6px 6px rgba(0,0,0,0.1),
    inset 0 1px 0 rgba(255,255,255,0.2),
    inset 0 -1px 0 rgba(0,0,0,0.1);
  cursor: pointer;
  transition: all 0.2s ease;
  contain: layout style;
  will-change: transform;
  transform: translateZ(0);
  backface-visibility: hidden;
  transform-style: preserve-3d;
}

.insight-card:hover {
  transform: translateY(-2px);
  box-shadow: 
    0 15px 30px rgba(0,0,0,0.2),
    0 10px 10px rgba(0,0,0,0.15),
    inset 0 1px 0 rgba(255,255,255,0.25),
    inset 0 -1px 0 rgba(0,0,0,0.1);
}

.insight-card:active {
  transform: translateY(2px) rotateX(15deg);
  box-shadow: 
    0 2px 5px rgba(0,0,0,0.1),
    inset 0 2px 10px rgba(0,0,0,0.25),
    inset 0 0 10px rgba(0,0,0,0.15);
  transition: all 0.1s ease;
}

.ripple {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
  transform: scale(0);
  animation: ripple 0.6s linear;
  pointer-events: none;
}

@keyframes ripple {
  to {
    transform: scale(4);
    opacity: 0;
  }
}

.insight-card-shine {
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.15), rgba(255, 255, 255, 0.02));
  pointer-events: none;
}

.theme-ember {
  background: linear-gradient(145deg, var(--ember-core) 0%, var(--ember-glow) 100%);
}

.theme-teal {
  background: linear-gradient(145deg, var(--teal-deep) 0%, var(--teal-bright) 100%);
}

.theme-coral {
  background: linear-gradient(145deg, var(--coral-deep) 0%, var(--coral-bright) 100%);
}

.theme-forest {
  background: linear-gradient(145deg, var(--forest-deep) 0%, var(--forest-bright) 100%);
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
  gap: var(--space-sm);
}

.insight-icon {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.15);
  border-radius: var(--radius-md);
}

.insight-kicker {
  font-size: 0.7rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: rgba(255, 255, 255, 0.7);
}

.insight-number {
  position: relative;
  z-index: 1;
  margin-top: var(--space-lg);
  font-size: 2.8rem;
  line-height: 1;
  font-weight: 800;
}

.insight-label {
  position: relative;
  z-index: 1;
  margin-top: var(--space-sm);
  font-size: 1rem;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.95);
}

.insight-bottom {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: var(--space-md);
  margin-top: var(--space-lg);
}

.insight-trend {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 0.82rem;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.9);
}

.trend-arrow {
  display: flex;
  align-items: center;
}

.insight-ring {
  width: 56px;
  height: 56px;
}

.insight-ring svg {
  transform: rotate(-90deg);
}

.overview-lower {
  margin-top: var(--space-xl);
  align-items: stretch;
}

.quick-actions-section,
.activity-section {
  position: relative;
  overflow: hidden;
  padding: var(--space-xl);
  border-radius: var(--radius-xl);
  background: rgba(255, 255, 255, 0.85);
  border: 1px solid rgba(232, 93, 4, 0.08);
  box-shadow: var(--shadow-md);
  display: flex;
  flex-direction: column;
  will-change: auto;
  contain: layout style;
}

.quick-actions-section {
  display: flex;
  flex-direction: column;
  min-height: 600px;
}

.project-progress-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
  margin-top: var(--space-lg);
  flex: 1;
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
  scroll-behavior: smooth;
  padding-right: var(--space-sm);
}

.project-progress-list::-webkit-scrollbar {
  width: 6px;
}

.project-progress-list::-webkit-scrollbar-track {
  background: rgba(232, 93, 4, 0.05);
  border-radius: var(--radius-full);
}

.project-progress-list::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, var(--ember-core), var(--ember-soft));
  border-radius: var(--radius-full);
  transition: background 0.3s ease;
}

.project-progress-list::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(180deg, var(--ember-glow), var(--ember-core));
}

.project-progress-item {
  padding: var(--space-md);
  border-radius: var(--radius-md);
  background: linear-gradient(180deg, rgba(232, 93, 4, 0.02), rgba(250, 163, 7, 0.01));
  border: 1px solid rgba(232, 93, 4, 0.06);
  transition: all 0.25s var(--ease-smooth);
  will-change: transform;
  transform: translateZ(0);
  backface-visibility: hidden;
}

.project-progress-item:hover {
  transform: translateX(4px);
  box-shadow: var(--shadow-sm);
  border-color: rgba(232, 93, 4, 0.12);
}

.project-header {
  cursor: pointer;
  user-select: none;
}

.project-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-sm);
}

.project-name {
  font-size: 1rem;
  font-weight: 700;
  color: var(--page-ink);
  display: flex;
  align-items: center;
  gap: var(--space-sm);
}

.expand-icon {
  display: flex;
  align-items: center;
  color: var(--ember-core);
  transition: transform 0.25s var(--ease-smooth);
}

.expand-icon.expanded {
  transform: rotate(90deg);
}

.project-stats {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  font-size: 0.82rem;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 4px;
}

.stat-label {
  color: var(--page-muted);
}

.stat-value {
  font-weight: 700;
  color: var(--page-ink);
}

.stat-divider {
  color: rgba(232, 93, 4, 0.2);
}

.progress-container {
  display: flex;
  align-items: center;
  gap: var(--space-md);
}

.progress-bar {
  flex: 1;
  height: 6px;
  background: rgba(232, 93, 4, 0.08);
  border-radius: var(--radius-full);
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  border-radius: inherit;
  transition: width 0.4s var(--ease-smooth);
  will-change: width;
  transform: translateZ(0);
  backface-visibility: hidden;
}

.progress-percentage {
  min-width: 45px;
  text-align: right;
  font-size: 0.9rem;
  font-weight: 700;
  color: var(--page-ink);
}

.modules-list {
  margin-top: var(--space-md);
  margin-left: var(--space-lg);
  padding-left: var(--space-md);
  border-left: 2px solid rgba(232, 93, 4, 0.12);
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
}

.module-item {
  padding: var(--space-sm) var(--space-md);
  border-radius: var(--radius-sm);
  background: rgba(255, 255, 255, 0.5);
  border: 1px solid rgba(232, 93, 4, 0.04);
  transition: all 0.2s var(--ease-smooth);
  position: relative;
  will-change: transform;
  transform: translateZ(0);
  backface-visibility: hidden;
}

.module-item::before {
  content: '';
  position: absolute;
  left: calc(var(--space-md) * -1);
  top: 50%;
  width: var(--space-sm);
  height: 1px;
  background: rgba(232, 93, 4, 0.12);
}

.module-item:hover {
  background: rgba(255, 255, 255, 0.8);
  border-color: rgba(232, 93, 4, 0.08);
  transform: translateX(2px);
}

.module-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.module-name {
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--ink-secondary);
}

.module-stats {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  font-size: 0.72rem;
}

.module-stats .stat-label {
  color: var(--ink-soft);
}

.module-stats .stat-value {
  color: var(--ink-secondary);
  font-weight: 600;
}

.module-bar {
  height: 4px;
  background: rgba(232, 93, 4, 0.04);
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--space-3xl) var(--space-md);
  margin-top: var(--space-lg);
  text-align: center;
}

.empty-icon {
  color: var(--slate-pale);
  margin-bottom: var(--space-md);
  opacity: 0.5;
}

.empty-text {
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--page-ink);
  margin-bottom: var(--space-xs);
}

.empty-hint {
  font-size: 0.88rem;
  color: var(--page-muted);
}

.view-all-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: var(--ember-core);
  font-size: 0.88rem;
  font-weight: 700;
  text-decoration: none;
  transition: all 0.25s var(--ease-smooth);
}

.view-all-link:hover {
  color: var(--ember-glow);
}

.view-all-link svg {
  transition: transform 0.25s var(--ease-smooth);
}

.view-all-link:hover svg {
  transform: translateX(4px);
}

.activity-timeline {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
  margin-top: var(--space-lg);
}

.activity-item {
  position: relative;
  padding-left: var(--space-lg);
}

.activity-line {
  position: absolute;
  top: 1.5rem;
  left: 6px;
  bottom: calc(var(--space-md) * -1);
  width: 2px;
  background: linear-gradient(180deg, rgba(232, 93, 4, 0.2), rgba(232, 93, 4, 0));
}

.activity-item:last-child .activity-line {
  display: none;
}

.activity-dot {
  position: absolute;
  top: 1.2rem;
  left: 0;
  width: 14px;
  height: 14px;
  border-radius: 50%;
  box-shadow: 0 0 0 4px rgba(232, 93, 4, 0.08);
}

.activity-dot.success {
  background: linear-gradient(135deg, var(--forest-primary), var(--forest-bright));
}

.activity-dot.warning {
  background: linear-gradient(135deg, var(--amber-primary), var(--amber-soft));
}

.activity-dot.info {
  background: linear-gradient(135deg, var(--teal-primary), var(--teal-bright));
}

.activity-card {
  padding: var(--space-md);
  border-radius: var(--radius-md);
  background: linear-gradient(180deg, rgba(232, 93, 4, 0.02), rgba(250, 163, 7, 0.01));
  border: 1px solid rgba(232, 93, 4, 0.06);
  transition: all 0.25s var(--ease-smooth);
  will-change: transform;
  transform: translateZ(0);
  backface-visibility: hidden;
}

.activity-card:hover {
  transform: translateX(4px);
  box-shadow: var(--shadow-sm);
  border-color: rgba(232, 93, 4, 0.1);
}

.activity-card-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: var(--space-md);
}

.activity-badge {
  display: inline-flex;
  align-items: center;
  min-height: 1.75rem;
  padding: 4px 12px;
  border-radius: var(--radius-full);
  font-size: 0.7rem;
  font-weight: 700;
}

.activity-badge.success {
  background: linear-gradient(135deg, rgba(34, 197, 94, 0.1), rgba(134, 239, 172, 0.08));
  color: var(--forest-primary);
}

.activity-badge.warning {
  background: linear-gradient(135deg, rgba(217, 119, 6, 0.1), rgba(251, 191, 36, 0.08));
  color: var(--amber-primary);
}

.activity-badge.info {
  background: linear-gradient(135deg, rgba(20, 184, 166, 0.1), rgba(94, 234, 212, 0.08));
  color: var(--teal-primary);
}

.activity-time {
  font-size: 0.76rem;
  color: var(--ink-soft);
}

.activity-title {
  margin-top: var(--space-sm);
  color: var(--page-ink);
  font-size: 0.95rem;
  font-weight: 700;
}

.activity-desc {
  margin-top: 4px;
  color: var(--page-muted);
  font-size: 0.85rem;
  line-height: 1.6;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: var(--space-sm);
  margin-top: var(--space-lg);
  padding-top: var(--space-md);
  border-top: 1px solid rgba(232, 93, 4, 0.08);
}

.pagination-page {
  min-width: 2.5rem;
  height: 2.25rem;
  padding: 0 var(--space-md);
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.9rem;
  font-weight: 700;
  color: var(--page-muted);
  cursor: pointer;
  transition: all 0.25s var(--ease-smooth);
  will-change: transform;
  transform: translateZ(0);
  backface-visibility: hidden;
}

.pagination-page:hover {
  background: rgba(232, 93, 4, 0.06);
  color: var(--page-ink);
}

.pagination-page.active {
  background: linear-gradient(135deg, var(--ember-core), var(--ember-glow));
  color: white;
  box-shadow: var(--shadow-sm), 0 0 15px rgba(232, 93, 4, 0.2);
}

.expand-enter-active,
.expand-leave-active {
  transition: all 0.25s var(--ease-smooth);
  overflow: hidden;
}

.expand-enter-from,
.expand-leave-to {
  opacity: 0;
  max-height: 0;
  margin-top: 0;
}

.expand-enter-to,
.expand-leave-from {
  opacity: 1;
  max-height: 500px;
}

@media (max-width: 1220px) {
  .hero-grid {
    grid-template-columns: 1fr;
  }

  .hero-panel {
    padding-bottom: 10.5rem;
  }

  .hero-visual {
    min-height: 280px;
  }

  .visual-core {
    right: 100px;
  }

  .visual-core-ring {
    right: 70px;
  }

  .signal-primary {
    left: 0;
  }

  .insight-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .overview-lower {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .hero-panel {
    padding: var(--space-lg);
    border-radius: var(--radius-lg);
  }

  .hero-grid {
    gap: var(--space-lg);
  }

  .hero-title-main {
    font-size: 2.5rem;
  }

  .hero-highlights,
  .insight-grid {
    grid-template-columns: 1fr;
  }

  .hero-visual {
    min-height: 240px;
  }

  .blob-one {
    width: 140px;
    height: 140px;
    right: 20px;
  }

  .blob-two {
    width: 100px;
    height: 100px;
    right: 80px;
    bottom: 30px;
  }

  .visual-core {
    width: 80px;
    height: 80px;
    right: 90px;
    top: 90px;
  }

  .visual-core-ring {
    width: 120px;
    height: 120px;
    right: 70px;
    top: 70px;
  }

  .signal-primary,
  .signal-secondary,
  .signal-secondary-top,
  .signal-secondary-bottom {
    position: absolute;
  }

  .signal-primary {
    width: calc(100% - var(--space-lg));
    left: 0;
    top: 10px;
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
    margin: var(--space-md) 0 0;
    padding: var(--space-lg);
    border-radius: var(--radius-lg);
  }

  .insight-header,
  .section-header,
  .activity-card-head {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
