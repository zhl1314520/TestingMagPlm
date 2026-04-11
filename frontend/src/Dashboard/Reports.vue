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
    </div>
  </div>
</template>

<script setup>
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

.page-subtitle {
  font-size: 1rem;
  opacity: 0.9;
  margin: 0;
}
</style>
