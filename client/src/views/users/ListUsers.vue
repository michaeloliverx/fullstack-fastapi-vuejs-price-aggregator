<template>
  <div class="app-container">
    <el-button
      type="primary"
      icon="el-icon-circle-plus"
      size="medium"
      @click="$router.push('/users/create/')"
    >
      Add
    </el-button>

    <el-table
      v-loading="loading"
      :data="users"
      style="width: 100%"
      empty-text="-"
    >
      <el-table-column
        prop="id"
        label="ID"
        width="80"
      />
      <el-table-column
        prop="email"
        label="Email"
        width="300"
      />
      <el-table-column
        prop="first_name"
        label="First Name"
        min-width="100"
      />
      <el-table-column
        prop="last_name"
        label="Last Name"
        min-width="100"
      />

      <el-table-column
        label="Status"
        prop="status"
        min-width="100"
      >
        <template slot-scope="{row}">
          <el-tag
            v-if="row.status === 'active'"
            type="primary"
          >
            {{ row.status }}
          </el-tag>

          <el-tag
            v-else-if="row.status === 'disabled'"
            type="danger"
          >
            {{ row.status }}
          </el-tag>
          <el-tag
            v-else-if="row.status === 'inactive'"
            type="warning"
          >
            {{ row.status }}
          </el-tag>
        </template>
      </el-table-column>

      <el-table-column
        prop="created_at"
        label="Created"
      >
        <template slot-scope="{row}">
          {{ new Date(row.created_at).toDateString() }}
        </template>
      </el-table-column>

      <el-table-column
        fixed="right"
        label="Actions"
        min-width="100px"
      >
        <template slot-scope="{row}">
          <el-button
            type="primary"
            plain
            size="small"
            icon="el-icon-edit"
            @click="$router.push('/users/edit/' + row.id)"
          >
            Edit
          </el-button>

          <el-button
            type="danger"
            plain
            size="small"
            icon="el-icon-delete"
            @click="handleDeleteDialog(row)"
          >
            Delete
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog
      title="Tips"
      :visible.sync="deleteDialogVisible"
      width="30%"
      :before-close="deleteData"
    >
      <span>Delete user?</span>
      <span
        slot="footer"
        class="dialog-footer"
      >
        <el-button @click="deleteDialogVisible = false">Cancel</el-button>
        <el-button
          type="primary"
          @click="deleteData()"
        >Confirm</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { IUserData, IUserUpdate } from '@/api/types';
import { UsersModule } from '@/store/modules/users';
import EditUser from './EditUser.vue';
import { UserStatus } from '@/api/enums';

@Component({
  name: 'ListUsers',
  components: {
    EditUser
  }
})
export default class extends Vue {
  private loading = true;
  private listQuery = { offset: 0, limit: 100 };
  private tempUserData = {} as IUserData;
  private deleteDialogVisible = false;

  get users() {
    return UsersModule.users;
  }

  get userStatus() {
    return UserStatus;
  }

  created() {
    this.getUserList();
  }

  private resetTempArticleData() {
    this.tempUserData = {} as IUserData;
  }

  private async getUserList() {
    this.loading = true;
    await UsersModule.GetUsers(this.listQuery);
    this.loading = false;
  }

  private handleDeleteDialog(row: IUserData) {
    this.tempUserData = row;
    this.deleteDialogVisible = true;
  }

  private async deleteData() {
    await UsersModule.DeleteUser(this.tempUserData.id);
    this.deleteDialogVisible = false;
    this.resetTempArticleData();
  }

  private async updateData() {
    await UsersModule.UpdateUser(this.tempUserData.id, {});
  }
}
</script>

<style lang="scss" scoped>
  .el-header {
    padding-top: 20px;
    margin-top: auto
  }
</style>
