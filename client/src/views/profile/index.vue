<template>
  <div class="app-container">
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

            <el-tab-pane label="Roles">
              <UserRoles />
            </el-tab-pane>

            <el-tab-pane label="Shops">
              <UserShops />
            </el-tab-pane>
          </el-tabs>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { UserMeModule } from '@/store/modules/me';
import Account from '@/views/profile/components/Account.vue';
import UserRoles from '@/views/profile/components/UserRoles.vue';
import UserShops from '@/views/profile/components/UserShops.vue';
@Component({
  name: 'Profile',
  components: {
    Account,
    UserRoles,
    UserShops
  }
})
export default class extends Vue {
  private activeTab = 'account';

  get user() {
    return UserMeModule.user;
  }

  created() {
    this.getData();
  }

  private async getData() {
    await UserMeModule.GetUserMe();
  }
}
</script>
