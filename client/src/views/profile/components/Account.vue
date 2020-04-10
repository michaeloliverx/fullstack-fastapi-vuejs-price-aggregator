<template>
  <el-form>
    <span>Status: </span>
    <el-tag
      :type="user.status === UserStatus.active ? 'success' : 'danger'"
      effect="light"
    >
      {{ user.status }}
    </el-tag>

    <el-form-item label="First Name">
      <el-input v-model="user.first_name" />
    </el-form-item>

    <el-form-item label="Last Name">
      <el-input v-model="user.last_name" />
    </el-form-item>

    <el-form-item label="Email">
      <el-input v-model="user.email" />
    </el-form-item>

    <el-form-item label="Password">
      <el-input
        v-model="password"
        placeholder="Please enter new password"
        show-password
      />
    </el-form-item>

    <el-form-item>
      <el-button
        type="primary"
        @click="submit"
      >
        Update
      </el-button>
    </el-form-item>
  </el-form>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import { IUserData, IUserUpdate } from '@/api/types';
import { UserStatus } from '@/api/enums';
import { UserMeModule } from '@/store/modules/me';

@Component({
  name: 'Account'
})
export default class extends Vue {
  @Prop({ required: true }) private user!: IUserData;
  password = '';

  // may have to declare some private vars that are not related to reactive state
  UserStatus = UserStatus;

  private submit() {
    const updateData: IUserUpdate = {};
    if (this.password !== '') {
      updateData.password = this.password;
    }
    /*
    Does API request to update current user with data currently inside component.
    on error will loop through details and create message toast.

     */
    UserMeModule.UpdateUserMe(this.user).then(() => {
      this.$message({
        message: 'User information has been updated successfully',
        type: 'success',
        duration: 5 * 1000
      });
    }).catch((rejects) => {
      const { detail } = rejects.response.data;
      detail.map((detail: { msg: any }) =>
        this.$message({
          message: detail.msg,
          type: 'error',
          duration: 5 * 1000
        }));
    });
  };
}
</script>
