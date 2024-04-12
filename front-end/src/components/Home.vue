<template>
  <div class="container">

    <div class="btn-group my-3 d-flex justify-content-center" role="group" aria-label="Categories">
          <button type="button" class="btn gradient-btn" @click="getPosts()" style="border-radius: 10px;">
            全部
          </button>
          <button v-for="category in categories" :key="category.id"
                  @click="getPostsByCategory(category.id)"
                  type="button"
                  class="btn gradient-btn" style="border-radius: 10px;">
            {{ category.name }}
          </button>
    </div>

    <!-- Modal: Edit Post -->
    <div data-backdrop="static" class="modal fade" id="editPostModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered modal-lg" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="editPostModalTitle">Update Post</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">

          <div class="row justify-content-center my-3">
            <div class="col-md-6">

            <form id="editPostForm" @submit.prevent="onSubmitUpdatePost" @reset.prevent="onResetUpdatePost">
              <div class="form-group" v-bind:class="{'u-has-error-v1': editPostForm.titleError}">
                <input type="text" v-model="editPostForm.title" class="form-control" id="editPostFormTitle" placeholder="标题">
                <small class="form-control-feedback" v-show="editPostForm.titleError">{{ editPostForm.titleError }}</small>
              </div>
              <div class="form-group">
                <input type="text" v-model="editPostForm.summary" class="form-control" id="editPostFormSummary" placeholder="摘要">
              </div>
              <div class="form-group">
                <textarea v-model="editPostForm.body" class="form-control" id="editPostFormBody" rows="5" placeholder=" 内容"></textarea>
                <small class="form-control-feedback" v-show="editPostForm.bodyError">{{ editPostForm.bodyError }}</small>
              </div>
              <button type="reset" class="btn btn-secondary">Cancel</button>
              <button type="submit" class="btn btn-primary">Update</button>
            </form>

            </div>
          </div>

          </div>
        </div>
      </div>
    </div>


    <form id="addPostForm" v-if="sharedState.is_authenticated && sharedState.user_perms.includes('write')" @submit.prevent="onSubmitAddPost" class="g-mb-40">
      <div class="form-group" v-bind:class="{'u-has-error-v1': postForm.titleError}">
        <input type="text" v-model="postForm.title" class="form-control" id="postFormTitle" placeholder="标题">
        <small class="form-control-feedback" v-show="postForm.titleError">{{ postForm.titleError }}</small>
      </div>
      <div class="form-group">
        <input type="text" v-model="postForm.summary" class="form-control" id="postFormSummary" placeholder="摘要">
      </div>
      <div class="form-group">
        <textarea v-model="postForm.body" class="form-control" id="postFormBody" rows="5" placeholder=" 内容"></textarea>
        <small class="form-control-feedback" v-show="postForm.bodyError">{{ postForm.bodyError }}</small>
      </div>

      <div class="form-group d-flex align-items-center">
          <select id="postFormCategory" class="form-control custom-select" v-model="postForm.category_id" style="width: 80%;">
            <option disabled value="">请选择一个分类</option>
            <option v-for="category in categories" :key="category.id" :value="category.id">{{ category.name }}</option>
          </select>
          <button type="submit" class="btn btn-primary ml-2">Submit</button>
          <small class="form-control-feedback" v-show="postForm.categoryError">{{ postForm.categoryError }}</small>
        </div>

    </form>

    <div class="card border-0 g-mb-15 my-3">
      <!-- Panel Header -->
      <div class="card-header d-flex align-items-center justify-content-between g-bg-blue text-white">
          <h3 class="h6 mb-0">
            <i class="icon-bubbles g-pos-rel g-top-1 g-mr-5"></i> All Posts <small v-if="posts">(共 {{ posts._meta.total_items }} 篇, {{ posts._meta.total_pages }} 页)</small>
          </h3>

        <div class="dropdown g-mb-10 g-mb-0--md">
          <span class="d-block g-color-primary--hover g-cursor-pointer g-mr-minus-5 g-pa-5" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
            <i class="icon-options-vertical g-pos-rel g-top-1"></i>
          </span>
          <div class="dropdown-menu dropdown-menu-right rounded-0 g-mt-10">
            <router-link v-bind:to="{ path: $route.path, query: { page: 1, per_page: 1 }}" class="dropdown-item g-px-10">
              <i class="icon-plus g-font-size-12 g-color-gray-dark-v5 g-mr-5"></i> 每页 1 篇
            </router-link>
            <router-link v-bind:to="{ path: $route.path, query: { page: 1, per_page: 5 }}" class="dropdown-item g-px-10">
              <i class="icon-layers g-font-size-12 g-color-gray-dark-v5 g-mr-5"></i> 每页 5 篇
            </router-link>
            <router-link v-bind:to="{ path: $route.path, query: { page: 1, per_page: 10 }}" class="dropdown-item g-px-10">
              <i class="icon-wallet g-font-size-12 g-color-gray-dark-v5 g-mr-5"></i> 每页 10 篇
            </router-link>

            <div class="dropdown-divider"></div>

            <router-link v-bind:to="{ path: $route.path, query: { page: 1, per_page: 20 }}" class="dropdown-item g-px-10">
              <i class="icon-fire g-font-size-12 g-color-gray-dark-v5 g-mr-5"></i> 每页 20 篇
            </router-link>

          </div>
        </div>
      </div>
      <!-- End Panel Header -->

      <!-- Panel Body -->
      <div v-if="posts" class="card-block g-pa-0" >

        <post v-for="(post, index) in posts.items" v-bind:key="index"
          v-bind:post="post"
          v-on:edit-post="onEditPost(post)"
          v-on:delete-post="onDeletePost(post)">
        </post>

      </div>
      <!-- End Panel Body -->
    </div>

    <!-- Pagination #04 -->
    <div v-if="posts && posts._meta.total_pages > 1" class="my-4">
      <pagination
        v-bind:cur-page="posts._meta.page"
        v-bind:per-page="posts._meta.per_page"
        v-bind:total-pages="posts._meta.total_pages">
      </pagination>
    </div>
    <!-- End Pagination #04 -->

  </div>
