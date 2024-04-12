<template>
  <div class="container">
    <div class="profile-form-wrapper rounded-lg shadow-lg py-5 px-4">
      <h2 class="text-center mb-4">Edit Your Public Profile</h2>
      <form @submit.prevent="onSubmit">
        <div class="form-group">
          <label for="name" class="form-label">Real Name</label>
          <input type="text" v-model="profileForm.name" class="form-control" id="name" placeholder="Enter your real name">
        </div>
        <div class="form-group">
          <label for="location" class="form-label">Location</label>
          <input type="text" v-model="profileForm.location" class="form-control" id="location" placeholder="Enter your location">
        </div>
        <div class="form-group">
          <label for="about_me" class="form-label">About Me</label>
          <textarea v-model="profileForm.about_me" class="form-control" id="about_me" rows="5" placeholder="Tell us something about yourself"></textarea>
        </div>
        <div class="text-center mt-4">
          <button type="submit" class="btn btn-primary px-4">Save Changes</button>
        </div>
      </form>
    </div>
  </div>
</template>


<style scoped>
.profile-form-wrapper {
  background-color: #ffffff; /* 白色背景 */
  max-width: 600px; /* 表单最大宽度 */
  margin: 0 auto; /* 水平居中 */
  border: 1px solid #e3e3e3; /* 边框颜色 */
  border-radius: 0.5rem; /* 边框圆角 */
}

.form-label {
  font-size: 1.1rem; /* 标签字体大小 */
  color: #495057; /* 标签字体颜色 */
  font-weight: 500; /* 字体加粗 */
}

.form-control {
  border-radius: 0.25rem; /* 输入框圆角 */
  box-shadow: none; /* 移除输入框默认阴影 */
}

.form-control:focus {
  border-color: #80bdff; /* 输入框聚焦时边框颜色 */
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25); /* 输入框聚焦时的阴影效果 */
}

.btn-primary {
  font-size: 1rem; /* 按钮字体大小 */
  letter-spacing: 0.05rem; /* 字母间距 */
  border-radius: 2rem; /* 按钮圆角 */
}
</style>



<script>
import store from '../../store'

export default {
  name: 'Profile',  //this is the name of the component
  data () {
    return {
      sharedState: store.state,
      profileForm: {
        name: '',
        location: '',
        about_me: ''
      }
    }
  },
  methods: {
    getUser (id) {
      const path = `/api/users/${id}`
      this.$axios.get(path)
        .then((response) => {
          this.profileForm.name = response.data.name
          this.profileForm.location = response.data.location
          this.profileForm.about_me = response.data.about_me
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
        });
    },
    onSubmit (e) {
      const user_id = this.sharedState.user_id
      const path = `/api/users/${user_id}`
      const payload = {
        name: this.profileForm.name,
        location: this.profileForm.location,
        about_me: this.profileForm.about_me
      }
      this.$axios.put(path, payload)
        .then((response) => {
          // handle success
          this.$toasted.success('Successed modify your profile.', { icon: 'fingerprint' })
          this.$router.push({ path: `/user/${user_id}/overview` })
        })
        .catch((error) => {
          // handle error
          console.log(error.response.data)
          this.$toasted.error(error.response.data.message, { icon: 'fingerprint' })
        })
    },

  },
  created () {
    const user_id = this.sharedState.user_id
    this.getUser(user_id)
  }
}
</script>
