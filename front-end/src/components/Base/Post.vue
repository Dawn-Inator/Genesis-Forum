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
        <router-link v-bind:to="{ path: `/user/${post.author.id}` }" class="author-link">{{ post.author.name || post.author.username }}</router-link>
        <h5 class="h5 g-color-gray-dark-v1 mb-0">
          <router-link v-bind:to="{ name: 'PostDetail', params: { id: post.id } }" class="g-text-underline--none--hover article-title"><span v-html="post.title"></span></router-link>
          <span class="category-tag">{{ categoryName }}</span>
        </h5>
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

@media (max-width: 460px) { /* 针对小屏幕设备的媒体查询 */
  .list-inline {
    flex-direction: column; /* 小屏幕上垂直排列 */
  }

  .list-inline-item {
    margin-right: 0; /* 移除水平间隔 */
    margin-bottom: 10px; /* 添加垂直间隔 */
  }
}

.author-link {
  text-decoration: none; /* 添加这行以去除下划线 */
  color: #007bff;
  font-weight: bold;
  margin-bottom: 5px;
}

.article-title {
  font-weight: 800;
  margin-right: 10px;
}

.category-tag {
  display: inline-block;
  background-image: linear-gradient(to right, #ca3cdd, #53bdba); /* 渐变蓝色背景 */
  color: white;
  border-radius: 12px;
  padding: 2px 8px;
  font-size: 0.75rem;
  vertical-align: middle;
}


/* 其他样式保持不变 */


.media {
  border: 1px solid #dee2e6;
  border-left: 5px solid #007bff; /* 左边框蓝色 */
  padding: 20px;
  margin-bottom: 20px;
  border-radius: 0.5rem;
  background-color: #ffffff;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  transition: box-shadow 0.3s ease;
}

.media:hover {
  box-shadow: 0 4px 8px rgba(215, 23, 232, 0.2);
}

.media img {
  border: 2px solid #ffffff;
  transition: transform 0.3s ease;
}

.u-badge-v2--xs {
  background-color: #ff0000;
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.markdown-body {
  font-size: 0.9rem;
  color: #333;
  line-height: 1.5;
}

/* 为按钮添加现代化的蓝色风格 */
.btn-xs, .g-color-gray-dark-v5 {
  transition: all 0.2s ease;
  background-image: linear-gradient(to right, #007bff, #0056b3); /* 渐变蓝色背景 */
  color: #ffffff; /* 文字颜色为白色 */
  border-radius: 20px; /* 边框圆角 */
  padding: 5px 10px; /* 调整内边距 */
  font-size: 0.8rem; /* 调整字体大小 */
  box-shadow: 0 2px 4px rgba(0,0,0,0.1); /* 添加阴影 */
}

.btn-xs:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 4px rgba(0,0,0,0.3); /* 悬浮时阴影加深 */
}

/* 作者名字和文章标题的蓝色表示 */
h5 a, .h6 a {
  color: #007bff !important; /* 设置链接颜色为蓝色 */
  transition: color 0.2s ease; /* 平滑颜色过渡效果 */
}

h5 a:hover, .h6 a:hover {
  color: #cd42f3 !important; /* 鼠标悬停时颜色加深 */
}

.icon-eye, .icon-heart, .icon-bubble {
  margin-right: 5px;
}

.list-inline-item .btn {
  margin: 0 5px;
}

.g-color-gray-dark-v5 {
  color: #c2d9ef !important;
}

.g-color-gray-dark-v5:hover {
  color: #ff6bff !important; /* 链接和图标悬停时的蓝色 */
}
</style>




<script>
import axios from 'axios' // 确保你已经安装并导入了axios
import store from '../../store'
import VueMarkdown from 'vue-markdown'

export default {
  props: ['post'],
  components: {
    VueMarkdown
  },
  data () {
    return {
      sharedState: store.state,
      categories: [] // 存储分类列表
    }
  },
  created() {
    this.fetchCategories(); // 组件创建时获取分类
  },
  methods: {
    fetchCategories() {
      // 获取所有分类
      axios.get('/api/categories/').then(response => {
        this.categories = response.data;
      }).catch(error => {
        console.error("There was an error fetching the categories:", error);
      });
    },
    findCategoryName(categoryId) {
      const category = this.categories.find(c => c.id === categoryId);
      return category ? category.name : '默认';
    },
  },
  computed: {
    categoryName() {
      return this.findCategoryName(this.post.category_id || 0);
    }
  },
}
</script>

