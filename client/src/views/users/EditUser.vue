<template>
  <div>
    Edit
    {{ user }}
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

  public cancel() {
    router.back();
  }
}
</script>
