<template>
  <div class="user-info-section">
    <!-- Username -->
    <div class="user-name">
      <h2 class="g-font-weight-300 g-mr-10">{{ user.name || user.username }}</h2>
    </div>
    <!-- End Username -->

    <!-- Member since and Last seen -->
    <div class="user-timings">
      <h4 v-if="user.member_since" class="g-font-weight-300 g-mb-10">
        <i class="icon-badge g-pos-rel g-top-1 g-mr-5"></i> Member since: {{ $moment(user.member_since).format('LLL') }}
      </h4>
      <h4 v-if="user.last_seen" class="g-font-weight-300 g-mb-10">
        <i class="icon-eye g-pos-rel g-top-1 g-mr-5"></i> Last seen: {{ $moment(user.last_seen).fromNow() }}
      </h4>
    </div>
    <!-- End Member since and Last seen -->

    <!-- User Info -->
    <ul class="list-inline user-info">
      <li class="list-inline-item g-mr-20">
        <i class="icon-check g-pos-rel g-top-1 g-mr-5"></i> Verified User
      </li>
      <li v-if="user.email" class="list-inline-item g-mr-20">
        <i class="icon-link g-pos-rel g-top-1 g-mr-5"></i> <a class="email-link" v-bind:href="'mailto:' + user.email">{{ user.email }}</a>
      </li>
    </ul>
    <!-- End User Info -->

    <!-- Location -->
    <div class="user-location">
      <h4 v-if="user.location" class="g-font-weight-300 g-mb-10">
        <i class="icon-location-pin g-pos-rel g-top-1 g-mr-5"></i> {{ user.location }}
      </h4>
    </div>
    <!-- End Location -->

    <!-- About Me -->
    <div v-if="user.about_me" class="user-about">
      <p>{{ user.about_me }}</p>
    </div>
    <!-- End About Me -->
  </div>
</template>

<style scoped>
.user-info-section {
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.user-name h2 {
  color: #007bff; /* 主题颜色 */
  font-size: 24px;
}

.user-timings h4 {
  color: #666;
  font-size: 16px;
}

.user-info {
  padding-top: 15px;
}

.user-info i {
  color: #28a745; /* Bootstrap success color for icons */
}

.email-link {
  color: #007bff; /* 主题颜色 */
  text-decoration: none;
}

.email-link:hover {
  text-decoration: underline;
}

.user-location h4 {
  color: #17a2b8; /* Bootstrap info color */
}

.user-about p {
  background-color: #fff;
  border-left: 4px solid #007bff;
  padding: 10px;
  color: #666;
  font-style: italic;
}
</style>


<script>
export default {
  name: 'Overview',  //this is the name of the component
  data () {
    return {
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
    const user_id = this.$route.params.id
    this.getUser(user_id)
  },
  // 进入子路由后重新加载数据
  beforeRouteUpdate (to, from, next) {
    next()
    this.getUser(to.params.id)
  }
}
</script>
