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

const jsonData = '[{"id":1,"name":"aldi","listings":[{"name":"Fresh Tagliatelle Pasta","url":"https:\\/\\/www.aldi.co.uk\\/fresh-tagliatelle-pasta\\/p\\/016774333996602","price":"1.192.38perkg","price_per_unit":null,"image_url":"https:\\/\\/cdn.aldi-digital.co.uk\\/\\/Fresh-Tagliatelle-Pasta-A.jpg?o=PDOPN2HcYse7V5Fh%24nrTgxqzg6oj&V=QuE%24&w=178&h=223&p=2&q=88, https:\\/\\/cdn.aldi-digital.co.uk\\/\\/Fresh-Tagliatelle-Pasta-A.jpg?o=PDOPN2HcYse7V5Fh%24nrTgxqzg6oj&V=QuE%24&w=356&h=446&p=2&q=83 2x"},{"name":"Cheese Pasta Salad","url":"https:\\/\\/www.aldi.co.uk\\/cheese-pasta-salad\\/p\\/002460198287502","price":"0.9924.8pper100g","price_per_unit":null,"image_url":"https:\\/\\/cdn.aldi-digital.co.uk\\/\\/Cheese-Pasta-Salad-A.jpg?o=2mt6etRnUjpczXatInBzb6orx78j&V=NP9g&w=178&h=223&p=2&q=88, https:\\/\\/cdn.aldi-digital.co.uk\\/\\/Cheese-Pasta-Salad-A.jpg?o=2mt6etRnUjpczXatInBzb6orx78j&V=NP9g&w=356&h=446&p=2&q=83 2x"},{"name":"Carbonara Pasta Sauce","url":"https:\\/\\/www.aldi.co.uk\\/carbonara-pasta-sauce\\/p\\/002806000353200","price":"0.5216.8pper100g","price_per_unit":null,"image_url":"https:\\/\\/cdn.aldi-digital.co.uk\\/\\/Carbonara-Pasta-Sauce-A.jpg?o=UnLYVAmb7OB4c3tesLdVs%40%4087vAj&V=YSDf&w=178&h=223&p=2&q=88, https:\\/\\/cdn.aldi-digital.co.uk\\/\\/Carbonara-Pasta-Sauce-A.jpg?o=UnLYVAmb7OB4c3tesLdVs%40%4087vAj&V=YSDf&w=356&h=446&p=2&q=83 2x"},{"name":"Tuna Pasta Bake","url":"https:\\/\\/www.aldi.co.uk\\/tuna-pasta-bake\\/p\\/081857200400800","price":"1.894.73perkg","price_per_unit":null,"image_url":"https:\\/\\/cdn.aldi-digital.co.uk\\/\\/Tuna-Pasta-Bake-A.jpg?o=t%40kJu1l6U6pWwwJabcSEMvRBZS4j&V=138d&w=178&h=223&p=2&q=88, https:\\/\\/cdn.aldi-digital.co.uk\\/\\/Tuna-Pasta-Bake-A.jpg?o=t%40kJu1l6U6pWwwJabcSEMvRBZS4j&V=138d&w=356&h=446&p=2&q=83 2x"},{"name":"Carbonara Pasta Sauce","url":"https:\\/\\/www.aldi.co.uk\\/carbonara-pasta-sauce\\/p\\/077398279806002","price":"0.992.83perkg","price_per_unit":null,"image_url":"https:\\/\\/cdn.aldi-digital.co.uk\\/\\/Carbonara-Pasta-Sauce-A.jpg?o=viutNWO38%40hx0Jvb7c4UiOmj0JEj&V=YSDf&w=178&h=223&p=2&q=88, https:\\/\\/cdn.aldi-digital.co.uk\\/\\/Carbonara-Pasta-Sauce-A.jpg?o=viutNWO38%40hx0Jvb7c4UiOmj0JEj&V=YSDf&w=356&h=446&p=2&q=83 2x"},{"name":"Fresh Fusilli Pasta","url":"https:\\/\\/www.aldi.co.uk\\/fresh-fusilli-pasta\\/p\\/016774333996401","price":"1.192.38perkg","price_per_unit":null,"image_url":"https:\\/\\/cdn.aldi-digital.co.uk\\/\\/Fresh-Fusilli-Pasta-A.jpg?o=8%40H%24%24cncr2y8N1fQ8%40q8O4vkzM4j&V=%40M%243&w=178&h=223&p=2&q=88, https:\\/\\/cdn.aldi-digital.co.uk\\/\\/Fresh-Fusilli-Pasta-A.jpg?o=8%40H%24%24cncr2y8N1fQ8%40q8O4vkzM4j&V=%40M%243&w=356&h=446&p=2&q=83 2x"},{"name":"Cheesy Macaroni Pasta","url":"https:\\/\\/www.aldi.co.uk\\/cheesy-macaroni-pasta\\/p\\/070916066805700","price":"0.8946.8pper100g","price_per_unit":null,"image_url":"https:\\/\\/cdn.aldi-digital.co.uk\\/\\/Cheesy-Macaroni-Pasta-A.jpg?o=3k8TrZPRA8VzbI86y7ZyLKMWKZAj&V=2Q%40z&w=178&h=223&p=2&q=88, https:\\/\\/cdn.aldi-digital.co.uk\\/\\/Cheesy-Macaroni-Pasta-A.jpg?o=3k8TrZPRA8VzbI86y7ZyLKMWKZAj&V=2Q%40z&w=356&h=446&p=2&q=83 2x"},{"name":"Chicken & Mushroom Pasta & Sauce","url":"https:\\/\\/www.aldi.co.uk\\/chicken-%26-mushroom-pasta-%26-sauce\\/p\\/043698254081501","price":"0.3933.9pper100g","price_per_unit":null,"image_url":"https:\\/\\/cdn.aldi-digital.co.uk\\/\\/Chicken-&-Mushroom-Pasta-&-Sauce-A.jpg?o=7a%40e9jK6xR7djj9w98s57poauCoj&V=oMTt&w=178&h=223&p=2&q=88, https:\\/\\/cdn.aldi-digital.co.uk\\/\\/Chicken-&-Mushroom-Pasta-&-Sauce-A.jpg?o=7a%40e9jK6xR7djj9w98s57poauCoj&V=oMTt&w=356&h=446&p=2&q=83 2x"},{"name":"Macaroni Cheese Pasta & Sauce","url":"https:\\/\\/www.aldi.co.uk\\/macaroni-cheese-pasta-%26-sauce\\/p\\/043694254081301","price":"0.3933.9pper100g","price_per_unit":null,"image_url":"https:\\/\\/cdn.aldi-digital.co.uk\\/\\/Macaroni-Cheese-Pasta-&-Sauce-A.jpg?o=XqKxTWR6Mc3Xt%40YEYf97BFWxHUMj&V=dtEQ&w=178&h=223&p=2&q=88, https:\\/\\/cdn.aldi-digital.co.uk\\/\\/Macaroni-Cheese-Pasta-&-Sauce-A.jpg?o=XqKxTWR6Mc3Xt%40YEYf97BFWxHUMj&V=dtEQ&w=356&h=446&p=2&q=83 2x"},{"name":"Cheese & Broccoli Pasta & Sauce","url":"https:\\/\\/www.aldi.co.uk\\/cheese-%26-broccoli-pasta-%26-sauce\\/p\\/043698003281800","price":"0.3933.9pper100g","price_per_unit":null,"image_url":"https:\\/\\/cdn.aldi-digital.co.uk\\/\\/Cheese-&-Broccoli-Pasta-&-Sauce-A.jpg?o=0vwg%24ZlSTGvRYs99I6IFcSqsik0j&V=hBhd&w=178&h=223&p=2&q=88, https:\\/\\/cdn.aldi-digital.co.uk\\/\\/Cheese-&-Broccoli-Pasta-&-Sauce-A.jpg?o=0vwg%24ZlSTGvRYs99I6IFcSqsik0j&V=hBhd&w=356&h=446&p=2&q=83 2x"}]},{"id":2,"name":"amazon_pantry","listings":[{"name":"Dolmio Original Bolognese Pasta Sauce, 2 x 500 g","url":"https:\\/\\/www.amazon.co.uk\\/Dolmio-Original-Bolognese-Pasta-Sauce\\/dp\\/B073QM1L3Q\\/ref=sr_1_1?dchild=1&keywords=pasta&qid=1588413654&s=pantry&sr=8-1&srs=5782660031","price":"2.00","price_per_unit":"2.00\\/kg","image_url":"https:\\/\\/m.media-amazon.com\\/images\\/I\\/91bsI1OZu6L._AC_UL320_.jpg"},{"name":"DOLMIO Bolognese 750g Extra Onion & Garlic","url":"https:\\/\\/www.amazon.co.uk\\/Dolmio-Sauce-Bolognese-Intense-Garlic\\/dp\\/B0176G8DPO\\/ref=sr_1_2?dchild=1&keywords=pasta&qid=1588413654&s=pantry&sr=8-2&srs=5782660031","price":"2.00","price_per_unit":"2.67\\/kg","image_url":"https:\\/\\/m.media-amazon.com\\/images\\/I\\/81w2DU28wFL._AC_UL320_.jpg"},{"name":"Dolmio Pasta Bake Creamy Tomato Pasta Sauce, 500 grams","url":"https:\\/\\/www.amazon.co.uk\\/Dolmio-Sauce-Pasta-Creamy-Tomato\\/dp\\/B0148K6FK6\\/ref=sr_1_3?dchild=1&keywords=pasta&qid=1588413654&s=pantry&sr=8-3&srs=5782660031","price":"1.75","price_per_unit":"3.50\\/kg","image_url":"https:\\/\\/m.media-amazon.com\\/images\\/I\\/81TWVLtaJlL._AC_UL320_.jpg"},{"name":"Uncle Ben\'s Spicy Mexican Rice 3 x 250g (750g)","url":"https:\\/\\/www.amazon.co.uk\\/Uncle-Bens-Spicy-Mexican-Rice\\/dp\\/B073H9JJL3\\/ref=sr_1_4?dchild=1&keywords=pasta&qid=1588413654&s=pantry&sr=8-4&srs=5782660031","price":"4.00","price_per_unit":"5.33\\/kg","image_url":"https:\\/\\/m.media-amazon.com\\/images\\/I\\/81V02PG4gXL._AC_UL320_.jpg"},{"name":"Domestos Original Thick Bleach, Toilet Disinfectant And Cleaner For Home And Bathroom, Removes Stains From Surafces And Kills 99.9% Of Bacteria And Germs (750 ml)","url":"https:\\/\\/www.amazon.co.uk\\/Domestos-100444506-Bleach-Original-750ml\\/dp\\/B014G50572\\/ref=sr_1_5?dchild=1&keywords=pasta&qid=1588413654&s=pantry&sr=8-5&srs=5782660031","price":"1.00","price_per_unit":"1.33\\/l","image_url":"https:\\/\\/m.media-amazon.com\\/images\\/I\\/71ERGDc7QjL._AC_UL320_.jpg"},{"name":"Loyd Grossman Tomato and Roastedgarlic Sauce, 350g","url":"https:\\/\\/www.amazon.co.uk\\/Loyd-Grossman-Tomato-Roastedgarlic-Sauce\\/dp\\/B014G2KM6Y\\/ref=sr_1_6?dchild=1&keywords=pasta&qid=1588413654&s=pantry&sr=8-6&srs=5782660031","price":"1.40","price_per_unit":"4.00\\/kg","image_url":"https:\\/\\/m.media-amazon.com\\/images\\/I\\/71rJ2hKwCIL._AC_UL320_.jpg"},{"name":"Colgate Cavity Protection Toothpaste Pump, 100 milliliters","url":"https:\\/\\/www.amazon.co.uk\\/Colgate-Cavity-Protection-Toothpaste-milliliters\\/dp\\/B014DDL4SQ\\/ref=sr_1_7?dchild=1&keywords=pasta&qid=1588413654&s=pantry&sr=8-7&srs=5782660031","price":"1.50","price_per_unit":"1.50\\/100ml","image_url":"https:\\/\\/m.media-amazon.com\\/images\\/I\\/71jrs72NWEL._AC_UL320_.jpg"},{"name":"Old El Paso Mexican Smoky BBQ Fajita Dinner Kit, 500g","url":"https:\\/\\/www.amazon.co.uk\\/Old-El-Paso-Mexican-Fajita\\/dp\\/B0161I24WG\\/ref=sr_1_8?dchild=1&keywords=pasta&qid=1588413654&s=pantry&sr=8-8&srs=5782660031","price":"2.75","price_per_unit":"5.50\\/kg","image_url":"https:\\/\\/m.media-amazon.com\\/images\\/I\\/91yzjm9uwFL._AC_UL320_.jpg"},{"name":"Heinz Baked Beans in Tomato Sauce, 415 g (Pack of 4)","url":"https:\\/\\/www.amazon.co.uk\\/Heinz-Baked-Beans-Tomato-Sauce\\/dp\\/B015O5BZDQ\\/ref=sr_1_9?dchild=1&keywords=pasta&qid=1588413654&s=pantry&sr=8-9&srs=5782660031","price":"2.50","price_per_unit":"1.51\\/kg","image_url":"https:\\/\\/m.media-amazon.com\\/images\\/I\\/81-JGC5d+dL._AC_UL320_.jpg"},{"name":"DOLMIO Sun-Ripened Tomato and Chilli Pasta Sauce, 350 g","url":"https:\\/\\/www.amazon.co.uk\\/DOLMIO-Sun-Ripened-Tomato-Chilli-Pasta\\/dp\\/B073H734C6\\/ref=sr_1_10?dchild=1&keywords=pasta&qid=1588413654&s=pantry&sr=8-10&srs=5782660031","price":"1.75","price_per_unit":"5.00\\/kg","image_url":"https:\\/\\/m.media-amazon.com\\/images\\/I\\/81XiJ8FcoBL._AC_UL320_.jpg"}]},{"id":3,"name":"asda","listings":null},{"id":4,"name":"iceland","listings":[{"name":"Pasta Reggia di Caserta Durum Semolina Pasta Spaghetti 1kg","url":"https:\\/\\/www.iceland.co.uk\\/p\\/pasta-reggia-di-caserta-durum-semolina-pasta-spaghetti-1kg\\/63445.html","price":"1.00","price_per_unit":"1.00\\/1kg","image_url":"https:\\/\\/assets.iceland.co.uk\\/i\\/iceland\\/Reggia_1kg_Spaghetti_Pasta_63445.jpg?$producttile$"},{"name":"Batchelors Pasta \'n\' Sauce Cheese & Broccoli 99g","url":"https:\\/\\/www.iceland.co.uk\\/p\\/batchelors-pasta-n-sauce-cheese-and-broccoli-99g\\/58040.html","price":"0.80","price_per_unit":"8.08\\/1kg","image_url":"https:\\/\\/assets.iceland.co.uk\\/i\\/iceland\\/batchelors_pasta_n_sauce_cheese_broccoli_99g_58040_T5.jpg?$producttile$"},{"name":"Pot Noodle Original Curry Standard 90g","url":"https:\\/\\/www.iceland.co.uk\\/p\\/pot-noodle-original-curry-standard-90g\\/40880.html","price":"1.00","price_per_unit":"11.11\\/1kg","image_url":"https:\\/\\/assets.iceland.co.uk\\/i\\/iceland\\/Pot_Noodle_90gm_Curry_Pot_40880.jpg?$producttile$"},{"name":"Pasta Reggia Fusilli 1kg","url":"https:\\/\\/www.iceland.co.uk\\/p\\/pasta-reggia-fusilli-1kg\\/63444.html","price":"1.00","price_per_unit":"1.00\\/1kg","image_url":"https:\\/\\/assets.iceland.co.uk\\/i\\/iceland\\/Reggia_1kg_Fusilli_Pasta_63444.jpg?$producttile$"},{"name":"Dolmio Bolognese Onion and Garlic Pasta Sauce 500g","url":"https:\\/\\/www.iceland.co.uk\\/p\\/dolmio-bolognese-onion-and-garlic-pasta-sauce-500g\\/37288.html","price":"1.70","price_per_unit":"34p\\/100g","image_url":"https:\\/\\/assets.iceland.co.uk\\/i\\/iceland\\/Dolmio_500g_Intense_Garlic_37288.jpg?$producttile$"},{"name":"Branston Baked Beans in a Rich and Tasty Tomato Sauce 4 x 410g","url":"https:\\/\\/www.iceland.co.uk\\/p\\/branston-baked-beans-in-a-rich-and-tasty-tomato-sauce-4-x-410g\\/55372.html","price":"1.50","price_per_unit":"91p\\/1kg","image_url":"https:\\/\\/assets.iceland.co.uk\\/i\\/iceland\\/Branston_4_X4_Beans_55372.jpg?$producttile$"},{"name":"Dolmio Lasagne Creamy White Sauce 470g","url":"https:\\/\\/www.iceland.co.uk\\/p\\/dolmio-lasagne-creamy-white-sauce-470g\\/28118.html","price":"1.70","price_per_unit":"36p\\/100g","image_url":"https:\\/\\/assets.iceland.co.uk\\/i\\/iceland\\/dolmio_lasagne_creamy_white_sauce_470g_28118_T1.jpg?$producttile$"},{"name":"Pasta Reggia Durum Semolina Pasta 1kg","url":"https:\\/\\/www.iceland.co.uk\\/p\\/pasta-reggia-durum-semolina-pasta-1kg\\/63443.html","price":"1.00","price_per_unit":"1.00\\/1kg","image_url":"https:\\/\\/assets.iceland.co.uk\\/i\\/iceland\\/Reggia_1kg_Penne_Pasta_63443.jpg?$producttile$"},{"name":"Dolmio Bolognese Pasta Sauce 500g","url":"https:\\/\\/www.iceland.co.uk\\/p\\/dolmio-bolognese-pasta-sauce-500g\\/3447.html","price":"1.70","price_per_unit":"34p\\/100g","image_url":"https:\\/\\/assets.iceland.co.uk\\/i\\/iceland\\/dolmio_bolognese_pasta_sauce_500g_3447_T517.jpg?$producttile$"},{"name":"Napolina Five Cheese Tortellini Egg Pasta 400g","url":"https:\\/\\/www.iceland.co.uk\\/p\\/napolina-five-cheese-tortellini-egg-pasta-400g\\/78602.html","price":"1.75","price_per_unit":"4.38\\/1kg","image_url":"https:\\/\\/assets.iceland.co.uk\\/i\\/iceland\\/napolina_five_cheese_tortellini_egg_pasta_400g_78602_T1.jpg?$producttile$"}]},{"id":5,"name":"morrisons","listings":[{"name":"Morrisons Free From Fusilli 500g","url":"https:\\/\\/groceries.morrisons.com\\/products\\/morrisons-free-from-fusilli-115683011","price":"0.60","price_per_unit":"1.20\\/kg","image_url":"https:\\/\\/groceries.morrisons.com\\/productImages\\/115\\/115683011_0_150x150.jpg?identifier=880b06c864fc72579e1cf9876cb26806"},{"name":"Napolina Fusilli 500g","url":"https:\\/\\/groceries.morrisons.com\\/products\\/napolina-fusilli-214994011","price":"1","price_per_unit":"2.00\\/kg","image_url":"https:\\/\\/groceries.morrisons.com\\/productImages\\/214\\/214994011_0_150x150.jpg?identifier=560bb2a3308f55e7ac4a02e2d9a7bafb"},{"name":"Morrisons Wholewheat Fusiili 500g","url":"https:\\/\\/groceries.morrisons.com\\/products\\/morrisons-wholewheat-fusiili-209572011","price":"0.55","price_per_unit":"1.10\\/kg","image_url":"https:\\/\\/groceries.morrisons.com\\/productImages\\/209\\/209572011_0_150x150.jpg?identifier=07edf5dc2e0ee269d4ed50f283729c97"},{"name":"Morrisons Fusilli 3kg","url":"https:\\/\\/groceries.morrisons.com\\/products\\/morrisons-fusilli-215025011","price":"2.90","price_per_unit":"96.7p\\/kg","image_url":"https:\\/\\/groceries.morrisons.com\\/productImages\\/215\\/215025011_0_150x150.jpg?identifier=ca55f96573a6dfeab7c060dc1535a281"},{"name":"Napolina Wholewheat Fusilli 500g","url":"https:\\/\\/groceries.morrisons.com\\/products\\/napolina-wholewheat-fusilli-114196011","price":"1.35","price_per_unit":"2.70\\/kg","image_url":"https:\\/\\/groceries.morrisons.com\\/productImages\\/114\\/114196011_0_150x150.jpg?identifier=ac6e2c451cf348c6cc8dae4a9e97beed"},{"name":"Morrisons The Best Fusilli Gigante 500g","url":"https:\\/\\/groceries.morrisons.com\\/products\\/morrisons-the-best-fusilli-gigante-347715011","price":"1.70","price_per_unit":"3.40\\/kg","image_url":"https:\\/\\/groceries.morrisons.com\\/productImages\\/347\\/347715011_0_150x150.jpg?identifier=bcb867af066076813dcee3e199d4cdd2"},{"name":"Morrisons The Best Trottole Pasta 500g","url":"https:\\/\\/groceries.morrisons.com\\/products\\/morrisons-the-best-trottole-pasta-372760011","price":"1.75","price_per_unit":"3.50\\/kg","image_url":"https:\\/\\/groceries.morrisons.com\\/productImages\\/372\\/372760011_0_150x150.jpg?identifier=617656667739cbae15ec6cf602312b2b"},{"name":"Morrisons The Best Fusillta Casareccia Pasta 500g","url":"https:\\/\\/groceries.morrisons.com\\/products\\/morrisons-the-best-fusillta-casareccia-pasta-372758011","price":"1.75","price_per_unit":"3.50\\/kg","image_url":"https:\\/\\/groceries.morrisons.com\\/productImages\\/372\\/372758011_0_150x150.jpg?identifier=1d5ac1d44e148e3cf6d19a05bdd5064f"},{"name":"Morrisons Wholefoods Vegetable Mix with Pasta 500g","url":"https:\\/\\/groceries.morrisons.com\\/products\\/morrisons-wholefoods-vegetable-mix-with-pasta-215689011","price":"0.70","price_per_unit":"1.40\\/kg","image_url":"https:\\/\\/groceries.morrisons.com\\/productImages\\/215\\/215689011_0_150x150.jpg?identifier=b190f75c4ddcf904cd0ca908dc82cb4b"},{"name":"Napolina Fusilli Bronze Die Pasta 500g","url":"https:\\/\\/groceries.morrisons.com\\/products\\/napolina-fusilli-bronze-die-pasta-276179011","price":"1.88","price_per_unit":"3.76\\/kg","image_url":"https:\\/\\/groceries.morrisons.com\\/productImages\\/276\\/276179011_0_150x150.jpg?identifier=736e08685a1c7ae206c1f99c69a1e029"}]},{"id":6,"name":"sainsburys","listings":[{"name":"Why not try Sainsbury\'s Pomodoro Sauce, Taste the Difference 350g","url":"https:\\/\\/www.sainsburys.co.uk\\/shop\\/gb\\/groceries\\/product\\/details\\/sainsburys-pomodoro-sauce--taste-the-difference-350g","price":"2.00\\/unit","price_per_unit":"5.71\\/kg","image_url":"https:\\/\\/www.sainsburys.co.uk\\/wcsstore7.46hf.15\\/ExtendedSitesCatalogAssetStore\\/images\\/catalog\\/productImages\\/66\\/0000001745566\\/0000001745566_L.jpeg"},{"name":"Why not try Batchelors Pasta \'n\' Sauce, Cheese & Broccoli 99g","url":"https:\\/\\/www.sainsburys.co.uk\\/shop\\/gb\\/groceries\\/product\\/details\\/batchelors-pasta---sauce--cheese---broccoli-123g","price":"1.05\\/unit","price_per_unit":"10.61\\/kg","image_url":"https:\\/\\/www.sainsburys.co.uk\\/wcsstore7.46hf.15\\/ExtendedSitesCatalogAssetStore\\/images\\/catalog\\/productImages\\/09\\/5000354404009\\/5000354404009_L.jpeg"},{"name":"Sainsbury\'s Fusilli 1kg","url":"https:\\/\\/www.sainsburys.co.uk\\/shop\\/gb\\/groceries\\/product\\/details\\/sainsburys-fusilli-1kg","price":"1.10\\/unit","price_per_unit":"1.10\\/kg","image_url":"https:\\/\\/www.sainsburys.co.uk\\/wcsstore7.46hf.15\\/ExtendedSitesCatalogAssetStore\\/images\\/catalog\\/productImages\\/93\\/0000000490993\\/0000000490993_L.jpeg"},{"name":"Sainsbury\'s Penne 1kg","url":"https:\\/\\/www.sainsburys.co.uk\\/shop\\/gb\\/groceries\\/product\\/details\\/sainsburys-penne-rigate--italian-1kg","price":"1.10\\/unit","price_per_unit":"1.10\\/kg","image_url":"https:\\/\\/www.sainsburys.co.uk\\/wcsstore7.46hf.15\\/ExtendedSitesCatalogAssetStore\\/images\\/catalog\\/productImages\\/57\\/0000000536257\\/0000000536257_L.jpeg"},{"name":"Napolina Spaghetti 500g","url":"https:\\/\\/www.sainsburys.co.uk\\/shop\\/gb\\/groceries\\/product\\/details\\/napolina-spaghetti-500g","price":"1.30\\/unit","price_per_unit":"2.60\\/kg","image_url":"https:\\/\\/www.sainsburys.co.uk\\/wcsstore7.46hf.15\\/ExtendedSitesCatalogAssetStore\\/images\\/catalog\\/productImages\\/72\\/5000184592372\\/5000184592372_L.jpeg"},{"name":"Sainsbury\'s Fresh Gnocchi 500g","url":"https:\\/\\/www.sainsburys.co.uk\\/shop\\/gb\\/groceries\\/product\\/details\\/sainsburys-fresh-gnocchi-500g","price":"1.70\\/unit","price_per_unit":"3.40\\/kg","image_url":"https:\\/\\/www.sainsburys.co.uk\\/wcsstore7.46hf.15\\/ExtendedSitesCatalogAssetStore\\/images\\/catalog\\/productImages\\/86\\/0000000636186\\/0000000636186_L.jpeg"},{"name":"Sainsbury\'s Fresh Egg Fusilli 500g","url":"https:\\/\\/www.sainsburys.co.uk\\/shop\\/gb\\/groceries\\/product\\/details\\/sainsburys-fresh-egg-fusilli-500g","price":"1.70\\/unit","price_per_unit":"3.40\\/kg","image_url":"https:\\/\\/www.sainsburys.co.uk\\/wcsstore7.46hf.15\\/ExtendedSitesCatalogAssetStore\\/images\\/catalog\\/productImages\\/58\\/0000001143058\\/0000001143058_L.jpeg"},{"name":"Sainsbury\'s Fusilli 500g","url":"https:\\/\\/www.sainsburys.co.uk\\/shop\\/gb\\/groceries\\/product\\/details\\/sainsburys-fusilli--italian-500g","price":"0.60","price_per_unit":"1.20\\/kg","image_url":"https:\\/\\/www.sainsburys.co.uk\\/wcsstore7.46hf.15\\/ExtendedSitesCatalogAssetStore\\/images\\/catalog\\/productImages\\/18\\/0000000321518\\/0000000321518_L.jpeg"},{"name":"Sainsbury\'s Fresh Egg Penne 500g","url":"https:\\/\\/www.sainsburys.co.uk\\/shop\\/gb\\/groceries\\/product\\/details\\/sainsburys-fresh-penne-pasta-500g","price":"1.70\\/unit","price_per_unit":"3.40\\/kg","image_url":"https:\\/\\/www.sainsburys.co.uk\\/wcsstore7.46hf.15\\/ExtendedSitesCatalogAssetStore\\/images\\/catalog\\/productImages\\/94\\/0000000636094\\/0000000636094_L.jpeg"},{"name":"Sainsbury\'s Linguine 500g","url":"https:\\/\\/www.sainsburys.co.uk\\/shop\\/gb\\/groceries\\/product\\/details\\/sainsburys-linguine-500g","price":"0.60","price_per_unit":"1.20\\/kg","image_url":"https:\\/\\/www.sainsburys.co.uk\\/wcsstore7.46hf.15\\/ExtendedSitesCatalogAssetStore\\/images\\/catalog\\/productImages\\/24\\/0000000579124\\/0000000579124_L.jpeg"}]},{"id":7,"name":"tesco","listings":[{"name":"Tesco Penne Pasta Quills 500G","url":null,"price":"0.53","price_per_unit":"1.06\\/kg","image_url":"https:\\/\\/img.tesco.com\\/Groceries\\/pi\\/845\\/5000119319845\\/IDShot_225x225.jpg"},{"name":"Tesco Penne 300G","url":null,"price":"1.25","price_per_unit":"4.17\\/kg","image_url":"https:\\/\\/img.tesco.com\\/Groceries\\/pi\\/937\\/5057545806937\\/IDShot_225x225.jpg"},{"name":"Tesco Short Spaghetti Pasta 500G","url":null,"price":"0.53","price_per_unit":"1.06\\/kg","image_url":"https:\\/\\/img.tesco.com\\/Groceries\\/pi\\/182\\/5000119117182\\/IDShot_225x225.jpg"},{"name":"Hearty Food Co. Spaghetti Pasta 500G","url":null,"price":"0.20","price_per_unit":"0.40\\/kg","image_url":"https:\\/\\/img.tesco.com\\/Groceries\\/pi\\/514\\/5057545092514\\/IDShot_225x225.jpg"},{"name":"Tesco Whole Wheat Fusilli Pasta 500G","url":null,"price":"0.53","price_per_unit":"1.06\\/kg","image_url":"https:\\/\\/img.tesco.com\\/Groceries\\/pi\\/906\\/5000119319906\\/IDShot_225x225.jpg"},{"name":"Tesco Fusilli Pasta Twists 1Kg","url":null,"price":null,"price_per_unit":null,"image_url":"https:\\/\\/img.tesco.com\\/Groceries\\/pi\\/305\\/5000119532305\\/IDShot_225x225.jpg"},{"name":"Tesco Fusilli 300G","url":null,"price":"1.25","price_per_unit":"0.42\\/100g","image_url":"https:\\/\\/img.tesco.com\\/Groceries\\/pi\\/579\\/5057753722579\\/IDShot_225x225.jpg"},{"name":"Napolina Fusilli Pasta 500G","url":null,"price":"1.28","price_per_unit":"2.56\\/kg","image_url":"https:\\/\\/img.tesco.com\\/Groceries\\/pi\\/402\\/5000184592402\\/IDShot_225x225.jpg"},{"name":"Napolina Fusilli Pasta 1Kg","url":null,"price":"2.28","price_per_unit":"2.28\\/kg","image_url":"https:\\/\\/img.tesco.com\\/Groceries\\/pi\\/458\\/5000232823458\\/IDShot_225x225.jpg"},{"name":"Napolina Penne Pasta 1Kg","url":null,"price":"2.28","price_per_unit":"2.28\\/kg","image_url":"https:\\/\\/img.tesco.com\\/Groceries\\/pi\\/397\\/5000232823397\\/IDShot_225x225.jpg"}]}]';

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
    this.results = JSON.parse(jsonData);
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
