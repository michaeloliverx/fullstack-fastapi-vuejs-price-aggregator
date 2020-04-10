<template>
  <div class="dashboard-container">
    <component :is="currentRole" />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { UserMeModule } from '@/store/modules/me';
import AdminDashboard from './admin/index.vue';
import EditorDashboard from './editor/index.vue';

@Component({
  name: 'Dashboard',
  components: {
    AdminDashboard,
    EditorDashboard
  }
})
export default class extends Vue {
  private currentRole = 'admin-dashboard';

  get roleNames() {
    return UserMeModule.role_names;
  }

  created() {
    if (!this.roleNames.includes('admin')) {
      this.currentRole = 'editor-dashboard';
    }
  }
}
</script>
