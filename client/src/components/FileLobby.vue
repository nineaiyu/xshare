<template>
  <div>
    <el-avatar :size="100" :src="url"/>
  </div>
  Lobby

</template>

<script>

import {createBase64} from "@/utils";

export default {
  name: "FileLobby",
  components: {},
  data() {

    return {
      url: ''
    }
  },
  mounted() {
    this.url = createBase64('X',)
  },
  methods: {}
}
</script>

<style scoped>

</style>
