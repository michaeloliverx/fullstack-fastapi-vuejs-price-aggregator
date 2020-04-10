<template>
  <div class="app-container">
    <el-card class="box-card">
      <div
        slot="header"
        class="clearfix"
      >
        <span>Create a new role</span>
      </div>
      <el-form
        ref="loginForm"
        :model="createForm"
        :rules="loginRules"
        autocomplete="on"
        label-position="left"
      >
        <el-form-item
          prop="name"
          label="Role Name"
        >
          <el-input
            v-model="createForm.name"
            type="text"
            tabindex="1"
          />
        </el-form-item>

        <el-form-item
          prop="description"
          label="Role Description"
        >
          <el-input
            v-model="createForm.description"
            type="text"
            tabindex="1"
          />
        </el-form-item>

        <el-button
          :loading="loading"
          type="primary"
          @click="handleCreate"
        >
          Create
        </el-button>

        <el-button
          @click="$router.back()"
        >
          Cancel
        </el-button>
      </el-form>
    </el-card>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { Form as ElForm, Input } from 'element-ui';
import { RolesModule } from '@/store/modules/roles';
import { IRoleCreate } from '@/api/types';

@Component({
  name: 'CreateRole',
  components: {}
})
export default class extends Vue {
  private loading = false;

  private createForm = {
    name: '',
    description: ''
  };

  private loginRules = {
    name: [{ trigger: 'blur', required: true, message: 'Please enter a name' }],
    description: [{ trigger: 'blur', required: true, message: 'Please enter a description' }]
  };

  mounted() {
    (this.$refs.name as Input).focus();
    (this.$refs.description as Input).focus();
  }

  private handleCreate() {
    (this.$refs.loginForm as ElForm).validate(async(valid: boolean) => {
      if (valid) {
        this.loading = true;
        const roleToCreate: IRoleCreate = {
          name: this.createForm.name,
          description: this.createForm.description
        };
        await RolesModule.CreateRole(roleToCreate)
          .then(() => {
            this.$message.success('Role created successfully');
            this.$router.push('/roles/list');
          }).catch(() => this.$message.error('Failed to create role'))
          .finally(() => {
            this.loading = false;
          });
      } else {
        this.$message.error('validation failed');
      }
    });
  }
}
</script>

<style lang="scss" scoped>

</style>
