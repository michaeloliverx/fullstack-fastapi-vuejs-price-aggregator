<template>
  <div class="app-container">
    <el-card class="box-card">
      <div
        slot="header"
        class="clearfix"
      >
        <span>Create a new role</span>
      </div>
      <el-form
        ref="loginForm"
        :model="createForm"
        :rules="createRules"
        autocomplete="on"
        label-position="left"
      >
        <el-form-item
          prop="name"
          label="Shop Name"
        >
          <el-input
            v-model="createForm.name"
            type="text"
          />
        </el-form-item>

        <el-form-item
          prop="baseUrl"
          label="Base URL"
        >
          <el-input
            v-model="createForm.baseUrl"
            type="text"
          />
        </el-form-item>

        <el-form-item
          prop="queryUrl"
          label="Query URL"
        >
          <el-input
            v-model="createForm.queryUrl"
            type="text"
          />
        </el-form-item>

        <el-form-item
          prop="renderJS"
          label="Render JavaScript"
        >
          <el-switch v-model="createForm.renderJS" />
        </el-form-item>

        <el-form-item
          prop="selectors"
          label="CSS Selectors"
        >
          <div class="editor-container">
            <json-editor
              ref="jsonEditor"
              v-model="createForm.selectorJson"
            />
          </div>
        </el-form-item>

        <el-button
          :loading="loading"
          type="primary"
          @click="handleCreate"
        >
          Create
        </el-button>

        <el-button
          @click="$router.back()"
        >
          Cancel
        </el-button>
      </el-form>
    </el-card>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { Form as ElForm, Input } from 'element-ui';
import JsonEditor from '@/components/JsonEditor/index.vue';

@Component({
  name: 'CreateShop',
  components: {
    JsonEditor
  }
})
export default class extends Vue {
  private loading = false;

  private createForm = {
    name: '',
    baseUrl: '',
    renderJS: false,
    queryUrl: '',
    selectorJson: {}
  };

  private createRules = {
    name: [{ trigger: 'blur', required: true, message: 'Please enter a name' }],
    baseUrl: [{ trigger: 'blur', required: true, message: 'Please enter the base URL' }],
    queryUrl: [{ trigger: 'blur', required: true, message: 'Please enter the query URL' }],
    selectorJson: [{ trigger: 'blur', required: true, message: 'Please add the CSS selector code' }]
  };

  mounted() {
    (this.$refs.name as Input).focus();
    (this.$refs.description as Input).focus();
  }

  private handleCreate() {
    (this.$refs.loginForm as ElForm).validate(async(valid: boolean) => {
      if (valid) {
        this.loading = true;
      } else {
        this.$message.error('validation failed');
      }
    });
  }
}
</script>

<style lang="scss" scoped>
.editor-container {
  position: relative;
  height: 100%;
}
.box-card {
  max-width: 60rem;
}
</style>
