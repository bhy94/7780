<script setup>


// 表单校验（账号名+密码）

import { ref } from 'vue'

import { ElMessage } from 'element-plus'
import 'element-plus/theme-chalk/el-message.css'
import { useRouter } from 'vue-router'
import axios from 'axios'

// 1. 准备表单对象
const form = ref({
  account: '',
  password: '',
  agree: true
})

// 2. 准备规则对象
const rules = {
  account: [
    { required: true, message: '用户名不能为空', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '密码不能为空', trigger: 'blur' },
    { min: 1, max: 14, message: '密码长度为6-14个字符', trigger: 'blur' },
  ],
  agree: [
    {
      validator: (rule, value, callback) => {
        console.log(value)
        // 自定义校验逻辑
        // 勾选就通过 不勾选就不通过
        if (value) {
          callback()
        } else {
          callback(new Error('请勾选协议'))
        }
      }
    }
  ]
}

// 3. 获取form实例做统一校验
const formRef = ref(null)
const router = useRouter()
const doRegister = () => {
  // const { account, password } = form.value
  let { user_username, user_password, user_display_name, address, avatar, telephone_number } = form.value

  if (user_username == undefined) {
    user_username = ''
  }
  if (user_password == undefined) {
    user_password = ''
  }
  if (user_display_name == undefined) {
    user_display_name = ''
  }
  if (address == undefined) {
    address = ''
  }
  if (avatar == undefined) {
    avatar = ''
  }
  if (telephone_number == undefined) {
    telephone_number = ''
  }

  if (user_username == '' || user_password == '' || user_display_name == '' || address == '' || avatar == '' || telephone_number == '') {
    // ElMessage.error('Please fill in all the information')
    ElMessage({ type: 'warning', message: 'Please fill in all the information' })
    return 
  } else {
    axios.post('/api/register', {
    user_username: user_username,
    user_password: user_password,
    user_display_name: user_display_name,
    address: address,
    avatar: avatar,
    telephone_number: telephone_number
  })
  .then((resp) => {
    if (resp.data.code == 200 && resp.data.data.success == 1) {
      ElMessage({ type: 'success', message: 'Register Success' })
      .then(() => {
        form.value.user_username = ''
        form.value.user_password = ''
        form.value.user_display_name = ''
        form.value.address = ''
        form.value.avatar = ''
        form.value.telephone_number = ''
      })
      .catch(() => {
        throw new Error('Submit Fail!')
      })
    } else {
      ElMessage({ type: 'error', message: 'Register Fail!' })
      .then(() => {
      })
      .catch(() => {
      })
    }
  })
  }
}

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
    <section class="login-section">
      <div class="wrapper">
        <nav>
          <a href="javascript:;">Register</a>
        </nav>
        <div class="account-box">
          <div class="form">
            <el-form ref="formRef" :model="form" label-position="right" label-width="80px" status-icon>
              <el-form-item prop="user_username" label="Account">
                <el-input v-model="form.user_username" />
              </el-form-item>
              <el-form-item prop="user_password" label="Password" >
                <el-input v-model="form.user_password" type="password" />
              </el-form-item>
              <el-form-item prop="user_display_name" label="Display">
                <el-input v-model="form.user_display_name" />
              </el-form-item>
              <el-form-item prop="address" label="Address">
                <el-input v-model="form.address" />
              </el-form-item>
              <el-form-item prop="avatar" label="Avatar">
                <el-input v-model="form.avatar" />
              </el-form-item>
              <el-form-item prop="telephone_number" label="Phone">
                <el-input v-model="form.telephone_number" />
              </el-form-item>
              <el-button size="large" class="subBtn" @click="doRegister">Click to Register</el-button>
            </el-form>
          </div>
        </div>
      </div>
    </section>

    <footer class="login-footer">
      <div class="container">
        <p>
          <a href="javascript:;">About Us</a>
          <a href="javascript:;">Help Center</a>
          <a href="javascript:;">After-sales Service</a>
          <a href="javascript:;">Delivery and Acceptance</a>
          <a href="javascript:;">Business Cooperation</a>
          <a href="javascript:;">Search Recommendations</a>
          <a href="javascript:;">Friendly Links</a>
        </p>
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
    left: 50%;
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
