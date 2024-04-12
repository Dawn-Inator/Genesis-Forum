<template>

  <nav aria-label="Page Navigation">
    <ul class="list-inline">
      <li class="list-inline-item">
        <router-link v-bind:to="{ path: $route.fullPath, query: { page: curPage - 1, per_page: perPage }}" v-bind:class="{'u-pagination-v1__item--disabled': curPage == 1}" class="u-pagination-v1__item u-pagination-v1-1 g-rounded-50 g-pa-12-21" aria-label="Previous">
          <span aria-hidden="true">
            <i class="fa fa-angle-left"></i>
          </span>
          <span class="sr-only">Previous</span>
        </router-link>
      </li>

      <li v-if="page != 'NaN'" v-for="(page, index) in iter_pages" v-bind:key="index" class="list-inline-item g-hidden-sm-down">
        <router-link v-bind:to="{ path: $route.fullPath, query: { page: page, per_page: perPage }}" v-bind:class="{'u-pagination-v1-1--active': $route.query.page == page || (!$route.query.page && page == 1)}" class="u-pagination-v1__item u-pagination-v1-1 g-rounded-50 g-pa-12-19">{{ page }}</router-link>
      </li>
      <li v-else class="list-inline-item g-hidden-sm-down">
        <span class="g-pa-12-19">...</span>
      </li>

      <li class="list-inline-item">
        <router-link v-bind:to="{ path: $route.fullPath, query: { page: curPage + 1, per_page: perPage }}" v-bind:class="{'u-pagination-v1__item--disabled': curPage == totalPages || totalPages == 0 }" class="u-pagination-v1__item u-pagination-v1-1 g-rounded-50 g-pa-12-21" aria-label="Next">
          <span aria-hidden="true">
            <i class="fa fa-angle-right"></i>
          </span>
          <span class="sr-only">Next</span>
        </router-link>
      </li>
      <li class="list-inline-item float-right">
        <span class="u-pagination-v1__item-info g-pa-12-19">Page {{ curPage }} of {{ totalPages }}</span>
      </li>
    </ul>
  </nav>

</template>

<style scoped>
/* 分页导航样式 */
.pagination-container {
  text-align: center; /* 居中分页导航 */
}

.u-pagination-v1__item {
  border: none; /* 移除边框 */
  background-image: linear-gradient(120deg, #89f7fe 0%, #66a6ff 100%); /* 用梯度背景 */
  color: #fff; /* 白色文字 */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* 添加阴影 */
  transition: all 0.3s ease; /* 平滑过渡效果 */
  cursor: pointer;
}

.u-pagination-v1__item--disabled {
  background-color: #ccc; /* 禁用状态的背景色 */
  color: #666; /* 禁用状态的文字颜色 */
  cursor: not-allowed; /* 禁用状态的鼠标样式 */
  pointer-events: none; /* 禁用点击事件 */
}

.u-pagination-v1__item--active {
  background-image: linear-gradient(120deg, #f6d365 0%, #fda085 100%); /* 活跃状态的梯度背景 */
  font-weight: bold; /* 加粗文字 */
}

.u-pagination-v1__item:hover {
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2); /* 鼠标悬停的阴影效果 */
  transform: translateY(-2px); /* 鼠标悬停时轻微上移 */
}

/* 额外的信息标签样式 */
.u-pagination-v1__item-info {
  background-color: #f0f0f0; /* 背景色 */
  color: #333; /* 文字颜色 */
  padding: 0.5rem 1rem; /* 内边距 */
  border-radius: 20px; /* 圆角 */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* 阴影 */
}
</style>

<script>
export default {
  name: 'Pagination',  // this is the name of the component
  props: {
    curPage: {
      required: true
    },
    perPage: {
      default: 3
    },
    totalPages: {
      required: true
    },
    leftPages: {
      default: 2
    },
    rightPages: {
      default: 2
    }
  },
  computed: {
    iter_pages: function () {
      // 构建分页导航，当前页左、右两边各显示2页，比如  1, 2, ... 7, 8, 9, 10, 11 ... 30, 31
      let arr = [1, 2]
      for (var i = this.leftPages; i > 0; i--) {
        arr.push(this.curPage - i)
      }
      arr.push(this.curPage)
      for (var i = 1; i <= this.rightPages; i++) {
        arr.push(this.curPage + i)
      }
      arr.push(this.totalPages - 1)
      arr.push(this.totalPages)


      // 小于1，或大于最大页数的都是非法的，要去除
      arr = arr.filter(item => item > 0 && item <= this.totalPages)
      // 去除重复项
      arr = [...new Set(arr)]
      // 假设当前页为1，总页数为6或6以上时，在倒数第2个位置插入特殊标记  1, 2, 3 ... 5, 6
      if (this.curPage + this.rightPages < this.totalPages - 2) {
        arr.splice(-2, 0, 'NaN')
      }
      // 当前页为6或6以上时，在第3个位置插入特殊标记  1, 2 ... 4, 5, 6
      if (this.curPage - this.leftPages - 1 > 2) {
        arr.splice(2, 0, 'NaN')
      }

      return arr
    }
  }
}
</script>
