<template>
  <div class="app-container">
    <el-table
      :data="shops"
      style="width: 100%"
    >
      <el-table-column
        v-for="prop in tableConfig.props"
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

      <el-table-column
        v-if="tableConfig.actions"
        fixed="right"
        label="Actions"
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
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { ShopsModule } from '@/store/modules/shops';

@Component({
  name: 'ListShops',
  components: {}
})
export default class extends Vue {
  private loading = true;

  private tableConfig = {
    props: [
      { name: 'id', type: 'text', label: 'ID', align: 'center', minWidth: 20 },
      { name: 'name', type: 'text', label: 'Name', align: 'center', minWidth: 80 },
      { name: 'created_at', type: 'timestamp', label: 'Created', align: 'center', minWidth: 80 },
      { name: 'url', type: 'text', label: 'URL', align: 'center', minWidth: 80 },
      {
        name: 'render_javascript',
        label: 'Renders JavaScript',
        type: 'tag',
        align: 'center',
        minWidth: 80,
        tag: {
          true: 'primary',
          false: 'info'
        }
      }
    ],
    actions: [
      { text: 'Edit', type: 'primary', icon: 'el-icon-edit', size: 'small', goto: '/dashboard' },
      { text: 'Delete', type: 'danger', icon: 'el-icon-delete', size: 'small', goto: '/dashboard' }
    ]
  }

  get shops() {
    return ShopsModule.shops;
  }

  created() {
    ShopsModule.GetShops({});
  }
}
</script>

<style lang="scss" scoped>

</style>
