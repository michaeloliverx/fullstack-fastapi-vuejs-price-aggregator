<template>
  <div>
    <el-button
      style="float: right; padding: 3px 0"
      type="text"
      @click="handleUpdate()"
    >
      Update
    </el-button>
    <el-select
      v-model="selectedShops"
      multiple
      placeholder="Select"
      no-data-text="No shops available"
    >
      <el-option
        v-for="shop in allShops"
        :key="shop.id"
        :label="shop.name"
        :value="shop.id"
      />
    </el-select>
    <el-table
      :data="userShops"
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
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import { IShopData } from '@/api/types';
import { UserMeModule } from '@/store/modules/me';
import { ShopsModule } from '@/store/modules/shops';

@Component({
  name: 'UserShops'
})
export default class extends Vue {
  private loading = false;
  private selectedShops = [];
  private tableProps = [
    { name: 'name', type: 'text', label: 'Name', align: 'center', minWidth: 80 }
  ]

  get userShops() {
    return UserMeModule.shops;
  }

  get allShops() {
    return ShopsModule.shops;
  }

  created() {
    this.getData();
  }

  private async getData() {
    await UserMeModule.GetUserMeShops();
    await ShopsModule.GetShops({});
  }

  private async handleUpdate() {
    this.loading = true;
    await UserMeModule.UpdateUserMeShops(this.selectedShops);
    this.loading = false;
  }
}
</script>

<style lang="scss" scoped>
  .el-card {
    margin: 5px;

  }

</style>
