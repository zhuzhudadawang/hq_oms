  <template>
    <div
      class="login-container"
      :style="{
        backgroundImage: `url(${bgImage})`
      }"
    >
      <!-- 右侧堆叠：站点 logo 在上，登录面板在下 -->
      <div class="right-block">
        <div class="site-logo">
          <img :src="logo" alt="site logo" />
          <div class="site-title">OMS</div>
        </div>

        <!-- 右侧玻璃面板登录框 -->
        <div class="login-panel" role="region">
        <img class="panel-decor" :src="loginBg2" alt="decor" />
        <div class="panel-header">
          <div class="panel-title">用户登录</div>
          <div class="panel-sub">USER LOGIN</div>
        </div>

        <el-form :model="loginForm" :rules="rules" ref="loginFormRef" class="login-form">
          <el-form-item prop="username">
            <el-input
              v-model="loginForm.username"
              placeholder="请输入用户名"
              prefix-icon="User"
              size="large"
            />
          </el-form-item>
          <el-form-item prop="password">
            <el-input
              v-model="loginForm.password"
              type="password"
              placeholder="请输入密码"
              prefix-icon="Lock"
              size="large"
              show-password
            />
          </el-form-item>
          <el-form-item>
            <el-button
              type="primary"
              size="large"
              :loading="loading"
              @click="handleLogin"
              class="login-button"
            >
              登录
            </el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
    </div>
  </template>

  <script setup>
  import { ref, reactive } from 'vue'
  import { useRouter, useRoute } from 'vue-router'
  import { ElMessage } from 'element-plus'
  import { useUserStore } from '@/stores/user'
  import bgImage from '@/assets/images/login-bg1.jpg'
  import logo from '@/assets/images/logo.png'
  import loginBg2 from '@/assets/images/login-bg2.svg'

  const router = useRouter()
  const route = useRoute()
  const userStore = useUserStore()
  const loginFormRef = ref(null)
  const loading = ref(false)

  const loginForm = reactive({
    username: '',
    password: ''
  })

  const rules = {
    username: [
      { required: true, message: '请输入用户名', trigger: 'blur' }
    ],
    password: [
      { required: true, message: '请输入密码', trigger: 'blur' },
      { min: 6, message: '密码长度不能小于6位', trigger: 'blur' }
    ]
  }

  const handleLogin = async () => {
    if (!loginFormRef.value) return
    
    await loginFormRef.value.validate(async (valid) => {
      if (valid) {
        loading.value = true
        
        try {
          // 调用登录 API
          await userStore.login(loginForm)
          
          ElMessage.success('登录成功')
          
          // 跳转到重定向页面或首页
          const redirect = route.query.redirect || '/'
          router.push(redirect)
        } catch (error) {
          console.error('登录失败:', error)
          // 错误提示已在 request.js 拦截器中处理，这里不再重复提示
        } finally {
          loading.value = false
        }
      }
    })
  }
  </script>

  <style lang="scss" scoped>
  .login-container {
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    position: relative;

    .right-block {
      position: absolute;
      right: 8%;
      top: 50%;
      transform: translateY(-50%);
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 18px;
      z-index: 3;
    }

    .site-logo {
      display: flex;
      align-items: center;
      gap: 12px;
      color: #ffffff;

      img {
        width: 96px;
        height: 96px;
        object-fit: contain;
        display: block;
      }

      .site-title {
        margin: 0;
        font-size: 24px;
        font-weight: 700;
        opacity: 0.98;
        line-height: 1;
      }
    }

    .login-panel {
    /* 由 .right-block 控制位置，面板保持静态布局 */
    width: 380px;
    padding: 26px 28px;
    border-radius: 8px;
    /* 更接近示例的深蓝半透明毛玻璃背景 */
    background: linear-gradient(180deg, rgba(6,30,56,0.46), rgba(6,20,44,0.28));
    border: 1px solid rgba(22,150,210,0.10);
    box-shadow: 0 12px 40px rgba(2,8,20,0.6), inset 0 1px 0 rgba(255,255,255,0.03);
    color: #e6f7ff;
    backdrop-filter: blur(10px) saturate(120%);

      .panel-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 18px;

        .panel-title {
          font-size: 18px;
          font-weight: 600;
        }
        .panel-sub {
          font-size: 12px;
          opacity: 0.6;
        }
      }

      .panel-decor {
        position: absolute;
        /* 放大并覆盖整个登录面板作为装饰背景 */
        left: -80px;
        top: -120px;
        width: 500px;
        height: 460px;
      }

      /* 确保表单和标题在装饰图之上 */
      .panel-header,
      .login-form {
        position: relative;
        z-index: 2;
      }
        .login-button {
          width: 100%;
          margin-top: 6px;
        }
      // }
    }
  }
  </style>
