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
      <el-row
        v-for="shop in results"
        :key="shop.id"
        :gutter="12"
      >
        <h2>{{ shop.name }}</h2>
        <el-col
          v-for="item in shop.listings"
          :key="item.url"
          :span="8"
        >
          <el-card
            class="box-card small"
            shadow="hover"
          >
            <el-row>
              <el-col :span="4">
                <div class="card-img">
                  <el-image
                    style="width: 100px; height: 100px"
                    :src="item.image_url"
                    fit="scale-down"
                    lazy
                  />
                </div>
              </el-col>
            </el-row>

            <el-row>
              {{ item.name }}
            </el-row>

            <el-row>
              <span class="item-price">£{{ item.price }}</span>
            </el-row>

            <el-row>
              <span class="item-price">£{{ item.price_per_unit }}</span>
            </el-row>

            <el-row>
              <el-col>
                <el-button
                  type="text"
                  class="button"
                >
                  <el-link
                    :href="item.url"
                    type="primary"
                  >
                    View Item
                  </el-link>
                </el-button>
              </el-col>
            </el-row>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
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
  .box-card {
    margin: 5px;
    max-width: 100rem;
    .item-price {
      font-weight: bold;
    }
  }
  .search-terms {
    max-width: 700px;
    margin: 10px;
  }
  .item {
    size: 50px;
    max-width: 250px;
  }
  .card-img {
    height: auto;
    max-width: 30%;
  }

</style>
