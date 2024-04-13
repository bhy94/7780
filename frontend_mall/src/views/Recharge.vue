<script setup>


import { ref } from 'vue'

import { ElMessage } from 'element-plus'
import 'element-plus/theme-chalk/el-message.css'
import { useRouter } from 'vue-router'
import { useStore } from '@/stores/pStore'
import axios from 'axios'
import Cookies from 'js-cookie'
import { onMounted } from 'vue'
import { set } from '@vueuse/core'

const store = useStore()

// 1. 准备表单对象


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
  } else {
    router.push('/login')
  }
})


const balance_add = ref('')



// 3. 获取form实例做统一校验

const router = useRouter()

const deposit = () => {
  if (balance_add.value == '') {
    ElMessage({ type: 'warning', message: 'Please enter the amount to top-up!' })
    return
  } else if (isNaN(balance_add.value)) {
    ElMessage({ type: 'error', message: 'Please enter a valid number!' })
    return
  } else {
    paypal.Buttons({
        createOrder: function(data, actions) {
            return actions.order.create({
                purchase_units: [{
                    amount: {
                        value: balance_add.value // Set up the transaction amount here
                    }
                }]
            });
        },
        onApprove: function(data, actions) {
            // This function captures the funds from the transaction.
            return actions.order.capture().then(function(details) {
                console.log(details, 'details')
                axios.post('/api/users/deposit', {
                  user_id: store.user_id,
                  balance_add: balance_add.value,
                  pporder_id: details.id
                })
                .then((res) => {
                  console.log(res, 'res')
                  if (res.data.code == 200 && res.data.data.success == 1) {
                    ElMessage({ type: 'success', message: 'Top-up Success' })
                  } else {
                    throw new Error('Top-up Failed')
                  }
                }).catch((err) => {
                  console.log(err, 'err')
                  ElMessage({ type: 'error', message: 'Top-up Failed' })
                })
                setTimeout(() => {
                  location.reload()
                }, 2000)
            });
        },
        oncancel: function(data, actions) {
            return actions.order.cancel().then(function(details) {
              location.reload()
            });
        },
        onError: function(err) {
            // 刷新页面
            location.reload()
        },
        onabort: function(data, actions) {
            return actions.order.abort().then(function(details) {
              location.reload()
            });
        } 
    }).render('#paypal-button-container');
  }
}

// const deposit1 = () => {
//   // 调用实例方法
//   console.log(balance_add.value)
//   if (balance_add.value == '') {
//     ElMessage({ type: 'warning', message: 'Please enter the amount to top-up!' })
//     return
//   } else if (isNaN(balance_add.value)) {
//     ElMessage({ type: 'error', message: 'Please enter a valid number!' })
//     return
//   } else {
//     console.log(store.user_id, 'store.user_id')
    
//   }
// }

// 1. 用户名和密码 只需要通过简单的配置（看文档的方式 - 复杂功能通过多个不同组件拆解）
// 2. 同意协议  自定义规则  validator:(rule,value,callback)=>{}
// 3. 统一校验  通过调用form实例的方法 validate -> true
</script>


<template>
  <div>
    <header class="login-header">
      <div class="container m-top-20">
        <h1 class="logo">
          <RouterLink to="/">GROUP29-7780</RouterLink>
        </h1>
        <RouterLink class="entry" to="/">
          Homepage
          <i class="iconfont icon-angle-right"></i>
          <i class="iconfont icon-angle-right"></i>
        </RouterLink>
      </div>
    </header>
    <div style="width: 100vw;height:80vh;display:flex;min-height:500px">
      <section class="login-section">
        <div class="wrapper">
          <nav>
            <a href="">Deposit</a>
          </nav>
          <div class="account-box">
            <div class="form">
              <el-form  label-position="right" label-width="80px" status-icon>
                <el-form-item prop="balance_add" label="Top-up">
                  <el-input v-model="balance_add" />
                </el-form-item>
                <el-button size="large" class="subBtn" @click="deposit">Create Top-up Link!</el-button>
              </el-form>
            </div>
          </div>
          <div id="paypal-button-container">
          </div>
        </div>
      </section>
    </div>
    

    <footer class="login-footer">
      <div class="container">
        <p>CopyRight &copy; GROUP29-7780</p>
      </div>
    </footer>
  </div>
