<script setup>
import { onMounted } from 'vue'
import Cookies from 'js-cookie'
import { useStore } from '@/stores/pStore'

const store = useStore()

onMounted(() => {
  let token = Cookies.get("token")
  let role = Cookies.get("role")
  let user_username = Cookies.get("user_username")
  let user_id = Cookies.get("user_id")
  let token_is_string = typeof token === 'string'
  console.log(role == 'user' || token_is_string)
  if (role == 'user' || token_is_string) {
    store.set_role(role)
    store.set_user_id(user_id)
  }
  console.log(store.user_id)
})
</script>

<template>
  <div class="container">
    <div class="xtx-member-aside">
      <div class="user-manage">
        <!-- <h4>My account</h4>
        <div class="links">
          <RouterLink to="/member">Person center</RouterLink>
        </div> -->
        <h4>Deal Manage</h4>
        <div class="links">
          <RouterLink to="/member/order">My order</RouterLink>
        </div>
      </div>
    </div>
    <div class="article">
      <!-- 三级路由的挂载点 -->
      <RouterView />
    </div>
  </div>
</template>

<style scoped lang="scss">
.container {
  display: flex;
  padding-top: 20px;

  .xtx-member-aside {
    width: 220px;
    margin-right: 20px;
    border-radius: 2px;
    background-color: #fff;

    .user-manage {
      background-color: #fff;

      h4 {
        font-size: 18px;
        font-weight: 400;
        padding: 20px 52px 5px;
        border-top: 1px solid #f6f6f6;
      }

      .links {
        padding: 0 52px 10px;
      }

      a {
        display: block;
        line-height: 1;
        padding: 15px 0;
        font-size: 14px;
        color: #666;
        position: relative;

        &:hover {
          color: $xtxColor;
        }

        &.active,
        &.router-link-exact-active {
          color: $xtxColor;

          &:before {
            display: block;
          }
        }

        &:before {
          content: '';
          display: none;
          width: 6px;
          height: 6px;
          border-radius: 50%;
          position: absolute;
          top: 19px;
          left: -16px;
          background-color: $xtxColor;
        }
      }
    }
  }

  .article {
    width: 1000px;
    background-color: #fff;
  }
}
</style>
