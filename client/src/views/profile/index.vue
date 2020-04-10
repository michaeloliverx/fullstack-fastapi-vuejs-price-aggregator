<template>
  <div class="app-container">
    <div v-if="user">
      <el-row :gutter="20">
        <el-col
          :span="18"
        >
          <el-card>
            <el-tabs v-model="activeTab">
              <el-tab-pane
                label="Account"
                name="account"
              >
                <Account :user="user" />
              </el-tab-pane>

              <el-tab-pane
                label="Roles"
                name="roles"
              >
                <Roles :roles="roles" />
              </el-tab-pane>
            </el-tabs>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { UserMeModule } from '@/store/modules/me';
import Account from '@/views/profile/components/Account.vue';
import Roles from '@/views/profile/components/Roles.vue';
@Component({
  name: 'Profile',
  components: {
    Account,
    Roles
  }
})
export default class extends Vue {
  private activeTab = 'account';

  get user() {
    return UserMeModule.user;
  }

  get roles() {
    return UserMeModule.roles;
  }
}
</script>
