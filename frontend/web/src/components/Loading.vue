<script setup></script>

<template>
  <div class="container">
    <div class="loading">
      <img
        id="loading-icon"
        width="250"
        height="250"
        src="@/assets/dots-rotate.svg"
        alt="Loading"
      />
      <span id="loading-text">Loading...</span>
    </div>
  </div>
</template>

<style scoped>
.loading {
  display: flex;
  flex-direction: column;
  margin: 2rem auto;
}

#loading-icon {
  margin: 2rem auto;
}

#loading-text {
  font-size: 32px;
  margin: 0 auto;
  padding: 0.5rem;
}
</style>
