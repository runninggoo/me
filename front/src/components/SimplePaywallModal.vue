<template>
  <div v-if="isOpen" class="paywall-overlay" @click.self="closeModal">
    <div class="paywall-modal">
      <div class="paywall-header">
        <div class="paywall-icon">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
            <path fill-rule="evenodd" d="M12 1.5a5.25 5.25 0 00-5.25 5.25v3a3 3 0 00-3 3v6.75a3 3 0 003 3h10.5a3 3 0 003-3v-6.75a3 3 0 00-3-3v-3c0-2.9-2.35-5.25-5.25-5.25zm3.75 8.25v-3a3.75 3.75 0 10-7.5 0v3h7.5z" clip-rule="evenodd" />
          </svg>
        </div>
        <h3 class="paywall-title">付费查看</h3>
      </div>
      <div class="paywall-content">
        <p>此内容需要支付 <span class="paywall-price">1元</span> 查看。支付后即可完整浏览。</p>
      </div>
      <div class="paywall-actions">
        <button class="paywall-button" @click="payAndView">支付1元并查看</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, defineEmits } from 'vue'

const emit = defineEmits(['close', 'pay'])

const isOpen = ref(true)

const closeModal = () => {
  isOpen.value = false
  emit('close')
}

const payAndView = () => {
  console.log('模拟支付1元')
  isOpen.value = false
  emit('pay')
}
</script>

<style scoped>
.paywall-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 50;
  padding: 1rem;
}

.paywall-modal {
  background-color: white;
  border-radius: 0.5rem;
  padding: 1.5rem;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  max-width: 24rem;
  width: 100%;
  text-align: center;
}

.paywall-header {
  margin-bottom: 1rem;
}

.paywall-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 3rem;
  height: 3rem;
  border-radius: 9999px;
  background-color: rgb(254, 252, 232);
  margin-bottom: 0.5rem;
}

.paywall-icon svg {
  width: 1.5rem;
  height: 1.5rem;
  color: rgb(161, 98, 7);
}

.paywall-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: rgb(17, 24, 39);
  margin: 0;
}

.paywall-content {
  margin-bottom: 1.5rem;
}

.paywall-content p {
  color: rgb(107, 114, 128);
  font-size: 0.875rem;
  margin: 0;
}

.paywall-price {
  font-weight: 700;
  color: rgb(220, 38, 38);
}

.paywall-actions {
  display: flex;
  justify-content: center;
}

.paywall-button {
  display: inline-flex;
  justify-content: center;
  align-items: center;
  border-radius: 0.375rem;
  border: 1px solid transparent;
  background-color: rgb(79, 70, 229);
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
  font-weight: 500;
  color: white;
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  cursor: pointer;
  transition: background-color 0.2s;
}

.paywall-button:hover {
  background-color: rgb(67, 56, 202);
}

.paywall-button:focus {
  outline: 2px solid transparent;
  outline-offset: 2px;
  box-shadow: 0 0 0 2px rgb(255, 255, 255), 0 0 0 4px rgb(79, 70, 229);
}
</style>