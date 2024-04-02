<template>
<section>
  <div class="container">
    <nav class="navbar navbar-expand-lg navbar-light bg-light" style="margin-bottom: 20px;">

      <div class="navbar-brand" v-if="sharedState.is_authenticated">
      <router-link to="/" class="g-text-underline--none--hover" style="color: black;">
        <img src="../../assets/GPT-logo.png" width="30" height="30" class="d-inline-block align-top" alt="">
          ChatGPT
      </router-link>
      <a href="https://chatgpt.inator.site" class="g-text-underline--none--hover" style="color: purple;">Accessing</a>
      </div>

      <div class="navbar-brand" v-else>
      <router-link to="/" class="g-text-underline--none--hover" style="color: black;">
        <img src="../../assets/github-mark.png" width="30" height="30" class="d-inline-block align-top" alt="">
          Wecome to
      </router-link>
      <a href="https://github.com/Dawn-Inator/Genesis-Forum" class="g-text-underline--none--hover" style="color: purple;">Genesis-Forum</a>
      </div>

      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav mr-auto mt-2 ">
          <li class="nav-item active">
            <router-link to="/" class="nav-link btn btn-info btn-sm btn-rounded" style="color: aliceblue;">Home <span class="sr-only">(current)</span></router-link>
          </li>
          <li class="nav-item">
            <router-link to="/ping" class="nav-link btn btn-info btn-sm btn-rounded" style="color: aliceblue;">Ping</router-link>
          </li>
          <li class="nav-item" v-if="sharedState.is_authenticated && sharedState.user_perms.includes('admin')">
            <router-link to="/admin" class="nav-link btn btn-info btn-sm btn-rounded" style="color: aliceblue;">Admin</router-link>
          </li>
        </ul>

         <div v-if="sharedState.is_authenticated" class="form-inline my-2 mr-5 ">
              <div class="input-group">
                <input v-model="searchForm.body" type="search" class="form-control" id="searchBody" placeholder="Search" aria-label="Search">
                <div class="input-group-append">
                  <button class="btn btn-primary" type="submit">Search</button>
                </div>
              </div>
         </div>

        <ul v-if="sharedState.is_authenticated" class="navbar-nav mr-auto mt-2 ">
          <li class="nav-item ">
            <router-link v-bind:to="{ path: '/notifications/comments' }" class="nav-link btn btn-warning btn-sm btn-rounded" >
              <span class="text-shift-right" style="font-size: 15px; padding:0px;">
                <i class="icon-education-033 u-line-icon-pro g-color-red g-font-size-16 g-pos-rel g-top-2 g-mr-3"></i>
                Notifications
              </span>
              <span id="new_notifications_count" style="visibility: hidden;" class="u-label g-font-size-11 g-bg-aqua g-rounded-20 g-px-10">0</span>
              </router-link>
          </li>
        </ul>

        <ul v-if="sharedState.is_authenticated" class="nav navbar-nav navbar-right mr-auto ">
          <li class=" nav-item dropdown">
            <a class=" dropdown-toggle no-caret"  id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
              <img v-bind:src="sharedState.user_avatar" class="g-brd-around g-brd-gray-light-v3 g-pa-2 rounded-circle rounded mCS_img_loaded " width="50" height="50">
              <span class="btn btn-light" style="font-weight: bold; font-size: 20px;">{{ sharedState.user_name }}</span>
            </a>
            <div class="dropdown-menu" aria-labelledby="navbarDropdown">
              <router-link v-bind:to="{ path: `/user/${sharedState.user_id}` }" class="dropdown-item"><i class="icon-star g-pos-rel g-top-1 g-mr-5"></i> Your profile</router-link>
              <router-link v-bind:to="{ name: 'PostsResource' }" class="dropdown-item"><i class="icon-share g-pos-rel g-top-1 g-mr-5"></i> Your resource</router-link>
              <router-link v-bind:to="{ name: 'SettingProfile' }" class="dropdown-item"><i class="icon-settings g-pos-rel g-top-1 g-mr-5"></i> Settings</router-link>
              <div class="dropdown-divider"></div>
              <a v-on:click="handlerLogout" class="dropdown-item" href="#"><i class="icon-logout g-pos-rel g-top-1 g-mr-5"></i> Sign out</a>
            </div>
          </li>
        </ul>

        <ul v-else class="nav navbar-nav navbar-right">
          <li class="navbar-nav mr-auto mt-2">
            <router-link to="/login" class="nav-link btn-primary btn-rounded" style="color: white;"><i class="icon-login g-pos-rel g-top-1 g-mr-5"></i> Sign in</router-link>
          </li>
        </ul>

      </div>
    </nav>
  </div>
</section>
</template>

<style scoped>

.container {
  padding-top: 20px; /* 避免内容被悬浮的导航栏遮挡 */
}

/* 基础调整，保持原有的设计精髓 */
.btn-rounded {
  border-radius: 10px;
  font-weight: bold;
  margin-bottom: 10px; /* 保持 */
  margin-left: 0.5rem; /* 保持 */
  margin-right: 0.5rem; /* 保持 */
  transition: background-color 0.3s ease; /* 平滑背景色变换 */
}

.text-shift-right {
  margin-left: 20px; /* 维持原有的偏移，确保视觉上的平衡 */
}

/* 提升按钮和链接的交互感 */
.nav-link:hover, .btn-nav:hover {
  background-color: #0056b3; /* 深蓝色，增强悬停反馈 */
  color: #ffffff;

}

