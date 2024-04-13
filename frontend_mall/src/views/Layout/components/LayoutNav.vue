<script setup>
// import { useUserStore } from '@/stores/userStore'
import { useRouter } from 'vue-router'
import { useStore } from '@/stores/pStore'
import { ElMessage } from 'element-plus'
import { set } from '@vueuse/core'
import axios from 'axios'
import Cookies from 'js-cookie'

const store = useStore()

const logout = () => {
  

  axios.post('/api/logout', {
	}).then((res) => {
    console.log(res, 'res')
    store.set_user_id(0)
    store.set_role('')
    Cookies.remove('token')
    Cookies.remove('role')
    Cookies.remove('user_username')
    Cookies.remove('user_id')
    ElMessage({ type: 'success', message: 'Logout Success' })
    setTimeout(() => {
      location.reload(true);
    }, 350)
	}).catch((err) => {
    console.log(err, 'err')
    store.set_user_id(0)
    store.set_role('')
    Cookies.remove('token')
    Cookies.remove('role')
    Cookies.remove('user_username')
    Cookies.remove('user_id')
    ElMessage({ type: 'success', message: 'Logout Success' })
    setTimeout(() => {
      location.reload(true);
    }, 350)
	})
}

</script>

<template>
  <nav class="app-topnav">
    <div class="container">
      <ul>
        <!-- 多模版渲染 区分登录状态和非登录状态 -->

        <!-- 适配思路: 登录时显示第一块 非登录时显示第二块  是否有token -->
        <!-- <template v-if="userStore.userInfo.token">
          <li><a href="javascript:;"><i class=" iconfont icon-user"></i>{{ userStore.userInfo.account }}</a></li>
          <li>
            <el-popconfirm @confirm="confirm" title="Are you sure you want to log out?" confirm-button-text="confirm" cancel-button-text="cancel">
              <template #reference>
                <a href="javascript:;">Log out</a>
              </template>
            </el-popconfirm>
          </li>
          <li><a href="javascript:;">My Orders</a></li>
          <li><a href="javascript:;">Member Center</a></li>
        </template> -->
        <!-- <template v-else> -->

          <li><a href="javascript:;" @click="$router.push('/about-us')" >About Us</a></li>
          <li><a href="javascript:;" @click="$router.push('/recharge')" v-if="store.user_id != 0">Top-up</a></li>
          <li><a href="javascript:;" @click="$router.push('/member/order')" v-if="store.user_id != 0">My Orders</a></li>
          <li><a href="javascript:;" @click="$router.push('/login')" v-if="store.user_id == 0">Login</a></li>
          <li><a href="javascript:;" @click="$router.push('/register')" v-if="store.user_id == 0">Register</a></li>
          <li><a href="javascript:;" @click="$router.push('/user-info')" v-if="store.user_id != 0">Personal</a></li>
          <li><a href="javascript:;" @click="logout" v-if="store.user_id != 0">Logout</a></li>
          <li><p  >&emsp;&emsp;&emsp;&emsp;&emsp;</p></li>
        <!-- </template> -->
      </ul>
    </div>
  </nav>
</template>


<style scoped lang="scss">
.app-topnav {
  background: #333;

  ul {
    display: flex;
    height: 53px;
    justify-content: flex-end;
    align-items: center;

    li {
      a {
        padding: 0 15px;
        color: #cdcdcd;
        line-height: 1;
        display: inline-block;

        i {
          font-size: 14px;
          margin-right: 2px;
        }

        &:hover {
          color: $xtxColor;
        }
      }

      ~li {
        a {
          border-left: 2px solid #666;
        }
      }
    }
  }
}
</style>
