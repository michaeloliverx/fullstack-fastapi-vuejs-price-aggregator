<template>
  <div
    class="app-container"
    align="center"
  >
    <el-card class="box-card">
      <el-form
        ref="createForm"
        :model="createForm"
        :rules="createFormRules"
        label-position="left"
        label-width="170px"
      >
        <el-form-item
          label="Name"
        >
          <el-input
            v-model="createForm.firstName"
            placeholder="First name"
          />

          <el-input
            v-model="createForm.lastName"
            placeholder="Last name"
          />
        </el-form-item>

        <el-form-item label="Email">
          <el-input v-model="createForm.email" />
        </el-form-item>

        <el-form-item label="Password">
          <el-input
            v-model="createForm.password"
            type="password"
            show-password
          />
          <el-input
            v-model="createForm.password2"
            type="password"
            placeholder="Confirm password"
            show-password
          />
        </el-form-item>

        <el-form-item label="Account Status">
          <el-select
            v-model="createForm.status"
            placeholder="Please select status"
          >
            <el-option
              v-for="status in userStatus"
              :key="status"
              :label="status"
              :value="status"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="Assign roles (optional)">
          <el-select
            v-model="createForm.roles"
            multiple
            placeholder="Select"
            no-data-text="No roles available"
          >
            <el-option
              v-for="role in roles"
              :key="role.id"
              :label="role.name"
              :value="role.id"
            />
          </el-select>
        </el-form-item>

        <el-form-item>
          <el-button
            type="primary"
            :loading="loading"
            @click="onSubmit"
          >
            Create
          </el-button>
          <el-button @click="$router.back()">
            Cancel
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { RolesModule } from '@/store/modules/roles';
import { UsersModule } from '@/store/modules/users';
import { UserStatus } from '@/api/enums';
import { IUserCreate } from '@/api/types';
import { UserMeModule } from '@/store/modules/me';
import { rejects } from 'assert';
import { Form } from 'element-ui';

@Component({
  name: 'CreateUser',
  components: {}
})
export default class extends Vue {
  private loading = false
  private createForm = {
    firstName: '',
    lastName: '',
    email: '',
    password: '',
    password2: '',
    status: '',
    roles: []
  }

   private validatePass = (rule: any, value: string, callback: any) => {
     if (value === '') {
       callback(new Error('Please input the password'));
     }
     callback();
   };

  private createFormRules = {
    firstName: [
      { required: true, message: 'Please enter first name', trigger: 'blur' }
    ],
    lastName: [{ required: true, message: 'Please enter last name', trigger: 'change' }]
  }

  get userStatus() {
    return UserStatus;
  }

  get roles() {
    return RolesModule.roles;
  }

  created() {
    this.getRolesList();
  }

  private async getRolesList() {
    await RolesModule.GetRoles({});
  }

  private async onSubmit() {
    const form = this.$refs.createForm as Form;
    console.log(form.validate());
    form.validate(async(valid: boolean) => {
      if (valid) {
        console.log('Valid');
      } else {
        console.log('No valid');
      }
    }
    );
  };

  // private async onSubmit() {
  //   this.loading = true;
  //
  //   const userToCreate: IUserCreate = {
  //     email: this.form.email,
  //     password: this.form.password,
  //     first_name: this.form.firstName,
  //     last_name: this.form.lastName,
  //     status: this.form.status as UserStatus
  //   };
  //
  //   await UsersModule.CreateUser(userToCreate)
  //     .then(() => {
  //       this.$message.success('User created successfully.');
  //       this.$router.push('/users/list');
  //     })
  //     .catch((rejects) => {
  //       this.$message.error('Failed to create user.');
  //       const { detail } = rejects.response.data;
  //       console.log(detail);
  //
  //       this.$notify({
  //         title: 'Validation error',
  //         message: detail,
  //         type: 'warning'
  //       });
  //     })
  //     .finally(() => {
  //       this.loading = false;
  //     });
  // }
}
</script>

<style lang="scss" scoped>
  .box-card {
    position: center;
    padding: 15px;
    max-width: 700px;
  }
  .el-input {
    margin: 5px;
  }
</style>
