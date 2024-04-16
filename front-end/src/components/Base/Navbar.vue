<template>
<section>
  <div class="container">

  <nav class="navbar navbar-expand-lg navbar-modern my-4" >
      <!-- Logo and home link with conditionally displayed based on authentication status -->

        <div class="navbar-brand" v-if="sharedState.is_authenticated">
            <router-link to="/" class="g-text-underline--none--hover" style="color: black; padding: 10px;">
              <img src="../../assets/GPT-logo.png" width="30" height="30" class="d-inline-block align-top">
                ChatGPT
            </router-link>
            <a href="https://chatgpt.inator.site" class="g-text-underline--none--hover" style="color: purple;">Accessing</a>
            </div>

            <div class="navbar-brand" v-else>
            <router-link to="/" class="g-text-underline--none--hover" style="color: black; padding: 10px;">
              <img src="../../assets/github-mark.png" width="30" height="30" class="d-inline-block align-top">
                Wecome to
            </router-link>
            <a href="https://github.com/Dawn-Inator/Genesis-Forum" class="g-text-underline--none--hover" style="color: purple;">Genesis-Forum</a>
            </div>

            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
              <span class="navbar-toggler-icon"></span>
            </button>

            <div class="collapse navbar-collapse" id="navbarSupportedContent">

              <ul class="navbar-nav mr-auto">
                        <li class="nav-item">
                          <router-link to="/" class="nav-link">Home</router-link>
                        </li>
                        <li class="nav-item">
                          <router-link to="/ping" class="nav-link">Ping</router-link>
                        </li>
                        <li v-if="sharedState.is_authenticated && sharedState.user_perms.includes('admin')" class="nav-item">
                          <router-link to="/admin" class="nav-link">Admin</router-link>
                        </li>
              </ul>

               <form v-if="sharedState.is_authenticated" class="form-inline navbar-left mr-auto" @submit.prevent="onSubmitSearch">
                         <input v-model="searchForm.body" id="searchBody" class="form-control mr-sm-2" type="search" placeholder="Search">
                         <button class="btn btn-search-purple my-2 my-sm-0" type="submit">Search</button>
                       </form>

              <ul v-if="sharedState.is_authenticated" class="navbar-nav" style="padding-right: 20px;">
                <li class="nav-item">
                  <router-link to="/notifications/comments" class="nav-link">
                    <span style="font-size: 16px; padding:5px;">
                      Notifications
                    </span>
                    <span id="new_notifications_count" style="visibility: hidden;" class="u-label g-font-size-11 g-bg-aqua g-rounded-20 ">0</span>
                  </router-link>
                </li>
              </ul>


              <ul v-if="sharedState.is_authenticated" class="nav navbar-nav navbar-right mr-auto ">
                <li class=" nav-item dropdown">
                  <a class=" dropdown-toggle no-caret"  id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" style="padding: 30px;">
                    <img v-bind:src="sharedState.user_avatar" class="g-brd-around g-brd-gray-light-v3 g-pa-2 rounded-circle rounded mCS_img_loaded " width="50" height="50">
                    <span class="btn btn-user_avatar" style="font-weight: bold; font-size: 20px;">{{ sharedState.user_name }}</span>
                  </a>
                  <div class="dropdown-menu" aria-labelledby="navbarDropdown">
                    <router-link v-bind:to="{ path: `/user/${sharedState.user_id}` }" class="dropdown-item"><i class="icon-star g-pos-rel g-top-1 g-mr-5"></i> Your profile</router-link>
                    <router-link v-bind:to="{ name: 'PostsResource' }" class="dropdown-item"><i class="icon-share g-pos-rel g-top-1 g-mr-5"></i> Your resource</router-link>
                    <router-link v-bind:to="{ name: 'SettingProfile' }" class="dropdown-item"><i class="icon-settings g-pos-rel g-top-1 g-mr-5"></i> Settings</router-link>
                    <a v-on:click="handlerLogout" class="dropdown-item" href="#"><i class="icon-logout g-pos-rel g-top-1 g-mr-5"></i> Sign out</a>
                  </div>
                </li>
              </ul>

              <ul v-else class="nav navbar-nav navbar-right">
                <li class="navbar-nav mr-auto mt-2">
                  <router-link to="/login" class="nav-link btn-rounded" style="font-size: 20px; padding-left: 10px;"><i class="icon-login g-pos-rel g-top-1 g-mr-5"></i> Sign in</router-link>
                </li>
              </ul>

            </div>
  </nav>
  </div>
</section>
</template>


<style scoped>


.btn-user_avatar:hover{
  background-color: #00aaff;
}

.btn-search-purple {
  background-image: linear-gradient(to right, #2df4f4, #d412f6); /* 渐变蓝色背景 */
  color: white;
  border: none; /* Optional: removes the border */
}

.btn-search-purple:hover {
  background-image: linear-gradient(to right, #e61445, #f3e00b); /* 渐变蓝色背景 */
  color: white;
  border: none; /* Optional: removes the border */
}

.navbar-modern {
  background-color: #007bff; /* Vibrant blue */
  border-radius: 60px; /* Rounded corners for modern look */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Subtle shadow for depth */
  padding: 10px; /* Adequate padding for visual balance */
}

.navbar-brand {
  display: flex;
  align-items: center;
  color: white; /* Contrast text color */
}

.nav-link {
  color: white;
  margin-right: 10px;
  transition: color 0.3s;
}

.nav-link:hover, .nav-link:focus {
  color: #66a6ff; /* Lighter blue on hover for interactivity */
}

.dropdown-menu {
  border-radius: 15px; /* 容器的圆角 */
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}


.dropdown-item:hover, .dropdown-item:focus {
  background-color: #0069d9; /* 互动时的浅蓝色 */
  color: white;
}

.dropdown-item:first-child {
  border-top-left-radius: 15px;
  border-top-right-radius: 15px;
}

.dropdown-item:last-child {
  border-bottom-left-radius: 15px;
  border-bottom-right-radius: 15px;
}


.badge-info {
  background-color: #17a2b8;
}

/* 改变折叠按钮的图标颜色 */
.navbar-toggler-icon {
    background-image: url("data:image/svg+xml;charset=utf8,%3Csvg viewBox='0 0 30 30' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath stroke='rgba(255, 255, 255, 0.5)' stroke-width='2' stroke-linecap='round' stroke-miterlimit='10' d='M4 7h22M4 15h22M4 23h22'/%3E%3C/svg%3E");
}

/* 调整背景色 */
.navbar-toggler {
    background-color: #17a2b8; /* 或者任何你想要的颜色 */
    margin-right: 20px;
}

/* 针对用户名的按钮移除下划线 */
.btn-user_avatar {
  text-decoration: none; /* 移除下划线 */
  transition: background-color 0.3s; /* 平滑的背景色变化 */
}

.btn-user_avatar:hover {
  background-color: #00aaff; /* 鼠标悬停时的背景色 */
  text-decoration: none; /* 确保悬停时没有下划线 */
}

/* 针对包含图片的链接移除下划线 */
a.no-caret {
  text-decoration: none; /* 移除下划线 */
}

a.no-caret:hover {
  text-decoration: none; /* 确保悬停时没有下划线 */
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
