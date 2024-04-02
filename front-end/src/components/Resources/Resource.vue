<template>
  <div class="container g-pt-20">
    <div class="row">
      <!-- 左边菜单栏 -->
      <div class="col-lg-3 g-mb-50">
        <aside class="g-brd-around g-brd-gray-light-v4 rounded g-px-20 g-py-30">
          <!-- 用户头像 -->
          <div v-if="user" class="text-center g-pos-rel g-mb-30">
            <div class="g-width-100 g-height-100 mx-auto mb-3">
              <img class="img-fluid rounded-circle g-brd-around g-brd-gray-light-v4 g-pa-2" v-bind:src="user._links.avatar" v-bind:alt="user.name || user.username">
            </div>

            <span class="d-block g-font-weight-500">{{ user.name || user.username }}</span>

            <router-link v-bind:to="{ path: `/user/${sharedState.user_id}` }">
              <span class="u-icon-v3 u-icon-size--xs g-color-white--hover g-bg-primary--hover rounded-circle g-pos-abs g-top-0 g-right-15 g-cursor-pointer" title="Go To Your Profile"
                    data-toggle="tooltip"
                    data-placement="top">
                <i class="icon-finance-067 u-line-icon-pro"></i>
              </span>
            </router-link>
          </div>
          <!-- End 用户头像 -->

          <hr class="g-brd-gray-light-v4 g-my-30">

          <!-- 菜单列表 -->
          <ul class="list-unstyled mb-0">
            <li class="g-pb-3">
              <router-link v-bind:to="{ name: 'PostsResource' }" v-bind:active-class="'active g-color-primary--active g-bg-gray-light-v5--active'" class="d-block align-middle u-link-v5 g-color-text g-color-primary--hover g-bg-gray-light-v5--hover rounded g-pa-3">
                <span class="u-icon-v1 g-color-gray-dark-v5 mr-2"><i class="icon-education-008 u-line-icon-pro"></i></span>
                Posts
              </router-link>
            </li>
            <li class="g-pb-3">
              <router-link v-bind:to="{ name: 'LikedPostsResource' }" v-bind:active-class="'active g-color-primary--active g-bg-gray-light-v5--active'" class="d-block align-middle u-link-v5 g-color-text g-color-primary--hover g-bg-gray-light-v5--hover rounded g-pa-3">
                <span class="u-icon-v1 g-color-gray-dark-v5 mr-2"><i class="icon-christmas-056 u-line-icon-pro"></i></span>
                Liked Posts
              </router-link>
            </li>
            <li class="g-py-3">
              <router-link v-bind:to="{ name: 'CommentsResource' }" v-bind:active-class="'active g-color-primary--active g-bg-gray-light-v5--active'" class="d-block align-middle u-link-v5 g-color-text g-color-primary--hover g-bg-gray-light-v5--hover rounded g-pa-3">
                <span class="u-icon-v1 g-color-gray-dark-v5 mr-2"><i class="icon-finance-206 u-line-icon-pro"></i></span>
                Comments
              </router-link>
            </li>
            <li class="g-py-3">
              <router-link v-bind:to="{ name: 'MessagesIndexResource' }" v-bind:active-class="'active g-color-primary--active g-bg-gray-light-v5--active'" class="d-block align-middle u-link-v5 g-color-text g-color-primary--hover g-bg-gray-light-v5--hover rounded g-pa-3">
                <span class="u-icon-v1 g-color-gray-dark-v5 mr-2"><i class="icon-communication-154 u-line-icon-pro"></i></span>
                Messages
              </router-link>
            </li>
          </ul>
          <!-- End 菜单列表 -->
        </aside>
      </div>
      <!-- End 左边菜单栏 -->

      <!-- 右边子路由匹配后，显示对应的组件 -->
      <div class="col-lg-9 g-mb-50">

        <router-view></router-view>

      </div>
      <!-- End 嵌套路由 -->
    </div>
  </div>
</template>

<style scoped>
.container {
  padding-top: 20px;
}

/* 侧边栏样式 */
aside {
  background-color: #f9f9fa; /* 轻微的背景色 */
  border-radius: 8px; /* 轻微的圆角 */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* 添加阴影效果 */
}

/* 侧边栏用户头像区域 */
.text-center {
  margin-bottom: 30px;
}

.g-width-100.g-height-100.mx-auto.mb-3 img {
  width: 100px;
  height: 100px; /* 使头像大小固定 */
}

/* 菜单项样式 */
.list-unstyled li {
  transition: background-color 0.3s ease; /* 平滑的背景颜色过渡效果 */
}

/* 菜单链接样式 */
.u-link-v5 {
  display: block;
  padding: 10px 15px; /* 增加内边距 */
  border-radius: 8px; /* 圆角 */
}


.active .u-icon-v1 {
  color: #ffffff;
}

/* 菜单图标 */
.u-icon-v1 {
  margin-right: 5px;
}


/* 右侧内容区域 */
.col-lg-9 {
  margin-bottom: 50px;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .container {
    padding-top: 10px;
  }

  .col-lg-3, .col-lg-9 {
    margin-bottom: 30px;
  }
}
</style>


<script>
import store from '../../store'

export default {
  name: 'Resource',  // this is the name of the component
  data () {
    return {
      sharedState: store.state,
      user: ''
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
    }
  },
  created () {
    const user_id = this.sharedState.user_id
    this.getUser(user_id)
    // tooltip
    $(document).ready(function(){
      $('[data-toggle="tooltip"]').tooltip();
    })
  }
}
</script>