</template>

<style scoped lang='scss'>
.login-header {
  background: #fff;
  border-bottom: 1px solid #e4e4e4;

  .container {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
  }

  .logo {
    width: 200px;

    a {
      display: block;
      height: 132px;
      width: 100%;
      text-indent: -9999px;
      background: url("@/assets/logo.png") no-repeat center 18px / contain;
    }
  }

  .sub {
    flex: 1;
    font-size: 24px;
    font-weight: normal;
    margin-bottom: 38px;
    margin-left: 20px;
    color: #666;
  }

  .entry {
    width: 120px;
    margin-bottom: 38px;
    font-size: 16px;

    i {
      font-size: 14px;
      color: $xtxColor;
      letter-spacing: -5px;
    }
  }
}

.login-section {
  height: 488px;
  position: relative;

  .wrapper {
    width: 380px;
    background: #fff;
    position: absolute;
    left: 60%;
    top: 54px;
    transform: translate3d(100px, 0, 0);
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.15);

    nav {
      font-size: 14px;
      height: 55px;
      margin-bottom: 20px;
      border-bottom: 1px solid #f5f5f5;
      display: flex;
      padding: 0 40px;
      text-align: right;
      align-items: center;

      a {
        flex: 1;
        line-height: 1;
        display: inline-block;
        font-size: 18px;
        position: relative;
        text-align: center;
      }
    }
  }
}

.login-footer {
  padding: 30px 0 50px;
  background: #fff;

  p {
    text-align: center;
    color: #999;
    padding-top: 20px;

    a {
      line-height: 1;
      padding: 0 10px;
      color: #999;
      display: inline-block;

      ~a {
        border-left: 1px solid #ccc;
      }
    }
  }
}

.account-box {
  .toggle {
    padding: 15px 40px;
    text-align: right;

    a {
      color: $xtxColor;

      i {
        font-size: 14px;
      }
    }
  }

  .form {
    padding: 0 20px 20px 20px;

    &-item {
      margin-bottom: 28px;

      .input {
        position: relative;
        height: 36px;

        >i {
          width: 34px;
          height: 34px;
          background: #cfcdcd;
          color: #fff;
          position: absolute;
          left: 1px;
          top: 1px;
          text-align: center;
          line-height: 34px;
          font-size: 18px;
        }

        input {
          padding-left: 44px;
          border: 1px solid #cfcdcd;
          height: 36px;
          line-height: 36px;
          width: 100%;

          &.error {
            border-color: $priceColor;
          }

          &.active,
          &:focus {
            border-color: $xtxColor;
          }
        }

        .code {
          position: absolute;
          right: 1px;
          top: 1px;
          text-align: center;
          line-height: 34px;
          font-size: 14px;
          background: #f5f5f5;
          color: #666;
          width: 90px;
          height: 34px;
          cursor: pointer;
        }
      }

      >.error {
        position: absolute;
        font-size: 12px;
        line-height: 28px;
        color: $priceColor;

        i {
          font-size: 14px;
          margin-right: 2px;
        }
      }
    }

    .agree {
      a {
        color: #069;
      }
    }

    .btn {
      display: block;
      width: 100%;
      height: 40px;
      color: #fff;
      text-align: center;
      line-height: 40px;
      background: $xtxColor;

      &.disabled {
        background: #cfcdcd;
      }
    }
  }

  .action {
    padding: 20px 40px;
    display: flex;
    justify-content: space-between;
    align-items: center;

    .url {
      a {
        color: #999;
        margin-left: 10px;
      }
    }
  }
}

.subBtn {
  background: $xtxColor;
  width: 100%;
  color: #fff;
}
</style>
