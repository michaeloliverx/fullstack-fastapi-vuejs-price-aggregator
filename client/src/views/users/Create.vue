<template>
  <el-row
    type="flex"
    class="row-bg"
    justify="center"
  >
    <el-col :span="12">
      <el-form
        ref="form"
        :model="form"
        label-width="170px"
      >
        <el-form-item
          label="Name"
        >
          <el-input
            v-model="form.firstName"
            placeholder="First name"
          />

          <el-input
            v-model="form.lastName"
            placeholder="Last name"
          />
        </el-form-item>

        <el-form-item label="Email">
          <el-input v-model="form.email" />
        </el-form-item>

        <el-form-item label="Password">
          <el-input
            v-model="form.password"
            type="password"
            show-password
          />
          <el-input
            v-model="form.password2"
            type="password"
            placeholder="Confirm password"
            show-password
          />
        </el-form-item>
        <el-form-item label="Account Status">
          <el-radio-group v-model="form.status">
            <el-radio
              v-for="status in userStatus"
              :key="status"
              :label="status"
            >
              {{ status }}
            </el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item label="Assign roles">
          <el-checkbox-group v-model="form.roles">
            <el-checkbox
              v-for="role in roles"
              :key="role.name"
              :label="role.name"
              border
            />
          </el-checkbox-group>
        </el-form-item>

        <el-form-item>
          <el-button
            type="primary"
            @click="onSubmit"
          >
            Create
          </el-button>
          <el-button @click="$router.back()">
            Cancel
          </el-button>
        </el-form-item>
      </el-form>
    </el-col>
  </el-row>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { RolesModule } from '@/store/modules/roles';
import { UsersModule } from '@/store/modules/users';
import { UserStatus } from '@/api/enums';
import {IUserCreate} from "@/api/types";

@Component({
  name: 'CreateUser',
  components: {}
})
export default class extends Vue {
  private form = {
    firstName: '',
    lastName: '',
    email: '',
    password: '',
    password2: '',
    status: '',
    roles: []
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
    const loading = this.$loading({
      lock: true,
      text: 'Loading',
      spinner: 'el-icon-loading'
    });

    const userToCreate: IUserCreate = {
      email: this.form.email,
      password: this.form.password,
      first_name: this.form.firstName,
      last_name: this.form.lastName,
      status: this.form.status as UserStatus
    };
    await UsersModule.CreateUser(userToCreate);
    loading.close();
  }
}
</script>

<style lang="scss" scoped>
  .grid-content {
    border-radius: 4px;
    min-height: 36px;
  }
  .row-bg {
    padding: 10px 0;
    background-color: #f9fafc;
  }
</style>
