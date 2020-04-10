<template>
  <div class="dashboard-editor-container">
    <h1>Admin Dashboard</h1>
  </div>
</template>

<script lang="ts">
import 'echarts/theme/macarons.js'; // Theme used in BarChart, LineChart, PieChart and RadarChart
import { Component, Vue } from 'vue-property-decorator';

@Component({
  name: 'DashboardAdmin',
  components: {

  }
})
export default class extends Vue {

}
</script>

<style lang="scss" scoped>
.dashboard-editor-container {
  padding: 32px;
  background-color: rgb(240, 242, 245);
  position: relative;

}
</style>
