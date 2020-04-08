<template>
  <div class="dashboard-container">
    <h2>Welcome, {{ user.first_name }}</h2>
    <div class="dashboard-text">
      <span />
    </div>

    <div class="dashboard-text">
      roles: <span
        v-for="role in roles"
        :key="role"
      >{{ role.name }}</span>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { UserModule } from '@/store/modules/user';

@Component({
  name: 'Dashboard'
})
export default class extends Vue {
  get user() {
    return UserModule.user;
  }

  get roles() {
    return UserModule.roles;
  }
}
</script>

<style lang="scss" scoped>
.dashboard {
  &-container {
    margin: 30px;
  }

  &-text {
    font-size: 30px;
    line-height: 46px;
  }
}
</style>
