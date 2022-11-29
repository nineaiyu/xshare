<template>
  <el-dialog v-model="showVisible" :close-on-click-modal="false" :title="videoTitle" center destroy-on-close draggable
             width="850px">
    <video-play
        :src="videoSrc"
        v-bind="videoOptions"
    />
  </el-dialog>
</template>

<script>
import 'vue3-video-play/dist/style.css'
import {videoPlay} from 'vue3-video-play'


export default {
  name: "PreviewVideo",
  data() {
    return {
      videoOptions: {
        width: "800px", //播放器高度
        height: "450px", //播放器高度
        color: "#409eff", //主题色
        title: "", //视频名称
        type: "m3u8",
        // src: "",
        muted: false, //静音
        webFullScreen: false,
        speedRate: ["0.75", "1.0", "1.25", "1.5", "2.0"], //播放倍速
        autoPlay: false, //自动播放
        loop: false, //循环播放
        mirror: false, //镜像画面
        lightOff: false, //关灯模式
        volume: 0.3, //默认音量大小
        control: true, //是否显示控制
        controlBtns: [
          "audioTrack",
          "speedRate",
          "volume",
          "setting",
          "pip",
          "pageFullScreen",
          "fullScreen",
        ], //显示所有按钮,
      },
    }
  },
  computed: {
    showVisible: {
      get() {
        return this.videoVisible
      },
      set(value) {
        this.$emit('update:videoVisible', value)
      }
    }
  },
  props: {
    videoVisible: {},
    videoTitle: {
      type: String,
      default: '',
    },
    videoSrc: {
      type: String,
      require: true,
    }
  }, methods: {}, watch: {}, components: {
    videoPlay
  }, mounted() {
  }
}
</script>

<style scoped>

</style>
