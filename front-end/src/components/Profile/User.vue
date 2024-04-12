<template>
  <section class="user-profile-section">
    <div class="container">
    <!-- Modal: Send Messages -->
    <div class="modal fade custom-modal" id="sendMessagesModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered modal-lg" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">群发私信</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">

            <form id="sendMessagesForm" @submit.prevent="onSubmitSendMessages" @reset.prevent="onResetSendMessages">
              <div class="form-group">
                <textarea v-model="sendMessagesForm.body" class="form-control" id="sendMessagesFormBody" rows="5" placeholder=" 内容"></textarea>
                <small class="form-control-feedback" v-show="sendMessagesForm.bodyError">{{ sendMessagesForm.bodyError }}</small>
              </div>
              <button type="reset" class="btn btn-secondary">Cancel</button>
              <button type="submit" class="btn btn-primary">Send</button>
            </form>

          </div>
        </div>
      </div>
    </div>
    <!-- End Modal: Send Messages -->

    <!-- 用户所有运行中的后台任务的进度 -->

      <alert
        v-for="(alert, index) in alerts" :key="index"
        v-bind:id="alert.id"
        v-bind:variant="alert.variant"
        v-bind:message="alert.message">
      </alert>


    <!-- 用户信息 -->
    <div v-if="user" class="user-info-box">
      <div class="g-brd-around g-brd-gray-light-v4 g-pa-20 g-mb-40">
        <div class="row">
          <div class="col-sm-3 g-mb-40 g-mb-0--lg">
            <!-- User Image -->
            <div class="g-mb-20">
              <div class="avatar-container">
                <a href="https://gravatar.com/" target="_blank">
                  <img v-if="user._links.avatar" class="img-fluid user-avatar" v-bind:src="user._links.avatar" v-bind:alt="user.name || user.username">
                </a>
              </div>
            </div>
            <!-- User Image -->

            <!-- Actions -->
            <button v-if="!user.is_following && $route.params.id != sharedState.user_id" v-on:click="onFollowUser($route.params.id)" class="btn btn-block u-btn-outline-primary g-rounded-50 g-py-12 g-mb-10">
              <i class="icon-user-follow g-pos-rel g-top-1 g-mr-5"></i> Follow
            </button>

            <button v-if="user.is_following && $route.params.id != sharedState.user_id" v-on:click="onUnfollowUser($route.params.id)" class="btn btn-block u-btn-outline-red g-rounded-50 g-py-12 g-mb-10">
              <i class="icon-user-unfollow g-pos-rel g-top-1 g-mr-5"></i> Unfollow
            </button>

            <router-link v-if="$route.params.id != sharedState.user_id" v-bind:to="{ name: 'MessagesHistoryResource', query: { from: $route.params.id } }" class="btn btn-block u-btn-outline-purple g-rounded-50 g-py-12 g-mb-10">
              <i class="icon-bubble g-pos-rel g-top-1 g-mr-5"></i> Send private message
            </router-link>

            <router-link v-if="$route.params.id == sharedState.user_id" v-bind:to="{ name: 'SettingProfile' }" class="btn btn-block u-btn-outline-primary g-rounded-50 g-py-12 g-mb-10">
              <i class="icon-settings g-pos-rel g-top-1 g-mr-5"></i> Settings
            </router-link>

            <button v-if="$route.params.id == sharedState.user_id && sharedState.user_perms.includes('admin')" data-toggle="modal" data-target="#sendMessagesModal" class="btn btn-block u-btn-outline-aqua g-rounded-50 g-py-12 g-mb-10">
              <i class="icon-bubble g-pos-rel g-top-1 g-mr-5"></i> Send Messages
            </button>

            <button v-if="$route.params.id == sharedState.user_id && sharedState.user_perms.includes('write')" v-on:click="onExportPosts()" class="btn btn-block u-btn-outline-purple g-rounded-50 g-py-12 g-mb-10">
              <i class="icon-cloud-download g-pos-rel g-top-1 g-mr-5"></i> Export posts
            </button>

            <button v-if="$route.params.id == sharedState.user_id" v-on:click="onDeleteUser($route.params.id)" class="btn btn-block u-btn-outline-red g-rounded-50 g-py-12 g-mb-10">
              <i class="icon-ban g-pos-rel g-top-1 g-mr-5"></i> Delete Your Account
            </button>
            <!-- End Actions -->

          </div>

          <div class="col-sm-9">

            <!-- Tab Nav -->
            <ul class="nav nav-tabs g-mb-20" >
              <li class="nav-item">
                <router-link v-bind:to="{ name: 'UserOverview' }" v-bind:active-class="'active'" class="nav-link" v-bind:class="isUserOverView" style="color: black;">Overview <span class="u-label g-font-size-11 g-bg-primary g-rounded-20 g-px-10"><i class="icon-layers g-pos-rel g-top-1 g-mr-8"></i></span></router-link>
              </li>
              <li class="nav-item">
                <router-link v-bind:to="{ name: 'UserFollowers' }" v-bind:active-class="'active'" class="nav-link">Followers <span class="u-label g-font-size-11 g-bg-deeporange g-rounded-20 g-px-10">{{ user.followers_count }}</span></router-link>
              </li>
              <li class="nav-item">
                <router-link v-bind:to="{ name: 'UserFollowing' }" v-bind:active-class="'active'" class="nav-link">Following <span class="u-label g-font-size-11 g-bg-aqua g-rounded-20 g-px-10">{{ user.followeds_count }}</span></router-link>
              </li>
              <li class="nav-item">
                <router-link v-bind:to="{ name: 'UserPosts' }" v-bind:active-class="'active'" class="nav-link" v-bind:class="{'active': $route.name == 'UserFollowingPosts'}">Posts <span class="u-label g-font-size-11 g-bg-purple g-rounded-20 g-px-10">{{ user.posts_count }}</span></router-link>
              </li>
            </ul>

            <!-- 嵌套的子路由出口 -->
            <router-view></router-view>

          </div>
        </div>
      </div>
    </div>

    </div>

    <div class="container">

      <div v-if="sharedState.is_authenticated && $route.params.id == sharedState.user_id && sharedState.user_perms.includes('write')" class="publish-new-post">
        <!-- Panel Header -->
        <div class="card-header d-flex align-items-center justify-content-between g-bg-gray-light-v5 border-0 g-mb-15">
          <h3 class="h6 mb-0 " style="font-size: 15px;">
            <i class="icon-fire g-pos-rel g-top-1 g-mr-5"></i> Welcome to Genesis Forum !!!
          </h3>

        </div>
        <!-- End Panel Header -->
      </div>

    </div>
  </section>
