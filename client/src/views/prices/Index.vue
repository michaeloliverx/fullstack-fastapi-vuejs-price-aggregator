<template>
  <div class="app-container">
    <h1>Prices</h1>

    <el-input
      v-model="params.query"
      placeholder="Query"
      clearable
    />
    <el-button
      type="primary"
      @click="searchPrices()"
    >
      Go
    </el-button>

    {{ results }}
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { UserMeModule } from '@/store/modules/me';
import { getShopListings } from '@/api/shops';
import { IShopListings } from '@/api/types';

@Component({
  name: 'Prices',
  components: {
  }
})
export default class extends Vue {
  private params = {
    query: '',
    limit: 10
  }

  private results: IShopListings[] = [];

  get userShops() {
    return UserMeModule.shops;
  }

  created() {
    UserMeModule.GetUserMeShops();
  }

  private async searchPrices() {
    const params = new URLSearchParams();
    params.append('query', this.params.query);
    params.append('include', '1');
    params.append('include', '2');
    params.append('include', '3');
    params.append('include', '4');
    params.append('include', '5');
    params.append('include', '6');
    params.append('include', '7');
    const { data } = await getShopListings(params);
    this.results = data;
  }
}
</script>

<style lang="scss" scoped>
  .el-checkbox-group {
    padding: 10px;
  }
  .price-card {
    width: 150px;
  }

</style>
