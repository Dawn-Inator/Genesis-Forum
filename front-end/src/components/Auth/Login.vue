<template>
  <div class="container">

        <div class="row justify-content-center">
          <div class="col-md-6 title-background">

          </div>
        </div>

    <!-- 登录表单居中显示 -->
    <div class="row justify-content-center">

      <div class="col-md-6">
        <form @submit.prevent="onSubmit" class="shadow p-4 rounded">
          <div class="form-group" v-bind:class="{'has-error': loginForm.usernameError}">
            <label for="username">{{ $t('auth.login.username') }}</label>
            <input type="text" v-model="loginForm.username" class="form-control" id="username" placeholder="">
            <small class="text-danger" v-show="loginForm.usernameError">{{ loginForm.usernameError }}</small>
          </div>
          <div class="form-group" v-bind:class="{'has-error': loginForm.passwordError}">
            <label for="password">{{ $t('auth.login.password') }}</label>
            <input type="password" v-model="loginForm.password" class="form-control" id="password" placeholder="">
            <small class="text-danger" v-show="loginForm.passwordError">{{ loginForm.passwordError }}</small>
          </div>

          <div class="cf-turnstile" data-sitekey="0x4AAAAAAAWIZbWOBsTyF9ID" data-callback="javascriptCallback"></div>

          <div class="text-center" v-if="cf_token">
            <button type="submit" class="btn btn-primary">{{ $t('auth.login.sign-in') }}</button>
          </div>



        </form>
      </div>
    </div>

    <!-- 链接居中显示 -->
    <div class="row justify-content-center mt-4">
      <div class="col-md-8 text-center">
        <p>{{ $t('auth.login.new-user') }} <router-link to="/register" style="color: blue;">{{ $t('auth.login.click-register') }}</router-link></p>
        <p>
          {{ $t('auth.login.forgot-pass') }}
          <router-link v-bind:to="{ name: 'ResetPasswordRequest' }" style="color: blue;">{{ $t('auth.login.click-reset') }}</router-link>
        </p>
      </div>
    </div>

    </div>

  </div>
</template>

<style scoped>

.cf-turnstile{
  display: grid;
  place-items: center; /* 这会同时处理水平和垂直居中 */
  height: 100px;
}

.title-background {
  background-image: url('~@/assets/Dark-Night.png');
  background-size: cover; /* 或者 'contain' 根据实际效果选择 */
  background-repeat: no-repeat;
  background-position: center;
  padding: 20px;
  margin-bottom: 20px; /* 与表单间隔 */
  min-height: 300px; /* 最小高度，根据背景图片内容调整 */
  display: flex;
  justify-content: center;
  align-items: center; /* 使文本垂直居中 */
}

.link-button {
  display: inline-block;
  background-color: #007bff;
  color: white;
  padding: 10px 20px;
  border-radius: 5px;
  text-decoration: none;
  transition: background-color 0.3s ease;
}

.link-button:hover, .link-button:focus {
  background-color: #0056b3;
  color: white;
  text-decoration: none;
}

.text-accent {
  color: #007bff; /* 调整为你喜欢的颜色 */
}

/* 可选：如果你想要特别突出“忘记密码”链接 */
.forgot-password-link {
  color: #dc3545; /* Bootstrap的危险颜色 */
}

.forgot-password-link:hover {
  color: #c82333; /* 深一点的红色 */
}

.login-background {
  background: url('../../assets/The-Earth-BG.png') no-repeat center center fixed;
  background-size: cover;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

.login-form {
  background-color: rgba(255, 255, 255, 0.8); /* 给表单添加半透明的白色背景 */
  border-radius: 15px; /* 可选：为表单添加圆角 */
  margin-top: -100px; /* 根据需要调整，确保表单在视窗中垂直居中 */
}

</style>


<script>
import store from '../../store'

export default {
  name: 'Login',  //this is the name of the component
  data () {
    return {
      cf_token: '',
      sharedState: store.state,
      loginForm: {
        username: '',
        password: '',
        errors: 0,  // 表单是否在前端验证通过，0 表示没有错误，验证通过
        usernameError: null,
        passwordError: null
      }
    }
  },
  methods: {
    onSubmit (e) {
      this.loginForm.errors = 0  // 重置

      if (!this.loginForm.username) {
        this.loginForm.errors++
        this.loginForm.usernameError = 'Username required.'
      } else {
        this.loginForm.usernameError = null
      }

      if (!this.loginForm.password) {
        this.loginForm.errors++
        this.loginForm.passwordError = 'Password required.'
      } else {
        this.loginForm.passwordError = null
      }

      if (this.loginForm.errors > 0) {
        // 表单验证没通过时，不继续往下执行，即不会通过 axios 调用后端API
        return false
      }

      const path = '/api/tokens'
      // axios 实现Basic Auth需要在config中设置 auth 这个属性即可
      this.$axios.post(path, {}, {
        auth: {
          'username': this.loginForm.username,
          'password': this.loginForm.password
        }
      }).then((response) => {
          // handle success
          window.localStorage.setItem('madblog-token', response.data.token)
          store.loginAction()

          this.$toasted.success(`Welcome ${this.sharedState.user_name}!`, { icon: 'fingerprint' })

          if (typeof this.$route.query.redirect == 'undefined') {
            this.$router.push('/')
          } else {
            this.$router.push(this.$route.query.redirect)
          }
        })
        .catch((error) => {
          // handle error
          // console.log('failed', error.response);
          if (typeof error.response != 'undefined') {
            if (error.response.status == 401) {
              this.loginForm.usernameError = 'Invalid username or password.'
              this.loginForm.passwordError = 'Invalid username or password.'
            } else {
              console.log(error.response)
            }
          }
        })
    }
  },
  mounted() {
    window.onloadTurnstileCallback = function () {
        turnstile.render('#cf-turnstile', {
            sitekey: '0x4AAAAAAAWIZbWOBsTyF9ID',
            callback: function(token) {
                console.log(`Challenge Success ${token}`);
                this.cf_token=token
            },
        });
    };

    if (typeof turnstile !== 'undefined') {
        window.onloadTurnstileCallback(); // 如果 turnstile 已加载，立即调用
      }
  }
}
</script>
