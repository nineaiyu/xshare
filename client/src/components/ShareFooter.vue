<template>
  <div class="footer">
    <el-link :underline="false"> {{ footer.copyright }}</el-link>
    &bull;
    <el-link :href="footer.ipcBeiAn.url" :underline="false" rel="nofollow noopener"
             target="_blank">{{ footer.ipcBeiAn.text }}
    </el-link>
    &bull;
    <el-link :href="footer.gongAnBeiAn.url" :underline="false">
      <i :style="{background:`url(${beianLogo})  0 0/100%`,width:'20px',height:'20px'}"/>{{ footer.gongAnBeiAn.text }}
    </el-link>
  </div>
</template>

<script>
const footer = process.env.base_env.footer
export default {
  name: "ShareFooter",
  data() {
    return {
      footer,
      beianLogo: require('@/assets/beianlogo.png')
    }
  }
}
</script>

<style scoped>
.footer {
  text-align: center;
}
</style>
