<template>
  <div :style="{minHeight:minHeight+'px'}">
    <ShareHeader v-if="showHeader"></ShareHeader>
    <div v-else style="margin-top: 60px"></div>
    <div class="v_body">
      <router-view></router-view>
    </div>
  </div>
  <share-footer></share-footer>
</template>

<script>
import ShareHeader from "@/components/ShareHeader";
import ShareFooter from "@/components/ShareFooter";
import {getAccessToken} from "@/utils/auth";

export default {
  name: 'App',
  components: {
    ShareHeader,
    ShareFooter
  },
  data() {
    return {
      minHeight: 0,
      showHeader: true
    }
  }, mounted() {
    this.minHeight = document.documentElement.clientHeight - 30
    let that = this
    window.onresize = function () {
      that.minHeight = document.documentElement.clientHeight - 30
    }
    this.setHeader(this.$route)
  }, watch: {
    $route: {
      handler: function (route) {
        this.setHeader(route)
      }
    }
  }, methods: {
    setHeader(route) {
      if (route.name === 'short' && !getAccessToken()) {
        this.showHeader = false
      }
    }
  }
}
</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  /*margin-top: 60px;*/
}

.v_body {
  width: 1200px;
  margin: 20px auto
}

.filter-container {
  padding-bottom: 10px;

  .filter-item {
    //display: inline-block;
    vertical-align: middle;
    margin-bottom: 10px;
    padding-right: 5px;
  }
}

.el-table .warning-row {
  --el-table-tr-bg-color: var(--el-color-warning-light-9);
}

.el-table .success-row {
  --el-table-tr-bg-color: var(--el-color-success-light-9);
}
</style>
