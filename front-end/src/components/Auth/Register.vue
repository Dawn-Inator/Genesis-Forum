<template>
  <div class="container mt-5">
    <!-- 标题居中显示 -->
    <div class="row justify-content-center">
      <div class="col-md-8">
        <h1 class="text-center display-4 text-primary my-5">Welcome to Genesis Forum !!</h1>
      </div>
    </div>
    <div class="row justify-content-center">
      <div class="col-md-6">
        <form @submit.prevent="onSubmit" class="p-5 shadow rounded">
          <div class="form-group" v-bind:class="{'has-error': registerForm.usernameError}">
            <label for="username">Username</label>
            <input type="text" v-model="registerForm.username" class="form-control" id="username" placeholder="Enter username">
            <small class="form-control-feedback text-danger" v-show="registerForm.usernameError">{{ registerForm.usernameError }}</small>
          </div>
          <div class="form-group" v-bind:class="{'has-error': registerForm.emailError}">
            <label for="email">Email address</label>
            <input type="email" v-model="registerForm.email" class="form-control" id="email" aria-describedby="emailHelp" placeholder="Enter email">
            <small v-if="!registerForm.emailError" id="emailHelp" class="form-text text-muted">We'll never share your email with anyone else.</small>
            <small class="form-control-feedback text-danger" v-show="registerForm.emailError">{{ registerForm.emailError }}</small>
          </div>
          <div class="form-group" v-bind:class="{'has-error': registerForm.passwordError}">
            <label for="password">Password</label>
            <input type="password" v-model="registerForm.password" class="form-control" id="password" placeholder="Password">
            <small class="form-control-feedback text-danger" v-show="registerForm.passwordError">{{ registerForm.passwordError }}</small>
          </div>
          <!-- Register Form Structure (Keep the same) -->
          <div class="container">
            <div class="row justify-content-center"> <!-- Added justify-content-center -->
              <div class="col-md-6"> <!-- Adjusted column size for better alignment -->
                <form @submit.prevent="onSubmit">
                  <!-- Form fields -->
                  <button type="submit" class="btn btn-primary mt-3 w-100">Register</button> <!-- Added w-100 for full width -->
                </form>
              </div>
            </div>
          </div>

        </form>
      </div>
    </div>
  </div>
</template>


<style scoped>

.row.justify-content-center {
  display: flex;
  justify-content: center; /* Flex container for center alignment */
}



.btn-primary {
  background-image: linear-gradient(to right, #4a90e2, #007bff); /* 渐变背景色 */
  border: none;
  color: #fff; /* 按钮文字颜色 */
  padding: 0.5rem 1.5rem; /* 按钮内边距调整 */
  transition: transform 0.3s ease, box-shadow 0.3s ease; /* 过渡动画 */
  display: inline-block; /* 使transition生效 */
  border-radius: 20px; /* 圆角边框 */
  width: auto; /* Override width if necessary */
  margin: 0 auto; /* Auto margins for horizontal centering */
}

.btn-primary:hover, .btn-primary:focus {
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2); /* 鼠标悬停时添加阴影 */
  background-image: linear-gradient(to right, #007bff, #4a90e2); /* 渐变背景色变化 */
}

.w-50 {
  width: 100%;
}

.text-danger {
  color: #e3342f;
}

.has-error input {
  border-color: #e3342f; /* 错误颜色 */
}

.form-control-feedback {
  display: block;
}

.shadow {
  box-shadow: 0 .5rem 1rem rgba(0,0,0,.15);
}

.rounded {
  border-radius: .25rem;
}

p-5 {
  padding: 3rem !important;
}

.text-center {
  text-align: center;
}

.mb-4 {
  margin-bottom: 1.5rem;
}

.mt-5 {
  margin-top: 3rem;
}

.btn-primary {
  background-color: #007bff;
  border: none;
}

.w-100 {
  width: 100%;
}

.text-danger {
  color: #e3342f;
}
</style>



<script>
export default {
  name: 'Register', //this is the name of the component
  data () {
    return {
      registerForm: {
        username: '',
        email: '',
        password: '',
        errors: 0,  // 表单是否在前端验证通过，0 表示没有错误，验证通过
        usernameError: null,
        emailError: null,
        passwordError: null
      }
    }
  },
  methods: {
    onSubmit (e) {
      this.registerForm.errors = 0  // 重置

      if (!this.registerForm.username) {
        this.registerForm.errors++
        this.registerForm.usernameError = 'Username required.'
      } else {
        this.registerForm.usernameError = null
      }

      if (!this.registerForm.email) {
        this.registerForm.errors++
        this.registerForm.emailError = 'Email required.'
      } else if (!this.validEmail(this.registerForm.email)) {
        this.registerForm.errors++
        this.registerForm.emailError = 'Valid email required.'
      } else {
        this.registerForm.emailError = null
      }

      if (!this.registerForm.password) {
        this.registerForm.errors++
        this.registerForm.passwordError = 'Password required.'
      } else {
        this.registerForm.passwordError = null
      }

      if (this.registerForm.errors > 0) {
        // 表单验证没通过时，不继续往下执行，即不会通过 axios 调用后端API
        return false
      }

      const path = '/api/users'
      const payload = {
        confirm_email_base_url: window.location.href.split('/', 4).join('/') + '/unconfirmed/?token=',
        username: this.registerForm.username,
        email: this.registerForm.email,
        password: this.registerForm.password
      }
      this.$axios.post(path, payload)
        .then((response) => {
          // handle success
          this.$toasted.success('A confirmation email has been sent to you by email.', { icon: 'fingerprint' })
          this.$router.push('/login')
        })
        .catch((error) => {
          // handle error
          for (var field in error.response.data.message) {
            if (field == 'username') {
              this.registerForm.usernameError = error.response.data.message.username
            } else if (field == 'email') {
              this.registerForm.emailError = error.response.data.message.email
            } else if (field == 'password') {
              this.registerForm.passwordError = error.response.data.message.password
            }
          }
        })
    },
    validEmail: function (email) {
      var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
      return re.test(email);
    }
  }
}
</script>
