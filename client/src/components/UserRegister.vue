<template>
  <div class="login-container">
    <el-form ref="loginForm" :model="loginForm" :rules="loginRules" autocomplete="on" class="login-form"
             label-position="left" size="large">

      <div class="title-container">
        <h3 class="title">Xshare</h3>
      </div>

      <el-form-item prop="username">
        <el-input
            ref="username"
            v-model="loginForm.username"
            autocomplete="on"
            name="username"
            placeholder="Username"
            prefix-icon="User"
            tabindex="1"
            type="text"
        />
      </el-form-item>

      <el-tooltip :visible="capsTooltip" content="Caps lock is On" manual placement="right">
        <el-form-item prop="password">
          <el-input
              :key="passwordType"
              ref="password"
              v-model="loginForm.password"
              :type="passwordType"
              autocomplete="on"
              name="password"
              placeholder="Password"
              prefix-icon="Lock"
              show-password
              tabindex="2"
              @blur="capsTooltip = false"
              @keyup="checkCapslock"
              @keyup.enter="handleRegister"
          />
        </el-form-item>
      </el-tooltip>

      <el-button :loading="loading" plain style="width:100%;margin-bottom:30px;" type="success"
                 @click.prevent="handleRegister">
        注册并登录
      </el-button>
      <el-link :underline="false" style="float: right" @click="$router.push({name:'login'})">直接登录</el-link>
    </el-form>
  </div>
</template>

<script>
import {userinfoStore} from "@/store";
import {mapActions} from "pinia/dist/pinia";
import {getToken} from "@/api/user";
import FingerprintJS from '@fingerprintjs/fingerprintjs'

export default {
  name: "UserRegister",
  components: {},
  data() {
    const validateUsername = (rule, value, callback) => {
      if (value.length < 6) {
        callback(new Error('The username can not be less than 6 digits'))
      } else {
        callback()
      }
    }
    const validatePassword = (rule, value, callback) => {
      if (value.length < 6) {
        callback(new Error('The password can not be less than 6 digits'))
      } else {
        callback()
      }
    }
    return {
      loginForm: {
        username: '',
        password: ''
      },
      loginRules: {
        username: [{required: true, trigger: 'blur', validator: validateUsername}],
        password: [{required: true, trigger: 'blur', validator: validatePassword}]
      },
      passwordType: 'password',
      capsTooltip: false,
      loading: false,
      otherQuery: {},
      loginData: {},
      client_id: '',
    }
  }, methods: {
    // 获取浏览器的唯一标识符
    createFingerprint() {
      const fpPromise = FingerprintJS.load()
      fpPromise.then(fp => {
        fp.get().then(res => {
          this.client_id = res.visitorId
          getToken({client_id: res.visitorId}).then(res => {
            this.loginData = res.data
            this.loginData.client_id = this.client_id
          })
        })
      })
    },

    checkCapslock(e) {
      const {key} = e
      this.capsTooltip = key && key.length === 1 && (key >= 'A' && key <= 'Z')
    }, handleRegister() {
      this.loading = true
      this.register(this.loginForm, this.loginData).then(() => {
        this.$router.push({path: this.redirect || '/', query: this.otherQuery})
        this.loading = false
      }).catch(() => {
        this.loading = false
      })
    }, getOtherQuery(query) {
      return Object.keys(query).reduce((acc, cur) => {
        if (cur !== 'redirect') {
          acc[cur] = query[cur]
        }
        return acc
      }, {})
    },
    ...mapActions(userinfoStore, ['register'])
  }, watch: {
    $route: {
      handler: function (route) {
        const query = route.query
        if (query) {
          this.redirect = query.redirect
          this.otherQuery = this.getOtherQuery(query)
        }
      },
      immediate: true
    }
  }, mounted() {
    this.createFingerprint()
  }
}
</script>

<style lang="scss">
$bg: #ffffff;
$light_gray: #1291ef;

.login-container {
  min-height: 100%;
  width: 100%;
  overflow: hidden;

  .login-form {
    position: relative;
    width: 520px;
    max-width: 100%;
    padding: 160px 35px 0;
    margin: 0 auto;
    overflow: hidden;
  }


  .title-container {
    position: relative;

    .title {
      font-size: 26px;
      color: $light_gray;
      margin: 0 auto 40px auto;
      text-align: center;
      font-weight: bold;
    }
  }

}
</style>
