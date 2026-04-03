<template>
  <div class="success-page">
    <div class="success-content">
      <h1>Password Reset Verified</h1>
      <p>You can now set your new password.</p>
    </div>
  </div>
</template>

<script setup>
// 空白页面，验证成功后跳转至此
</script>

<style scoped>
.success-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: white;
}

.success-content {
  text-align: center;
}

.success-content h1 {
  font-size: 2rem;
  font-weight: 700;
  color: #111827;
  margin-bottom: 1rem;
}

.success-content p {
  font-size: 1rem;
  color: #6b7280;
}
</style>
