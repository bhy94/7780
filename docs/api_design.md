## API Design

##### 1. User Login

- URL：`/api/login`
- Method：POST
- Request Parameters：
```js
{
  "username": "string",
  "password": "string",
  "destination": Literal["back_end", "front_end"] 
}
```
- response：
```js
{
  "code": 200,               // 一般只返回200/304/403/404/503
  "data": {
    "success": 1,  
    "message": "success",    // 大多数情况下留空
    "user_id": 1,
    "vendor_id": 1,          // user_id和vendor_id can not have both
    "token": "md5string",    // server create_token
    "role": "vendor",        // Literal["customer", "vendor", "admin"]
  }
}
```

##### 2. User Logout

- URL：`/api/logout`
- Method：POST
- Request Parameters：
```js
{
  "user_id": 1,              // token in cookie
}
```
- response：
```js
{
  "code": 200,
  "data": {
    "sucecss": 1,
    "message": "logout success",    // 
  }
}
```

##### 3. Request Product List

- URL：`/api/products`
- Method：POST
- Request Parameters：`tags: string`
```js
{
  "tags": "自行车, 洗衣机, 冰箱, 彩电, 红的"     // Split logic back-end processing, leave 
                                              //empty to return all the goods, the front-end can be done to turn the page.
  "vendor_id": 10,                            // Second Dimension Screening Scope

}
```
- response：
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

##### 4. Request Product Info
- URL：`/api/products/info`
- Method：GET
- Request Parameters：
```js
{
  product_id: 10        // Full URL is /api/products/info?product_id=10
}
```
- response：
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


##### 5. UsersPlace Orders
- URL：`/api/users/orders/create`
- Method：POST
- Request Parameters：
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
      "quantity": 1              // The interface follows this specification. Since the front-end has 
                                //been designed for shopping carts, the back-end actually needs to perform 1-n order creation operations
    },
  ]
}
```
- response：
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
- Method：POST
- Request Parameters：
```js
{
  "user_id": 12,
  "order_id": 66
}
```
- response：
```js
{
  "code": 200,
  "data": {
    "success": 1,                       // check if deposit success
    "message": ""
  }
}
```

##### 7. User Request Personal Info
- URL：`/api/users/info`
- Method：GET
- Request Parameters：
  ```js
{
  user_id: 10        // Full src /api/users/info?user_id=10
}
```
- response：
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

##### 8. User Request Orders
- URL：`/api/users/orders`
- Method：POST
- Request Parameters：
```js
{
  "user_id": 12
}
```
- response：`code: int`, `message: string`, `data: {}`
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

##### 9.  User Cancel Order
- URL：`/api/users/orders/delete`
- Method：POST
- Request Parameters：
```js
{
  "user_id": 12,
  "order_id": 3
}
```
- response：
```js
{
  "code": 200,
  "data": {
    "success": 1,                       // checked at backend
    "message": "",   
  }
}
```

##### 10. frentend deposit money
- URL：`/api/users/deposit`
- Method：POST
- Request Parameters：
```js
{
  "user_id": 12,
  "balance_add": 100,                  // >=0
}
```
- response：
```js
{
  "code": 200,
  "data": {
    "success": 1,                       
    "message": "",   
  }
}
```


##### 11. Backend request vendor's products

- URL：`/api/vendors/products`
- Method：POST
- Request Parameters：
```js
{
  "vendor_id": 10
}
```
- response：
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
        "product_name": "Xiaomi Phone",
        "product_cover": "https://1.jpg",
        "product_info",
        "tags": ["xiaomi", "phone", "red"],
        "price": 60,
        "score": 4.5
      },
      {...},
      {...}
    ]
  }
}
```


##### 12. Vendors Add Products

- URL：`/api/vendors/products/create`
- Method：POST
- Request Parameters：
```js
{
  "vendor_id": 10,
  "product_name": "Xiaomi2",
  "product_cover": "https://1.jpg",
  "product_info": "**雷军**\n金凡",
  "tags": ["xiaomi", "phone", "red"],
  "price": 62
}
```
- response：
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

##### 13. Vendors Delete Products

- URL：`/api/vendors/products/delete`
- Method：POST
- Request Parameters：
```js
{
  "vendor_id": 10,
  "product_id": 13
}
```
- response：
```js
{
  "code": 200,
  "data": {
    "succcess": 1,     // Delete shops may fail
    "message": "",   
  }
}
```

##### 13. Vendor express

- URL：`/api/vendors/orders/express`
- Method：POST
- Request Parameters：
```js
{
  "vendor_id": 10,
  "order_id": 13,
  "express_number": 0123456789,
}
```
- response：
```js
{
  "code": 200,
  "data": {
    "succcess": 1,     // deletion may file because there's still orders remained
    "message": "",   
  }
}
```

##### 15. vendor request orders
- URL：`/api/vendors/orders`
- Method：POST
- Request Parameters：
```js
{
  "vendor_id": 12
}
```
- response：
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

##### 16. vendor cancel order
- URL：`/api/vendors/orders/delete`
- Method：POST
- Request Parameters：
```js
{
  "vendor_id": 12,
  "order_id": 3
}
```
- response：
```js
{
  "code": 200,
  "data": {
    "success": 1,                       // 后端有成功失败检查
    "message": "",   
  }
}
```

