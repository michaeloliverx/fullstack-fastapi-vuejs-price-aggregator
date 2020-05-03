<template>
  <div>
    Edit
    {{ user }}

    <el-button type="primary" @click="handleClick">Log</el-button>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';
import { IUserData, IUserUpdate } from '@/api/types';
import router from '@/router';

@Component({
  name: 'EditUser',
  components: {}
})
export default class extends Vue {
  @Prop({ required: true }) private user!: IUserData;
  private updateForm = {
    email: '',
    firstName: '',
    lastName: '',
    password: '',
    status: ''
  };

  private userID = '';

  public cancel() {
    router.back();
  }

  public handleClick() {
    console.log(this.$route);
  }

}
</script>
