<template>
  <el-table
    :data="roles"
    stripe
    style="width: 100%"
  >
    <el-table-column
      prop="name"
      label="Name"
      width="180"
    />
    <el-table-column
      prop="description"
      label="Description"
    />
    <el-table-column
      prop="created_at"
      label="Assigned Date"
    />
  </el-table>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import { IRoleData } from '@/api/types';

@Component({
  name: 'Roles'
})
export default class extends Vue {
  @Prop({ required: true }) private roles!: IRoleData;
  // var d = new Date('2020-04-05T11:35:42.704744+00:00')
  // d.toDateString()
}
</script>