</template>

<style scoped>
.user-profile-section .custom-modal .modal-content {
  border-radius: 10px;
  box-shadow: 0 5px 15px rgba(0,0,0,.5);
}

.user-profile-section .user-info-box {
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0,0,0,.1);
  padding: 20px;
  margin-bottom: 20px;
}

.user-profile-section .user-info-box .btn {
  border-radius: 25px;
  padding: 10px 30px;
}

.user-profile-section .publish-new-post {
  background: #f9f9f9;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0,0,0,.1);
  margin-bottom: 20px;
}

.user-profile-section .publish-new-post .btn-primary {
  background-color: #007bff;
  border: none;
  border-radius: 25px;
  padding: 10px 30px;
}

.user-profile-section .publish-new-post .form-control {
  border-radius: 10px;
  border: 1px solid #ddd;
}

.user-profile-section .nav-tabs .nav-item .nav-link {

  margin-right: 5px;
}

.user-profile-section .nav-tabs .nav-item .nav-link.active {
  background-color: #007bff;
  color: white;
}

/* 模态框美化 */
.custom-modal .modal-content {
  border-radius: 15px;
  padding: 20px;
  background: #f7f7f7;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.2);
}

/* 用户头像美化 */
.user-avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  box-shadow: 0 0 8px rgba(0, 0, 0, 0.15);
  transition: all 0.3s ease;
}

