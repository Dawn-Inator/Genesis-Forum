<template>
  <div class="settings-container container py-5">
    <div class="row">
      <!-- Profile Settings Sidebar -->
      <div class="col-lg-3 mb-5">
        <aside class="profile-settings-sidebar rounded-lg shadow p-3">
          <!-- Profile Picture -->
          <div v-if="user" class="text-center position-relative mb-4">
            <div class="profile-pic-wrapper mx-auto mb-3">
              <img class="img-fluid rounded-circle" :src="user._links.avatar" :alt="user.name || user.username">
            </div>
            <span class="d-block font-weight-bold">{{ user.name || user.username }}</span>
            <router-link :to="{ path: `/user/${sharedState.user_id}` }">
              <span class="profile-to-user-icon" title="Go To Your Profile">
                <i class="icon-finance-067"></i>
              </span>
            </router-link>
          </div>
          <!-- End Profile Picture -->

          <hr class="my-4">

          <!-- Profile Settings List -->
          <ul class="list-unstyled mb-0">
            <li class="py-2">
              <router-link :to="{ name: 'SettingProfile' }" class="settings-link">
                Profile
              </router-link>
            </li>
            <li class="py-2">
              <router-link :to="{ name: 'SettingAccount' }" class="settings-link">
                Account
              </router-link>
            </li>
            <li class="py-2">
              <router-link :to="{ name: 'SettingEmail' }" class="settings-link">
                Email
              </router-link>
            </li>
            <li class="py-2">
              <router-link :to="{ name: 'SettingNotification' }" class="settings-link">
                Notification
              </router-link>
            </li>
          </ul>
          <!-- End Profile Settings List -->
        </aside>
      </div>
      <!-- End Profile Settings Sidebar -->

      <!-- Main Content -->
      <div class="col-lg-9">
        <div class="settings-content rounded-lg shadow p-4">
          <router-view></router-view>
        </div>
      </div>
      <!-- End Main Content -->
    </div>
  </div>
</template>

<style scoped>
.settings-container {
  /* Optionally, you can add some styles for the container */
}

.profile-settings-sidebar,
.settings-content {
  background-color: #fff; /* White background */
  border: 1px solid #ddd; /* Light border */
}

.profile-settings-sidebar .profile-pic-wrapper {
  width: 100px;
  height: 100px;
  overflow: hidden;
}

.profile-to-user-icon {
  display: inline-block;
  width: 32px;
  height: 32px;
  background-color: #007bff;
  color: white;
  border-radius: 50%;
  text-align: center;
  line-height: 32px;
  position: absolute;
  top: -16px;
  right: 16px;
  cursor: pointer;
}

.settings-link {
  display: block;
  color: #333;
  padding: 10px 15px;
  border-radius: .25rem;
  transition: background-color .3s, color .3s;
}

.settings-link:hover, .settings-link.active {
  background-color: #007bff;
  color: #fff;
  text-decoration: none;
}
</style>


<script>
import store from '../../store'

export default {
  name: 'Settings',  //this is the name of the component
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
