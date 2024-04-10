## API设计

##### 1. 用户登录 // 前后台通用接口

- URL：`/api/login`
- 方法：POST
- 请求参数：
```js
{
  "username": "string",
  "password": "string",
  "destination": Literal["back_end", "front_end"] 
}
```
- 响应：
```js
{
  "code": 200,               // 一般只返回200/304/403/404/503
  "data": {
    "success": 1,  
    "message": "登录成功",    // 大多数情况下留空
    "user_id": 1,
    "vendor_id": 1,          // user_id和vendor_id两者只有一个有值
    "token": "md5string",    // 服务器生成令牌
    "role": "vendor",        // Literal["customer", "vendor", "admin"]
  }
}
```

##### 2. 用户登出

- URL：`/api/logout`
- 方法：POST
- 请求参数：
```js
{
  "user_id": 1,              // token应携带在cookies里一起发送，下同。 
}
```
- 响应：
```js
{
  "code": 200,
  "data": {
    "sucecss": 1,
    "message": "登出成功",    // 
  }
}
```

##### 3. 前台请求商品列表

- URL：`/api/products`
- 方法：POST
- 请求参数：`tags: string`
```js
{
  "tags": "自行车, 洗衣机, 冰箱, 彩电, 红的"     // 拆分逻辑后端处理，留空返回所有商品，前端可做翻页。
  "vendor_id": 10,                            // 第二维筛选范围
}
```
- 响应：
```js
{
  "code": 200,
  "data": {
    "success": 1,
    "message": "",   
    "products": [
      {"product_name": "小米手机", "product_cover": "https://1.jpg", "price": 60},
      {"product_name": "苹果手机", "product_cover": "https://2.jpg", "price": 90},
    ]
  }
}
```

##### 4. 前台请求商品详细信息
- URL：`/api/products/info`
- 方法：GET
- 请求参数：
```js
{
  product_id: 10        // 完整链接为/api/products/info?product_id=10
}
```
- 响应：
```js
{
  "code": 200,
  "data": {
    "success": 1,
    "message": "",  
    "product_id": 10,
    "product_name": "小米手机",
    "product_cover": "https://a.b.com/1.jpg",
    "product_info": "遥遥领先\n余承东.jpg"
    "tags": ["小米", "手机", "红色"],
    "price": 60,
    "origin_address":,
    "score": 4.5                                    // out of 5
  }
}
```


##### 5. 前台用户下单
- URL：`/api/users/orders/create`
- 方法：POST
- 请求参数：
```js
{
  "user_id": 12,
  "items": [
    {
      "product_id": 24,
      "quantity": 6
    },
    {
      "product_id": 25,
      "quantity": 1              // 接口遵循该规范。由于前端已设计购物车，实际上后端需要执行1-n次创建订单操作
    },
  ]
}
```
- 响应：
```js
{
  "code": 200,
  "data": {
    "success": 1,
    "message": ""
  }
}
```

##### 6. 前台用户付款
- URL：`/api/payments/pay`
- 方法：POST
- 请求参数：
```js
{
  "user_id": 12,
  "order_id": 66
}
```
- 响应：
```js
{
  "code": 200,
  "data": {
    "success": 1,                       // 后端要检查用户余额扣款是否成功
    "message": ""
  }
}
```

##### 7. 前台用户请求个人信息列表
- URL：`/api/users/info`
- 方法：GET
- 请求参数：
  ```js
{
  user_id: 10        // 完整链接为/api/users/info?user_id=10
}
```
- 响应：
```js
{
  "code": 200,
  "data": {
    "success": 1,
    "message": "",  
    "user_id": 12,
    "user_display_name": "foo",
    "avatar": "https://123.jpg",
    "address": "东胜神洲傲来国花果山水帘洞",
    "telephone_number": 13888888888
  }
}
```

##### 8. 前台用户请求订单列表
- URL：`/api/users/orders`
- 方法：POST
- 请求参数：
```js
{
  "user_id": 12
}
```
- 响应：`code: int`, `message: string`, `data: {}`
```js
{
  "code": 200,
  "data": {
    "success": 1,
    "message": "",
    "orders": [
      {
        "order_id": 10,
        "product_id": 13,
        "order_status": "shipping",
        "place_time": '2024-02-29 00:00:00',
        "quantity": 6,
        "total_price": 10.22,
        "parent_order_id": 9
      },
      {...}  
    ]
  }
}
```

##### 9. 前台用户取消订单
- URL：`/api/users/orders/delete`
- 方法：POST
- 请求参数：
```js
{
  "user_id": 12,
  "order_id": 3
}
```
- 响应：
```js
{
  "code": 200,
  "data": {
    "success": 1,                       // 后端有成功失败检查
    "message": "",   
  }
}
```