.avatar-container {
  display: flex;
  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中 */
  height: 100px; /* 或任何希望的高度 */
  width: 100%; /* 容器宽度 */
}

.user-avatar:hover {
  transform: scale(1.05);
  box-shadow: 0 0 12px rgba(0, 0, 0, 0.2);
}

/* 用户操作按钮美化 */
.user-info-box .btn {
  border-radius: 30px;
  padding: 8px 20px;
  transition: all 0.3s ease;
  margin-bottom: 10px;
}

.user-info-box .btn:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.btn-primary {
  background-color: #0074f1;
}

.btn-primary:hover {
  background-color: #004099;
}


/* Tab 样式调整 */
.nav-tabs .nav-item .nav-link.active {
  background-color: #007bff;
  color: white;
  border-radius: .25rem;
}


</style>


<script>
import Alert from '../Base/Alert'
import store from '../../store'
// bootstrap-markdown 编辑器依赖的 JS 文件，初始化编辑器在组件的 created() 方法中，同时它需要 JQuery 支持哦
import '../../assets/bootstrap-markdown/js/bootstrap-markdown.js'
import '../../assets/bootstrap-markdown/js/bootstrap-markdown.zh.js'
import '../../assets/bootstrap-markdown/js/marked.js'


export default {
  name: 'User',  //this is the name of the component
  components: {
    alert: Alert
  },
  data () {
    return {
      sharedState: store.state,
      user: '',
      postForm: {
        title: '',
        summary: '',
        body: '',
        errors: 0,  // 表单是否在前端验证通过，0 表示没有错误，验证通过
        titleError: null,
        bodyError: null
      },
      sendMessagesForm: {
        body: '',
        bodyError: null
      },
      alerts: []
    }
  },
  computed: {
    isUserOverView: function () {
      const tabs = ['UserFollowers', 'UserFollowing', 'UserPosts', 'UserFollowingPosts']
      if (tabs.indexOf(this.$route.name) == -1) {
        return 'active'
      } else {
        return ''
      }
    }
  },
  methods: {
    getUser (id) {
      const path = `/api/users/${id}`
      this.$axios.get(path)
        .then((response) => {
          // handle success
          this.user = response.data
        })
        .catch((error) => {
          // handle error
          console.error(error)
        })
    },
    onFollowUser (id) {
      const path = `/api/follow/${id}`
      this.$axios.get(path)
        .then((response) => {
          // handle success
          this.getUser(id)
          this.$toasted.success(response.data.message, { icon: 'fingerprint' })
        })
        .catch((error) => {
          // handle error
          console.error(error)
        })
    },
    onUnfollowUser (id) {
      const path = `/api/unfollow/${id}`
      this.$axios.get(path)
        .then((response) => {
          // handle success
          this.getUser(id)
          this.$toasted.success(response.data.message, { icon: 'fingerprint' })
        })
        .catch((error) => {
          // handle error
          console.error(error)
        })
    },
    onDeleteUser (id) {
      this.$swal({
        title: "Are you sure ?",
        text: "Please provide your password.",
        input: 'password',
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        inputValidator: (value) => {
          return !value && 'Please provide a valid password.'
        }
      }).then((result) => {
        if (result.value) {
          const path = '/api/tokens'
          // axios 实现Basic Auth需要在config中设置 auth 这个属性即可
          this.$axios.post(path, {}, {
            auth: {
              'username': this.user.username,
              'password': result.value
            }
          }).then((response) => {
              // handle success
              const path = `/api/users/${id}`
              this.$axios.delete(path)
                .then((response) => {
                  // handle success
                  this.$swal('Deleted', 'You are anonymous now, Goodby!', 'success')
                  store.logoutAction()
                  this.user = ''
                  this.$router.push('/')
                })
                .catch((error) => {
                  // handle error
                  console.log(error.response.data)
                  this.$toasted.error(error.response.data.message, { icon: 'fingerprint' })
                })
            })
            .catch((error) => {
              // handle error
              this.$toasted.error('Invalid password, you cannot delete this account.', { icon: 'fingerprint' })
              console.error('Invalid password, you cannot delete this account.')
            })
        } else {
          this.$swal('Cancelled', 'Your account is safe :)', 'error')
        }
      })
    },
    onSubmitAddPost (e) {
      this.postForm.errors = 0  // 重置

      if (!this.postForm.title) {
        this.postForm.errors++
        this.postForm.titleError = 'Title is required.'
      } else {
        this.postForm.titleError = null
      }

      if (!this.postForm.body) {
        this.postForm.errors++
        this.postForm.bodyError = 'Body is required.'
        // 给 bootstrap-markdown 编辑器内容添加警示样式，而不是添加到 #post_body 上
        $('.md-editor').closest('.form-group').addClass('u-has-error-v1')  // Bootstrap 4
      } else {
        this.postForm.bodyError = null
        $('.md-editor').closest('.form-group').removeClass('u-has-error-v1')
      }

      if (this.postForm.errors > 0) {
        // 表单验证没通过时，不继续往下执行，即不会通过 axios 调用后端API
        return false
      }

      const path = '/api/posts/'
      const payload = {
        title: this.postForm.title,
        summary: this.postForm.summary,
        body: this.postForm.body
      }
      this.$axios.post(path, payload)
        .then((response) => {
          // handle success
          this.$toasted.success('Successed add a new post.', { icon: 'fingerprint' })
          this.postForm.title = '',
          this.postForm.summary = '',
          this.postForm.body = ''
          // 必须加个动态参数，不然路由没变化的话，UserPosts 组件不会刷新重新加载博客列表
          this.$router.push({ name: 'UserPosts', query: { pid: response.data.id } })
        })
        .catch((error) => {
          // handle error
          console.log(error.response.data)
          this.$toasted.error(error.response.data.message, { icon: 'fingerprint' })
        })
    },
    onSubmitSendMessages () {  // 群发私信
      this.sendMessagesForm.bodyError = null  // 重置
      // 每次提交前先移除错误，不然错误就会累加
      $('#sendMessagesForm .form-control-feedback').remove()
      $('#sendMessagesForm .form-group.u-has-error-v1').removeClass('u-has-error-v1')

      if (!this.sendMessagesForm.body) {
        this.sendMessagesForm.bodyError = 'Body is required.'
        // boostrap4 modal依赖jQuery，不兼容 vue.js 的双向绑定。所以要手动添加警示样式和错误提示
        // 给 bootstrap-markdown 编辑器内容添加警示样式，而不是添加到 #post_body 上
        $('#sendMessagesForm .md-editor').closest('.form-group').addClass('u-has-error-v1')  // Bootstrap 4
        $('#sendMessagesForm .md-editor').after('<small class="form-control-feedback">' + this.sendMessagesForm.bodyError + '</small>')
      } else {
        this.sendMessagesForm.bodyError = null
      }

      if (this.sendMessagesForm.bodyError) {
        // 表单验证没通过时，不继续往下执行，即不会通过 axios 调用后端API
        return false
      }

      const path = `/api/send-messages/`
      const payload = {
        body: this.sendMessagesForm.body
      }
      this.$axios.post(path, payload)
        .then((response) => {
          // 重新加载，看看没有有后台任务Alert
          this.get_user_tasks_in_progress(this.$route.params.id)
          // 先隐藏 Modal
          $('#sendMessagesModal').modal('hide')

          // handle success
          this.$toasted.success(response.data.message, { icon: 'fingerprint' })
          this.sendMessagesForm.body = ''
        })
        .catch((error) => {
          // 每次提交前先移除错误，不然错误就会累加
          $('#sendMessagesForm .form-control-feedback').remove()
          $('#sendMessagesForm .form-group.u-has-error-v1').removeClass('u-has-error-v1')
          // handle error
          if (error.response.data.message instanceof Array) {
            for (var field in error.response.data.message) {
              if (field == 'body') {
                this.sendMessagesForm.bodyError = error.response.data.message[field]
                // boostrap4 modal依赖jQuery，不兼容 vue.js 的双向绑定。所以要手动添加警示样式和错误提示
                // 给 bootstrap-markdown 编辑器内容添加警示样式，而不是添加到 #post_body 上
                $('#sendMessagesForm .md-editor').closest('.form-group').addClass('u-has-error-v1')  // Bootstrap 4
                $('#sendMessagesForm .md-editor').after('<small class="form-control-feedback">' + this.sendMessagesForm.bodyError + '</small>')
              } else {
                this.$toasted.error(error.response.data.message[field], { icon: 'fingerprint' })
              }
            }
          } else {
            this.$toasted.error(error.response.data.message, { icon: 'fingerprint' })
          }
        })
    },
    onResetSendMessages () {
      // 先移除错误
      $('#sendMessagesForm .form-control-feedback').remove()
      $('#sendMessagesForm .form-group.u-has-error-v1').removeClass('u-has-error-v1')
      // 再隐藏 Modal
      $('#sendMessagesModal').modal('hide')
      this.$toasted.info('Cancelled, not send messages.', { icon: 'fingerprint' })
    },
    get_user_tasks_in_progress (id) {
      const path = `/api/users/${id}/tasks`
      this.$axios.get(path)
        .then((response) => {
          // handle success
          this.alerts = []  // 需要先清空，不然发起第二个后台任务时，会显示3个

          // 如果当前用户有正在运行的后台任务，则自动创建 Alerts
          for (var i = 0; i < response.data.items.length; i++) {
            var alert = new Object()
            alert.id = response.data.items[i].id
            alert.variant = 'info'
            alert.message = response.data.items[i].description + ' ' + response.data.items[i].progress + '%'
            this.alerts.push(alert)
          }
        })
        .catch((error) => {
          // handle error
          console.error(error)
        })
    },
    onExportPosts () {
      const path = `/api/posts/export-posts`
      this.$axios.get(path)
        .then((response) => {
          // handle success
          // 重新加载，看看没有有后台任务Alert
          this.get_user_tasks_in_progress(this.$route.params.id)
          this.$toasted.success(response.data.message, { icon: 'fingerprint' })
        })
        .catch((error) => {
          // handle error
          console.error(error)
          this.$toasted.error(error.response.data.message, { icon: 'fingerprint' })
        })
    }
  },
  created () {
    const user_id = this.$route.params.id
    this.getUser(user_id)
    if (this.$route.params.id == this.sharedState.user_id) {
      this.get_user_tasks_in_progress(user_id)
    }
    // 初始化 bootstrap-markdown 插件
    $(document).ready(function() {
      $("#postFormBody, #sendMessageFormBody, #sendMessagesFormBody").markdown({
        autofocus:false,
        savable:false,
        iconlibrary: 'fa',  // 使用Font Awesome图标
        language: 'zh'
      })
    })
  },
  // 当路由变化后重新加载数据
  beforeRouteUpdate (to, from, next) {
    next()
    this.getUser(to.params.id)
    if (this.$route.params.id == this.sharedState.user_id) {
      this.get_user_tasks_in_progress(to.params.id)
    }
    // 初始化 bootstrap-markdown 插件
    $(document).ready(function() {
      $("#postFormBody, #sendMessageFormBody").markdown({
        autofocus:false,
        savable:false,
        iconlibrary: 'fa',  // 使用Font Awesome图标
        language: 'zh'
      })
    })
  }
}
</script>