.nav-profile:hover{
  padding: 10px;
  background-color: #9ca7b3; /* 深灰色，增强悬停反馈 */
}

.dropdown-item:hover, .dropdown-item:focus {
  background-color: #0069d9; /* 略微亮一点的蓝色，增强交互效果 */
  color: #ffffff;
}

/* 微调下拉菜单样式，增加细微阴影，提升层次感 */
.dropdown-menu {
  box-shadow: 0 2px 5px rgba(0,0,0,.1);
  border: 1px solid #ddd; /* 轻微边框，增强视觉效果 */
}

/* 增加导航栏的视觉吸引力 */
.navbar {
  position: sticky;
    top: 0; /* 将导航栏固定在视口的顶部 */
    z-index: 1000; /* 确保导航栏位于页面其他元素之上 */
    background-color: #007bff; /* 导航栏背景颜色 */
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* 添加一些阴影以增强层次感 */
    border-radius: 30px; /* 可以根据需要调整圆角 */
}
</style>


<script>
import store from '../../store'
// 在 JQuery 中使用 axios 的话需要重新导入，不能使用 main.js 中定义的 Vue 全局属性 this.$axios
import axios from 'axios'

export default {
  name: 'Navbar',  //this is the name of the component
  data () {
    return {
      sharedState: store.state,
      searchForm: {
        body: ''
      }
    }
  },
  methods: {
    handlerLogout (e) {
      store.logoutAction()
      this.$toasted.show('You have been logged out.', { icon: 'fingerprint' })
      this.$router.push('/login')
    },
    onSubmitSearch() {
      if (!this.searchForm.body) {
        $('#searchBody').attr('placeholder', 'keyword required.');
        $('#searchBody').css('background-color', '#fff0f0');

        // 表单验证没通过时，不继续往下执行，即不会通过 axios 调用后端API
        return false
      } else {
        $('#searchBody').css('background-color', '');
      }

      // 提供了搜索关键词后，只需要路由到搜索结果页即可，在 SearchResult.vue 中再请求后端 API
      let q = this.searchForm.body
      let page = 1
      let per_page = 5
      if (typeof this.$route.query.page != 'undefined') {
        page = this.$route.query.page
      }

      if (typeof this.$route.query.per_page != 'undefined') {
        per_page = this.$route.query.per_page
      }

      // 路由到搜索结果页
      this.$router.replace({
        path: '/search',
        query: {
          q: q,
          page: page,
          per_page: per_page
        }
      })
    }
  },
  mounted () {
    // 轮询 /api/users/<int:id>/notifications/ 请求用户的新通知
    $(function() {
      let since = 0
      let total_notifications_count = 0  // 总通知计数
      let unread_recived_comments_count = 0  // 收到的新评论通知计数
      let unread_messages_count = 0  // 收到的新私信通知计数
      let unread_follows_count = 0  // 新粉丝通知计数
      let unread_posts_likes_count = 0  // 新收藏文章的通知计数
      let unread_comments_likes_count = 0  // 新的评论点赞的通知计数
      let unread_followeds_posts_count = 0  // 用户关注的人的新文章通知计数

      setInterval(function() {
        if (window.localStorage.getItem('madblog-token')) {
          // 如果用户已登录，才开始请求 API
          const payload = JSON.parse(atob(window.localStorage.getItem('madblog-token').split('.')[1]))
          const user_id = payload.user_id
          const path = `/api/users/${user_id}/notifications/?since=${since}`
          axios.get(path)
            .then((response) => {
              // handle success
              for(var i = 0; i < response.data.length; i++) {
                switch (response.data[i].name) {
                  case 'unread_recived_comments_count':
                    unread_recived_comments_count = response.data[i].payload
                    // jQuery设置值 (因为左侧导航栏不是一个组件内)
                    $('#unread_recived_comments_count').text(unread_recived_comments_count);
                    break

                  case 'unread_messages_count':
                    unread_messages_count = response.data[i].payload
                    $('#unread_messages_count').text(unread_messages_count);
                    break

                  case 'unread_follows_count':
                    unread_follows_count = response.data[i].payload
                    $('#unread_follows_count').text(unread_follows_count);
                    break

                  case 'unread_posts_likes_count':
                    unread_posts_likes_count = response.data[i].payload
                    $('#unread_posts_likes_count').text(unread_posts_likes_count);
                    break

                  case 'unread_comments_likes_count':
                    unread_comments_likes_count = response.data[i].payload
                    $('#unread_comments_likes_count').text(unread_comments_likes_count);
                    break

                  case 'unread_followeds_posts_count':
                    unread_followeds_posts_count = response.data[i].payload
                    $('#unread_followeds_posts_count').text(unread_followeds_posts_count);
                    break

                  case 'task_progress':
                    $('#' + response.data[i].payload.task_id).text(response.data[i].payload.description + ' ' + response.data[i].payload.progress + '%')
                    break
                }
                since = response.data[i].timestamp
              }

              total_notifications_count = unread_recived_comments_count + unread_messages_count + unread_follows_count + unread_posts_likes_count + unread_comments_likes_count + unread_followeds_posts_count
              // 每一次请求之后，根据 total_notifications_count 的值来显示或隐藏徽标
              $('#new_notifications_count').text(total_notifications_count)
              $('#new_notifications_count').css('visibility', total_notifications_count ? 'visible' : 'hidden');
            })
            .catch((error) => {
              // handle error
              console.error(error)
            })
        }
      }, 3000)
    })
  }
}
</script>