##### 10. 前台用户充值
- URL：`/api/users/deposit`
- 方法：POST
- 请求参数：
```js
{
  "user_id": 12,
  "balance_add": 100,                  // 要求非负
}
```
- 响应：
```js
{
  "code": 200,
  "data": {
    "success": 1,                       
    "message": "",   
  }
}
```


##### 11. 后台商户请求个人商品列表

- URL：`/api/vendors/products`
- 方法：POST
- 请求参数：
```js
{
  "vendor_id": 10
}
```
- 响应：
```js
{
  "code": 200,
  "message": "",   
  "data": {
    "success": 1,
    "message": "",   
    "list": [
      {
        "product_id": 10,
        "product_name": "小米手机",
        "product_cover": "https://1.jpg",
        "product_info",
        "tags": ["小米", "手机", "红色"],
        "price": 60,
        "score": 4.5
      },
      {...},
      {...}
    ]
  }
}
```


##### 12. 后台商户添加商品

- URL：`/api/vendors/products/create`
- 方法：POST
- 请求参数：
```js
{
  "vendor_id": 10,
  "product_name": "小米手机2",
  "product_cover": "https://1.jpg",
  "product_info": "**雷军**\n金凡",
  "tags": ["小米", "手机", "红色"],
  "price": 62
}
```
- 响应：
```js
{
  "code": 200,
  "data": {
    "success": 1,
    "message": "",   
    "product_id": 13
  }
}
```

##### 13. 后台商户删除商品

- URL：`/api/vendors/products/delete`
- 方法：POST
- 请求参数：
```js
{
  "vendor_id": 10,
  "product_id": 13
}
```
- 响应：
```js
{
  "code": 200,
  "data": {
    "succcess": 1,     // 删除商品可能由于有订单而失败
    "message": "",   
  }
}
```

##### 13. 后台商户发货

- URL：`/api/vendors/orders/express`
- 方法：POST
- 请求参数：
```js
{
  "vendor_id": 10,
  "order_id": 13,
  "express_number": 0123456789,
}
```
- 响应：
```js
{
  "code": 200,
  "data": {
    "succcess": 1,     // 删除商品可能由于有订单而失败
    "message": "",   
  }
}
```

##### 15. 后台商户请求订单列表  // 与用户请求订单列表略有不同，查询方向是物到人和人到物的区别
- URL：`/api/vendors/orders`
- 方法：POST
- 请求参数：
```js
{
  "vendor_id": 12
}
```
- 响应：
```js
{
  "code": 200,
  "data": {
    "success": 1,
    "message": "",  
    "orders": [
      {
        "user_id": 1,
        "order_id": 10,
        "product_id": 13,
        "order_status": "shipping",
        "place_time": '2024-02-29 00:00:00',
        "quantity": 6,
        "total_price": 10.22,
        "parent_order_id": 9
      },
      {...}  
    ]
  }
}
```

##### 16. 后台商户删除订单 -> 共用前台API
- URL：`/api/vendors/orders/delete`
- 方法：POST
- 请求参数：
```js
{
  "vendor_id": 12,
  "order_id": 3
}
```
- 响应：
```js
{
  "code": 200,
  "data": {
    "success": 1,                       // 后端有成功失败检查
    "message": "",   
  }
}
```

##### 17. 后台管理员获取用户列表

- URL：`/api/admin/users`
- 方法：POST
- 请求参数：
```js
{
}
```
- 响应：
```js
{
  "code": 200,
  "data": {
    "success": 1,
    "message": "", 
    "users": [
      {  
        "user_id": 10,
        "user_display_name: "Steven",
        "balance": 1
      },
      {...},
      {...}
    ]
  }
}
```


##### 18. 后台管理员获取用户列表

- URL：`/api/admin/vendors`
- 方法：POST
- 请求参数：
```js
{
}
```
- 响应：
```js
{
  "code": 200,
  "data": {
    "success": 1,
    "message": "",  
    "vendors": [
      {  
        "vendor_id": 10,
        "vendor_display_name: "Steven",
        "product_count": 10                         // 发布了多少种商品
      },
      {...},
      {...}
    ]
  }
}
```

##### 19. 后台管理员删除用户

- URL：`/api/admin/users/delete`
- 方法：POST
- 请求参数：
```js
{
  "user_id": 1,
  "vendor_id": 1,
  "role": Literal["users", "vendors"]
}
```
- 响应：
```js
{
  "code": 200,
  "data": {
    "success": 1,
    "message": "",   
  }
}
```
