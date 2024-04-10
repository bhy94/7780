# GROUP25-7640

#### 目录
- 分组
- 功能简述
- 前端设计参考
- 后端设计参考
- 对象设计参考
- [API设计](https://github.com/GoodManWEN/GOUP25-7640/blob/main/docs/api_design.md)
- [设计图参考](https://github.com/GoodManWEN/GOUP25-7640/blob/main/docs/previews.md)

## 分组
需求制作使用mysql的网页应用（多商家/多用户商城），前后分离

1. 书面文件，文档，ER图等：温
2. 前端：陈，周
3. 后端：RICK，刘

## 功能简述

1. 用户注册、用户登录
2. 商家注册、商家登录
3. 超级管理员写死（后端配置文件提供）
5. 用户查看商品
6. 用户添加购物车
7. 用户购买商品
8. 用户充值
9. 用户在某些订单状态下可以取消中的某些商品
10. 用户在某些订单状态下可以取消订单
11. 后台商家添加商品
12. 后台商家删除商品
13. 后台商家取消订单
14. 超级管理员新增、删除用户
15. 超级管理员新增、删除商家

##### 总体原则
1. 假设代码完全在合法条件下运行
2. 健壮性满足合法情况即可
3. 关联性由数据库维护，不考虑强同步
4. 请保证代码质量不要无法code review
5. 所有涉及图片的，不维护二进制存储，一律储存图片url字符串
6. 货币系统：设计用户可以通过特定API充值平台虚拟货币，而后货币和退款等一系列操作由系统内部维护，超级管理员可以打破买卖货币平衡规则。

## 前端设计参考

- 总体设计：使用H5技术，同时搞定响应式，Vue/React工程化，选定合适组件库节省开发时间。
- 编译后文件打包至一个单独的html+css+js文件，放置于后端assets
- 用户可以浏览商品，商家有管理后台，可以添加商品。
- 技术栈举例：Vite + Vue3 + Pinia + ElementPlus

### 视图

##### 前台项目

1. 主页视图：导航栏、直接显示商品列表、搜索框。
2. 登录页面：允许用户注册/登录。 
3. 商品页面：展示商品详情（富文本），添加至购物车。
4. 购物车（付款）页面：查看所有已添加商品（购物车状态完全由前端维护）。
5. 充值页面：一个input框和一个按钮，input输入100后点击充值即可为用户账户充值100元。
7. 用户个人资料视图： 展示用户基础信息。
8. 用户订单页面：展示所有个人订单，可取消未shipping订单。

##### 后台项目

1. 商户商品管理： 商品列表，可以删除商品。
2. 商户添加商品视图。
3. 商户订单追踪： 订单列表，添加订单、删除订单。
4. 超级管理员：用户列表、删除用户。
5. 超级管理员添加用户。

### 主要组件

前端自行维护

### 其他补充

- 路由守卫、不同用户级别的前段权限拦截。
- 可能需要自建开发服务器。
- 用户token储存在cookie
- 登录后所有请求要带token

## 后端设计参考

- 总体设计：短周期后端，降低项目工程化复杂度
- 由于不需要复杂鉴权和状态维护等一系列中间件，推荐使用毛坯房框架（直接写某路由对应某逻辑），不使用SpringBoot/Django
- 技术栈举例：Python + FastAPI/Flask + aiomysql/pymysql

### 主要表
用户表
```
users(
  user_id,                         // 自增主键，下同
  user_username, 
  user_password,                   // hash+salt简单防脱裤模式，细节由后端自行维护
  user_display_name,
  telephone_number,
  address,
  avatar,
  balance                          // 虚拟货币余额
)
```

商户表
```
vendors(
  vendor_id,               
  vendor_username,
  vendor_password,                // hash+salt简单防脱裤模式，细节由后端自行维护
  vendor_display_name,
  origin_address,
  vendor_score,                   // 所有商品的评分合计，数据库事务或者业务端维护更新。
  avatar,
  balance                         // 虚拟货币余额
)
```

商品表
``` 
products(
  product_id,
  product_name,
  product_cover,
  product_info,
  product_score,                  // 商品评分，数据库事务或者业务端维护更新。
  price
)
```

订单表
```
orders(
  order_id,
  user_id,
  parent_order_id,               // 由于一个订单可以包含多个项目，实际上实现上是包含多个子订单
                                 // orders存在深度为1的父子关系。
                                 // 业务上需要维护父子订单状态一致性。
  product_id,
  quantity,
  total_price,
  place_time,
  status                         // CHAR(10)
  express_number                 // 快递单号
)
```

标签表
```
tags(
  tag_id,
  tag_name
)
```

多对多关系维护
```
tag_product_rel(
  tp_rel_id,
  tag_id,
  product_id
)

vendor_product_rel(
  vp_rel_id,
  vendor_id,
  product_id
)
```

登录状态
```
login_status_user(
  lsu_id,
  user_id,
  token,
  expire_time            // 考虑测试服务器的业务简单性，只设置过期时间，不维护过期行为。
)

login_status_vendor(
  lsv_id,
  vendor_id,
  token,
  expire_time            
)

login_status_admin(
  lsa_id,
  token,
  expire_time
)
```

### 其他补充
路由鉴权

## 对象设计参考

#### 商品主要属性

- 标题
- 图片（不维护二进制存储系统，一律要求互联网url格式）
- 描述
- 标签
- 售价
- 评分

#### 用户主要属性

- 用户名
- 密码
- 显示名
- 头像（不维护二进制存储系统，一律要求互联网url格式，有开源avatarAPI）
- 涉及订单
- 收货地址
- 电话号码

#### 商户主要属性

- 用户名
- 密码
- 显示名
- 头像
- 发货地
- 评分

#### 订单状态
分为
- 已创建（placed）
- 已付款（paid）
- 已发货（shipping）
- 已收货（finished）
  
已创建和已付款状态下商户和用户都可以取消订单。

#### 权限级别

- 前端分为前台后台，各自维护两个权限不互通的项目。
- 后台有管理员级和普通商户
- 管理员可以删除任意商户和用户（并删除所有相关订单或商品记录）
- 商户无法删除尚存有未完成订单的商品。
- 按上述规则，应存在无法链接到商品的订单（可以统一指向一个商品已删除的商品），不存在其他空链接。

## 关系型/数据库创建命令
略，后端出

