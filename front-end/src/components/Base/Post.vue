<template>
  <div class="container g-mt-10">
  <div class="media g-brd-around g-brd-gray-light-v4 g-brd-left-1 g-pa-20 g-mb-20">
    <router-link v-bind:to="{ path: `/user/${post.author.id}` }" v-bind:title="post.author.name || post.author.username">
      <span v-if="post.is_new" class="d-inline-block g-pos-rel">
        <span class="u-badge-v2--xs u-badge--top-left g-bg-red g-mt-7 g-ml-7"></span>
        <img class="d-flex g-brd-around g-brd-gray-light-v3 g-pa-2 g-width-40 g-height-40 rounded-circle rounded mCS_img_loaded g-mt-3 g-mr-15" v-bind:src="post.author.avatar" v-bind:alt="post.author.name || post.author.username">
      </span>
      <img v-else class="d-flex g-brd-around g-brd-gray-light-v3 g-pa-2 g-width-40 g-height-40 rounded-circle rounded mCS_img_loaded g-mt-3 g-mr-15" v-bind:src="post.author.avatar" v-bind:alt="post.author.name || post.author.username">
    </router-link>

    <div class="media-body">
      <div class="g-mb-15">
        <h5 class="h5 g-color-gray-dark-v1 mb-0"><router-link v-bind:to="{ path: `/user/${post.author.id}` }" class="g-text-underline--none--hover">{{ post.author.name || post.author.username }}</router-link> <span class="h6">发布了文章<router-link v-bind:to="{ name: 'PostDetail', params: { id: post.id } }" class="g-text-underline--none--hover">《<span v-html="post.title"></span>》</router-link></span></h5>
        <span class="g-color-gray-dark-v4 g-font-size-12">{{ $moment(post.timestamp).format('YYYY年MM月DD日 HH:mm:ss') }}</span>
      </div>

      <!-- vue-markdown 开始解析markdown，它是子组件，通过 props 给它传值即可
      v-highlight 是自定义指令，用 highlight.js 语法高亮 -->
      <vue-markdown
        :source="post.summary"
        class="markdown-body g-mb-15"
        v-highlight>
      </vue-markdown>

      <div class="d-flex justify-content-start">
        <ul class="list-inline mb-0">
          <li class="list-inline-item g-mr-20">
            <a class="g-color-gray-dark-v5 g-text-underline--none--hover" href="javascript:;">
              <i class="icon-eye g-pos-rel g-top-1 g-mr-3"></i> {{ post.views }}
            </a>
          </li>
          <li class="list-inline-item g-mr-20">
            <router-link v-bind:to="{ path: `/post/${post.id}#like-post` }" class="g-color-gray-dark-v5 g-text-underline--none--hover">
              <i class="icon-heart g-pos-rel g-top-1 g-mr-3"></i> {{ post.likers_count }}
            </router-link>
          </li>
          <li class="list-inline-item g-mr-20">
            <router-link v-bind:to="{ path: `/post/${post.id}#comment-list-wrap` }" class="g-color-gray-dark-v5 g-text-underline--none--hover">
              <i class="icon-bubble g-pos-rel g-top-1 g-mr-3"></i> {{ post.comments_count }}
            </router-link>
          </li>
        </ul>
        <ul class="list-inline mb-0 ml-auto">
          <li class="list-inline-item g-mr-5">
            <router-link v-bind:to="{ name: 'PostDetail', params: { id: post.id } }" class="btn btn-xs u-btn-outline-primary">阅读全文</router-link>
          </li>
          <li v-if="post.author.id == sharedState.user_id || sharedState.user_perms.includes('admin')" class="list-inline-item g-mr-5">
            <button v-on:click="$emit('edit-post')" class="btn btn-xs u-btn-outline-purple" data-toggle="modal" data-target="#editPostModal">编辑</button>
          </li>
          <li v-if="post.author.id == sharedState.user_id || sharedState.user_perms.includes('admin')" class="list-inline-item">
            <button v-on:click="$emit('delete-post')" class="btn btn-xs u-btn-outline-red">删除</button>
          </li>
        </ul>
      </div>
    </div>
  </div>
  </div>
</template>

<style scoped>
.media {
  border: 1px solid #dee2e6; /* 细边框 */
  border-left: 5px solid #007bff; /* 加粗左侧边框以突出显示 */
  padding: 20px;
  margin-bottom: 20px;
  border-radius: 0.5rem; /* 增加圆角大小 */
  background-color: #ffffff; /* 使用纯白背景色 */
  box-shadow: 0 2px 4px rgba(0,0,0,0.1); /* 添加阴影以提升层次感 */
  transition: box-shadow 0.3s ease; /* 鼠标悬停时增加阴影效果 */
}

.media img {
  border: 3px solid #f8f9fa; /* 图像边框颜色 */
  transition: transform 0.3s ease; /* 图像悬停放大效果 */
}

.media:hover {
  box-shadow: 0 4px 8px rgba(0,0,0,0.2); /* 鼠标悬停时阴影更明显 */
}

.media img {
  border: 2px solid #ffffff; /* 保持图片边框与背景一致 */
  transition: transform 0.3s ease; /* 保留图像悬停放大效果 */
}

.u-badge-v2--xs {
  background-color: #ff0000; /* 使用更鲜艳的红色 */
  width: 10px; /* 增大标记尺寸 */
  height: 10px;
  border-radius: 50%; /* 圆形标记 */
}

.markdown-body {
  font-size: 0.9rem; /* 细微调整字体大小 */
  color: #333; /* 深色字体 */
  line-height: 1.5; /* 增加行高改善可读性 */
}

/* 按钮样式调整 */
.btn-xs, .g-color-gray-dark-v5 {
  transition: all 0.2s ease; /* 平滑过渡效果 */
}

.btn-xs:hover {
  transform: translateY(-2px); /* 按钮轻微上移 */
  box-shadow: 0 2px 4px rgba(0,0,0,0.2); /* 按钮添加阴影 */
}

/* Icon样式调整 */
.icon-eye, .icon-heart, .icon-bubble {
  margin-right: 5px;
}

.list-inline-item .btn {
  margin: 0 5px; /* 调整按钮间距 */
}

/* 链接和图标的颜色 */
.g-color-gray-dark-v5 {
  color: #343a40 !important; /* 更深的灰色 */
}

.g-color-gray-dark-v5:hover {
  color: #0056b3; /* 链接颜色变化，保持一致性 */
}

</style>


<script>
import store from '../../store'
// 导入 vue-markdown 组件解析 markdown 原文为　HTML
import VueMarkdown from 'vue-markdown'

export default {
  props: ['post'],
  components: {
    VueMarkdown
  },
  data () {
    return {
      sharedState: store.state
    }
  },
  /*
  computed: {
    leftBrdColor: function () {
      const colors = ['primary', 'blue', 'red', 'purple', 'orange', 'yellow', 'aqua', 'cyan', 'teal', 'brown', 'pink', 'black']
      let index = Math.floor((Math.random() * colors.length))
      return 'g-brd-' + colors[index] + '-left'
    }
  }
  */
}
</script>
