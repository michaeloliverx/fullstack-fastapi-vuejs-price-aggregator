<template>
  <el-table
    :data="userRoles"
    stripe
    style="width: 100%"
  >
    <el-table-column
      v-for="prop in tableProps"
      :key="prop.name"
      :label="prop.label"
      :align="prop.align"
      :min-width="prop.minWidth"
    >
      <template slot-scope="{row}">
        <span v-if="prop.type === 'text'">
          {{ row[prop.name] }}
        </span>
        <span v-if="prop.type === 'timestamp'">
          {{ new Date(row[prop.name]).toDateString() }}
        </span>
        <span v-if="prop.type === 'tag'">
          <el-tag
            :type="prop.tag[row[prop.name]]"
          >
            {{ row[prop.name] }}
          </el-tag>
        </span>
      </template>
    </el-table-column>
  </el-table>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import { IRoleData } from '@/api/types';
import { UserMeModule } from '@/store/modules/me';

@Component({
  name: 'Roles'
})
export default class extends Vue {
    private tableProps = [
      { name: 'name', type: 'text', label: 'Name', align: 'center', minWidth: 80 },
      { name: 'description', type: 'text', label: 'Description', align: 'center', minWidth: 80 },
      { name: 'created_at', type: 'timestamp', label: 'Assigned', align: 'center', minWidth: 80 }
    ]

    get userRoles() {
      return UserMeModule.roles;
    }

    created() {
      this.getData();
    }

    private async getData() {
      await UserMeModule.GetUserMeRoles();
    }
}
</script>
