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
              @keyup.enter="handleLogin"
          />
        </el-form-item>
      </el-tooltip>

      <el-button :loading="loading" style="width:100%;margin-bottom:30px;" type="primary" @click.prevent="handleLogin">
        登录
      </el-button>
    </el-form>
  </div>
</template>

<script>
import {userinfoStore} from "@/store";
import {mapActions} from "pinia/dist/pinia";

export default {
  name: "UserLogin",
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
    }
  }, methods: {
    checkCapslock(e) {
      const {key} = e
      this.capsTooltip = key && key.length === 1 && (key >= 'A' && key <= 'Z')
    }, handleLogin() {
      console.log('login')
      this.loading = true
      // eslint-disable-next-line no-unused-vars
      this.login(this.loginForm).then(() => {
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
    ...mapActions(userinfoStore, ['login'])
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
  },
}
</script>

<style lang="scss">
$bg: #ffffff;
$light_gray: #1291ef;

.login-container {
  min-height: 100%;
  width: 100%;
  background-color: $bg;
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
