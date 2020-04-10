<template>
  <el-container>
    <el-header>
      <el-button
        type="primary"
        icon="el-icon-circle-plus"
        size="medium"
        @click="$router.push('/roles/create/')"
      >
        Add
      </el-button>
    </el-header>
    <el-main>
      <el-table
        v-loading="loading"
        :data="roles"
        style="width: 100%"
      >
        <el-table-column
          prop="id"
          label="ID"
          width="80"
          min-width="80"
        />
        <el-table-column
          prop="name"
          label="Name"
          min-width="100"
        />
        <el-table-column
          prop="description"
          label="Description"
          min-width="200"
        />

        <el-table-column
          prop="created_at"
          label="Created"
          min-width="150"
        >
          <template slot-scope="{row}">
            {{ new Date(row.created_at).toDateString() }}
          </template>
        </el-table-column>

        <el-table-column
          fixed="right"
          label="Actions"
        >
          <template slot-scope="{row}">
            <el-button
              type="primary"
              plain
              size="small"
              icon="el-icon-edit"
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
    </el-main>

    <el-dialog
      title="Warning"
      :visible.sync="deleteDialogVisible"
      width="30%"
      :before-close="handleClose"
    >
      <span>Delete role?</span>
      <span
        slot="footer"
        class="dialog-footer"
      >
        <el-button @click="deleteDialogVisible = false">Cancel</el-button>
        <el-button
          type="primary"
          @click="handleDelete()"
        >Confirm</el-button>
      </span>
    </el-dialog>
  </el-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { IRoleData } from '@/api/types';
import { RolesModule } from '@/store/modules/roles';

@Component({
  name: 'ListRole',
  components: {}
})
export default class extends Vue {
  private loading = true;
  private tempRoleData = {} as IRoleData;
  private deleteDialogVisible = false;
  private dialogFormVisible = false
  private dialogStatus = ''
  private textMap = {
    update: 'Edit',
    create: 'Create'
  }

  get roles() {
    return RolesModule.roles;
  }

  created() {
    this.getRoleList();
  }

  private async getRoleList() {
    this.loading = true;
    await RolesModule.GetRoles({});
    this.loading = false;
  }

  private resetTempRole() {
    this.tempRoleData = {} as IRoleData;
  }

  private handleDeleteDialog(row: IRoleData) {
    this.deleteDialogVisible = true;
    this.tempRoleData = row;
  }

  private async handleDelete() {
    await RolesModule.DeleteRole(this.tempRoleData.id);
    this.deleteDialogVisible = false;
    this.resetTempRole();
    this.$message.success('Role has been deleted');
  }
}
</script>

<style lang="scss" scoped>
  .el-header {
    padding-top: 20px;
    margin-top: auto
  }
</style>
