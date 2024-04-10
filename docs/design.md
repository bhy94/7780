# GROUP25-7640

#### [中文文档](https://github.com/GoodManWEN/GOUP25-7640/blob/main/docs/design_zh.md)

#### Table of Contents
- Grouping
- Brief Description of Functions
- Frontend Design Reference
- Backend Design Reference
- Object Design Reference
- [API Design](https://github.com/GoodManWEN/GOUP25-7640/blob/main/docs/api_design.md)
- [Design Reference](https://github.com/GoodManWEN/GOUP25-7640/blob/main/docs/previews.md)

## Grouping
Requirement for creating a web application using MySQL (multi-merchant/multi-user mall), front-end and back-end separation.

1. Documentation, documents, ER diagrams, etc.: Wen
2. Frontend: Chen, Zhou
3. Backend: RICK, Liu

## Function Overview

1. User registration, user login
2. Merchant registration, merchant login
3. Super administrator hardcoded (provided in backend configuration file)
5. Users can view products
6. Users can add items to the shopping cart
7. Users can purchase products
8. Users can recharge their accounts
9. Users can cancel certain items in certain order statuses
10. Users can cancel orders in certain order statuses
11. Backend merchants can add products
12. Backend merchants can delete products
13. Backend merchants can cancel orders
14. Super administrators can add or delete users
15. Super administrators can add or delete merchants

##### General Principles
1. Assume the code runs under legal conditions
2. Robustness should meet legal scenarios
3. Database maintains relationships, no strong synchronization considered
4. Ensure code quality is reviewable
5. For all image-related operations, store image URLs instead of binary data
6. Currency system: Design users to recharge virtual currency via specific APIs, and then manage currency, refunds, and other operations internally; super administrators can override buying and selling currency balance rules.

## Frontend Design Reference

- Overall design: Use H5 technology, ensure responsiveness, and utilize Vue/React for engineering. Choose the right component library to save development time.
- Compiled files are packaged into a single html+css+js file, placed in the backend assets.
- Users can browse products, and merchants have a management backend to add products.
- Example technology stack: Vite + Vue3 + Pinia + ElementPlus

### Views

##### Frontend Project

1. Home view: Navigation bar, directly display product list, search box.
2. Login page: Allows user registration/login.
3. Product page: Display product details (rich text), add to shopping cart.
4. Shopping cart (payment) page: View all added products (shopping cart status is entirely maintained by the frontend).
5. Recharge page: An input box and a button, entering 100 and clicking recharge will recharge the user's account with 100 yuan.
7. User profile view: Display user basic information.
8. User orders page: Display all personal orders, can cancel orders not yet shipped.

##### Backend Project

1. Merchant product management: Product list, can delete products.
2. Merchant add product view.
3. Merchant order tracking: Order list, add orders, delete orders.
4. Super administrator: User list, delete users.
5. Super administrator add user.

### Main Component

Frontend Self-Maintenance

### Additional Information

- Route guards, frontend permission interception for different user levels.
- May need to build a custom development server.
- User tokens stored in cookies.
- All requests after login must include a token.

## Backend Design Reference

- Overall design: Short-cycle backend, reducing project engineering complexity.
- Due to not needing complex authentication and state maintenance middleware, it is recommended to use a bare-bones framework (directly write certain logic for a specific route), not using SpringBoot/Django.
- Example technology stack: Python + FastAPI/Flask + aiomysql/pymysql:

### Main Tables
Users
```
users(
  user_id,                         // Auto increment
  user_username, 
  user_password,                   // hash+salt simple hmac mode
  user_display_name,
  telephone_number,
  address,
  avatar,
  balance                          // virtual balance
)
```

Vendors
```
vendors(
  vendor_id,               
  vendor_username,
  vendor_password,                
  vendor_display_name,
  origin_address,
  vendor_score,                   // scores are maintained by app node。
  avatar,
  balance                         
)
```

Products
``` 
products(
  product_id,
  product_name,
  product_cover,
  product_info,
  product_score,                  
  price
)
```

Orders
```
orders(
  order_id,
  user_id,
  parent_order_id,               // Since one order can contain multiple items, it is actually implemented as multiple sub-orders
                                 // Orders have a parent-child relationship with a depth of 1.
                                 // Business-wise, it is necessary to maintain consistency in the status of parent and child orders.
  product_id,
  quantity,
  total_price,
  place_time,
  status                         // CHAR(10)
  express_number                 // express company number
)
```

tags
```
tags(
  tag_id,
  tag_name
)
```

Many-to-many & Many-to-one relationship maintenance
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

Login status
```
login_status_user(
  lsu_id,
  user_id,
  token,
  expire_time            // Considering the business simplicity of the test server,
                         // only the expiration time is set and the expiration behavior is not maintained.
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

### Additional Information
Route Authentication

## Object Design Reference

#### Main Product Attributes

- Title
- Image (Binary storage systems are not maintained, all images must be in internet URL format)
- Description
- Tags
- Selling Price
- Rating

#### Main User Attributes

- Username
- Password
- Display Name
- Avatar (Binary storage systems are not maintained, all avatars must be in internet URL format, open-source avatar APIs are available)
- Related Orders
- Shipping Address
- Phone Number

#### Main Merchant Attributes

- Username
- Password
- Display Name
- Avatar
- Shipping Origin
- Rating

#### Order Status
Divided into:
- Placed
- Paid
- Shipping
- Finished

Both merchants and users can cancel orders in the Placed and Paid status.

#### Permission Levels

- The frontend is divided into public and admin sections, each maintaining two projects with non-interchangeable permissions.
- The backend has administrator-level and regular merchants
- Administrators can delete any merchant and user (and delete all related orders or product records)
- Merchants cannot delete products that still have unfinished orders.
- According to the above rules, there should be orders that cannot link to any product (can uniformly point to a deleted product), no other broken links exist.

## Relational/Database Creation Commands
Omitted, backend provided.
