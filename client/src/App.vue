<template>
  <div :style="{minHeight:minHeight+'px'}">
    <ShareHeader></ShareHeader>
    <div class="v_body">
      <router-view></router-view>
    </div>
  </div>
  <share-footer></share-footer>
</template>

<script>
import ShareHeader from "@/components/ShareHeader";
import ShareFooter from "@/components/ShareFooter";

export default {
  name: 'App',
  components: {
    ShareHeader,
    ShareFooter
  },
  data() {
    return {
      minHeight: 0,
    }
  }, mounted() {
    this.minHeight = document.documentElement.clientHeight - 30
    let that = this
    window.onresize = function () {
      that.minHeight = document.documentElement.clientHeight - 30
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
  background-image: linear-gradient(to bottom, #e8f3ee 0%, #ebecee 100%);
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
