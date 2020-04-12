<template>
  <div class="app-container">
    <div
      class="search-prices"
    >
      <div class="search-terms">
        <el-select
          v-model="params.include"
          multiple
          placeholder="Select shops"
          no-data-text="No shops available"
        >
          <el-option
            v-for="shop in allShops"
            :key="shop.id"
            :label="shop.name"
            :value="shop.id"
          />
        </el-select>
        <el-input
          v-model="params.query"
          placeholder="Query"
          clearable
          style="width: 200px"
        />
        <el-button
          :loading="loading"
          type="primary"
          @click="searchPrices()"
        >
          Search
        </el-button>
      </div>
    </div>

    <div class="search-results">
      <div
        class="item"
        v-for="shopResult in results"
        :key="shopResult.id"
      >
        <div
          v-for="listing in shopResult.listings"
          :key="listing.url"
        >
          <el-card
          class="hover">
            <img
              :src="listing.image_url"
              class="image"
            >
            <div style="padding: 14px;">
              <span>{{ listing.name }}</span>
              <div class="bottom clearfix">
                <time class="time">{{ listing.price }}</time>
                <el-button
                  type="text"
                  class="button"
                >
                  View item
                </el-button>
              </div>
            </div>
          </el-card>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { UserMeModule } from '@/store/modules/me';
import { getShopListings } from '@/api/shops';
import { IShopListings } from '@/api/types';
import { ShopsModule } from '@/store/modules/shops';

@Component({
  name: 'Prices',
  components: {
  }
})
export default class extends Vue {
  private loading = false;
  private params = {
    include: [],
    query: '',
    limit: 10
  }

  private results: IShopListings[] = [];

  get allShops() {
    return ShopsModule.shops;
  }

  created() {
    this.getData();
  }

  private async getData() {
    await ShopsModule.GetShops({});
  }

  private async searchPrices() {
    this.loading = true;
    // Build URL params
    const params = new URLSearchParams();
    params.append('query', this.params.query);
    for (const i in this.params.include) {
      params.append('include', this.params.include[i]);
    }
    const { data } = await getShopListings(params);
    this.results = data;
    this.loading = false;
  }
}
</script>

<style lang="scss" scoped>
  .el-checkbox-group {
    padding: 10px;
  }
  .listing-card {
    width: 150px;
  }
  .search-terms {
    max-width: 700px;
    margin: 10px;
  }
  .item {
    size: 50px;
    max-width: 250px;
  }

</style>