</template>

<style scoped>
.btn-group {
  display: flex;
  justify-content: center; /* 水平居中按钮组 */
  flex-wrap: wrap; /* 允许按钮换行 */
}

.gradient-btn {
  color: white; /* 设置按钮文本为白色 */
  background-image: linear-gradient(to right, #444dec, #51fc51); /* 渐变背景色 */
  border: none; /* 去除边框 */
  margin: 0 30px; /* 增加按钮间的间距 */
  transition: transform 0.3s ease-in-out; /* 平滑变换效果 */
}

.gradient-btn:hover {
  transform: translateY(-2px); /* 鼠标悬停时上移按钮 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* 添加阴影效果 */
}

.custom-select {
  flex-grow: 1; /* 选择框占据剩余空间 */
  margin-right: 10px; /* 添加右边距，使按钮与选择框分开 */
}

.btn-primary {
  flex-shrink: 0; /* 防止按钮在小屏幕上缩小 */
}

/* 可以在这里添加其他美化样式，如下 */
.custom-select {
  border-radius: 0.25rem;
}

.btn-primary:hover {
  background-color: #0056b3; /* 更深的蓝色 */
}

.g-bg-blue {
    background-color: #007bff !important; /* Bootstrap 4 primary color */
}

/* 基础重设与公共样式 */
.form-control, .btn {
  border-radius: 0.25rem;
}

.btn-primary, .btn-secondary {
  padding: 0.5rem 1rem;
  margin: 0.25rem;
}

/* 模态窗口样式调整 */
.modal-content {
  border-radius: 0.5rem;
}

.modal-header, .modal-body {
  padding: 20px;
}

/* 提交表单样式 */
#addPostForm, #editPostForm {
  background-color: #f8f9fa;
  padding: 20px;
  border-radius: 0.5rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

/* 错误信息样式 */
.form-control-feedback {
  color: #dc3545;
}

/* 卡片样式调整 */
.card {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border-radius: 0.5rem;
}

.card-header {
  background-color: #007bff;
  color: #ffffff;
  border-radius: 0.5rem 0.5rem 0 0;
}

/* 分页样式调整 */
.pagination {
  justify-content: center; /* 分页居中 */
}

/* 链接美化 */
a {
  color: #007bff;
}

a:hover {
  text-decoration: none;
  color: #0056b3;
}

.btn-outline-primary {
  margin: 0.5rem;
}
</style>


<script>
import store from '../store'
import Post from './Base/Post'
import Pagination from './Base/Pagination'
// bootstrap-markdown 编辑器依赖的 JS 文件，初始化编辑器在组件的 created() 方法中，同时它需要 JQuery 支持哦
import '../assets/bootstrap-markdown/js/bootstrap-markdown.js'
import '../assets/bootstrap-markdown/js/bootstrap-markdown.zh.js'
import '../assets/bootstrap-markdown/js/marked.js'


export default {
  name: 'Home',  //this is the name of the component
  components: {
    Post,
    Pagination
  },
  data () {
    return {
      sharedState: store.state,
      posts: '',
      categories: [],
      postForm: {
        title: '',
        summary: '',
        body: '',
        category_id: null,
        errors: 0,  // 表单是否在前端验证通过，0 表示没有错误，验证通过
        titleError: null,
        bodyError: null,
        categoryError: null,
      },
      editPostForm: {
        title: '',
        summary: '',
        body: '',
        errors: 0,  // 表单是否在前端验证通过，0 表示没有错误，验证通过
        titleError: null,
        bodyError: null
      }
    }
  },
  methods: {
    getPostsByCategory(categoryId) {
          let page = 1;
          let per_page = 5;
          if (typeof this.$route.query.page != 'undefined') {
            page = this.$route.query.page;
          }
          if (typeof this.$route.query.per_page != 'undefined') {
            per_page = this.$route.query.per_page;
          }
          const path = `/api/posts/?category_id=${categoryId}&page=${page}&per_page=${per_page}`;
          this.$axios.get(path)
            .then((response) => {
              this.posts = response.data;
            })
            .catch((error) => {
              console.error("Failed to load posts:", error);
            });
        },

    getCategories() {
      this.$axios.get('/api/categories')
        .then(response => {
          console.log("Categories loaded:", response.data); // 查看返回的数据
          this.categories = response.data; // 确保这是正确的数据结构
        })
        .catch(error => {
          console.error("Failed to load categories:", error);
        });
    },

    getPosts () {
      let page = 1
      let per_page = 5
      if (typeof this.$route.query.page != 'undefined') {
        page = this.$route.query.page
      }

      if (typeof this.$route.query.per_page != 'undefined') {
        per_page = this.$route.query.per_page
      }

      const path = `/api/posts/?page=${page}&per_page=${per_page}`
      this.$axios.get(path)
        .then((response) => {
          // handle success
          this.posts = response.data
        })
        .catch((error) => {
          // handle error
          console.log(error.response.data)
          this.$toasted.error(error.response.data.message, { icon: 'fingerprint' })
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
        // 给 bootstrap-markdown 编辑器内容添加警示样式，而不是添加到 #postFormBody 上
        $('#addPostForm .md-editor').closest('.form-group').addClass('u-has-error-v1')  // Bootstrap 4
      } else {
        this.postForm.bodyError = null
        $('#addPostForm .md-editor').closest('.form-group').removeClass('u-has-error-v1')
      }

      if (!this.postForm.title) {
        this.postForm.errors++
        this.postForm.titleError = 'Title is required.'
      } else {
        this.postForm.titleError = null
      }

      if (!this.postForm.category_id) {
        this.postForm.errors++
        this.postForm.categoryError = 'Category is required.'
      } else {
        this.postForm.categoryError = null
      }


      if (this.postForm.errors > 0) {
        // 表单验证没通过时，不继续往下执行，即不会通过 axios 调用后端API
        return false
      }

      const path = '/api/posts'
      const payload = {
        title: this.postForm.title,
        summary: this.postForm.summary,
        body: this.postForm.body,
        category_id: this.postForm.category_id // 确保这里使用了正确的字段
      };

      this.$axios.post(path, payload)
        .then((response) => {
          // handle success
          this.getPosts()
          this.$toasted.success('Successed add a new post.', { icon: 'fingerprint' })
          this.postForm.title = '',
          this.postForm.summary = '',
          this.postForm.body = '',
          console.log("Data fetched:", response.data);
        })
        .catch((error) => {
          // handle error
          for (var field in error.response.data.message) {
            if (field == 'title') {
              this.postForm.titleError = error.response.data.message[field]
            } else if (field == 'body') {
              this.postForm.bodyError = error.response.data.message[field]
            } else if (field == 'category') {
              this.postForm.categoryError = error.response.data.message[field]
            } else{
              this.$toasted.error(error.response.data.message[field], { icon: 'fingerprint' })
            }
          }
        })
    },
    onEditPost(post) {
      this.editPostForm = Object.assign({}, post, { category_id: post.category_id });
    },


    onSubmitUpdatePost () {
      this.editPostForm.errors = 0  // 重置
      // 每次提交前先移除错误，不然错误就会累加
      $('#editPostForm .form-control-feedback').remove()
      $('#editPostForm .form-group.u-has-error-v1').removeClass('u-has-error-v1')

      if (!this.editPostForm.title) {
        this.editPostForm.errors++
        this.editPostForm.titleError = 'Title is required.'
        // boostrap4 modal依赖jQuery，不兼容 vue.js 的双向绑定。所以要手动添加警示样式和错误提示
        $('#editPostFormTitle').closest('.form-group').addClass('u-has-error-v1')  // Bootstrap 4
        $('#editPostFormTitle').after('<small class="form-control-feedback">' + this.editPostForm.titleError + '</small>')
      } else {
        this.editPostForm.titleError = null
      }

      if (!this.editPostForm.body) {
        this.editPostForm.errors++
        this.editPostForm.bodyError = 'Body is required.'
        // boostrap4 modal依赖jQuery，不兼容 vue.js 的双向绑定。所以要手动添加警示样式和错误提示
        // 给 bootstrap-markdown 编辑器内容添加警示样式，而不是添加到 #postFormBody 上
        $('#editPostForm .md-editor').closest('.form-group').addClass('u-has-error-v1')  // Bootstrap 4
        $('#editPostForm .md-editor').after('<small class="form-control-feedback">' + this.editPostForm.bodyError + '</small>')
      } else {
        this.editPostForm.bodyError = null
      }

      if (this.editPostForm.errors > 0) {
        // 表单验证没通过时，不继续往下执行，即不会通过 axios 调用后端API
        return false
      }

      const path = `/api/posts/${this.editPostForm.id}`
      const payload = {
        title: this.editPostForm.title,
        summary: this.editPostForm.summary,
        body: this.editPostForm.body,
      }
      this.$axios.put(path, payload)
        .then((response) => {
          // 先隐藏 Modal
          $('#editPostModal').modal('hide')

          // handle success
          this.getPosts()
          this.$toasted.success('Successed update the post.', { icon: 'fingerprint' })
          this.editPostForm.title = '',
          this.editPostForm.summary = '',
          this.editPostForm.body = ''
        })
        .catch((error) => {
          // handle error
          for (var field in error.response.data.message) {
            if (field == 'title') {
              this.editPostForm.titleError = error.response.data.message[field]
              // boostrap4 modal依赖jQuery，不兼容 vue.js 的双向绑定。所以要手动添加警示样式和错误提示
              $('#editPostFormTitle').closest('.form-group').addClass('u-has-error-v1')  // Bootstrap 4
              $('#editPostFormTitle').after('<small class="form-control-feedback">' + this.editPostForm.titleError + '</small>')
            } else if (field == 'body') {
              this.editPostForm.bodyError = error.response.data.message[field]
              // boostrap4 modal依赖jQuery，不兼容 vue.js 的双向绑定。所以要手动添加警示样式和错误提示
              // 给 bootstrap-markdown 编辑器内容添加警示样式，而不是添加到 #postFormBody 上
              $('#editPostForm .md-editor').closest('.form-group').addClass('u-has-error-v1')  // Bootstrap 4
              $('#editPostForm .md-editor').after('<small class="form-control-feedback">' + this.editPostForm.bodyError + '</small>')
            } else {
              this.$toasted.error(error.response.data.message[field], { icon: 'fingerprint' })
            }
          }
        })
    },
    onResetUpdatePost () {
      // 先移除错误
      $('#editPostForm .form-control-feedback').remove()
      $('#editPostForm .form-group.u-has-error-v1').removeClass('u-has-error-v1')
      // 再隐藏 Modal
      $('#editPostModal').modal('hide')
      // this.getPosts()
      this.$toasted.info('Cancelled, the post is not update.', { icon: 'fingerprint' })
    },
    onDeletePost (post) {
      this.$swal({
        title: "Are you sure?",
        text: "该操作将彻底删除 [ " + post.title + " ], 请慎重",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, delete it!',
        cancelButtonText: 'No, cancel!'
      }).then((result) => {
        if(result.value) {
          const path = `/api/posts/${post.id}`
          this.$axios.delete(path)
            .then((response) => {
              // handle success
              this.$swal('Deleted', 'You successfully deleted this post', 'success')
              // this.$toasted.success('Successed delete the post.', { icon: 'fingerprint' })
              this.getPosts()
            })
            .catch((error) => {
              // handle error
              console.log(error.response.data)
              this.$toasted.error(error.response.data.message, { icon: 'fingerprint' })
            })
        } else {
          this.$swal('Cancelled', 'The post is safe :)', 'error')
        }
      })
    }
  },
  created () {
    this.getPosts()
    this.getCategories()
    // 初始化 bootstrap-markdown 插件
    $(document).ready(function() {
      $("#postFormBody, #editPostFormBody").markdown({
        autofocus:false,
        savable:false,
        iconlibrary: 'fa',  // 使用Font Awesome图标
        language: 'zh'
      })
    })
  },
  // 当查询参数 page 或 per_page 变化后重新加载数据
  beforeRouteUpdate (to, from, next) {
    // 注意：要先执行 next() 不然 this.$route.query 还是之前的
    next()
    this.getPosts()
  },
}
</script>
