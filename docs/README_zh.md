# GROUP25-7640

## 组员
- 23462426 F.Q Wen (Report & Documentation & Developer)
- 23455543 Cheung Chun Shing (Backend Developer)
- 23450274 Liu Bo (Backend Developer)
- 23418990 ZHOU Guangyu (Frontend User Mall Developer)
- 23430389 CHEN Dexi (Frontend Admin Panel Developer)

## 在线演示
[https://comp7640.wendemoapi.site](https://comp7640.wendemoapi.site)
- 商城: `/`
- 管理面板: `/panel/`
- 默认用户/密码: `alice`/`alice123`
- 默认商户/密码: `xiaomi`/`xiaomi123`
- 默认管理员: `admin`/`admin`



## ER图
![](https://github.com/GoodManWEN/GOUP25-7640/blob/main/misc/ERD-v2.png?raw=true)

#### ER图描述
- Each **user** may have 0 or many **orders**
- Eash **order** must belonged to a **user**

- Each **order** can have many **products** 
- Each **product** can be included in many **orders**

- Each **product** can be labelled with 0 or up to 3 tags
- Each **tag** can be label to many **products**

- Each **vendor** can provide 0 or many **products**
- Each **product** must be provided by at least 1 vendor

- Not captured in this ER diagram: 3 tables for permission control

## 主要实现功能
- 前台可以注册用户
- 后台可以由管理员添加商户
- 商户可以添加商品
- 用户可以浏览商品
- 用户可以按标签搜索商品，支持搜索多标签取交集
- 用户可以按商户搜索商品，只看对应商户的商品
- 用户可以购买商品
- 用户可以将商品添加至购物车，每一个订单可以包含来自不同商家的产品
- 用户可以在未发货前取消订单
- 用户可以取消订单中的一部分或取消整个订单
- 商户可以在未发货前取消订单
- 商户可以取消订单中的一部分或取消整个订单
- 商户可以对指定订单进行发货，并输入快递号
- 商户可以管理（新增/查看/删除）自己所有的商品
- 用户可以在前台查看自己的个人信息
- 用户可以在充值渠道充值
- 超级管理员可以新增用户
- 超级管理员可以管理（查看/删除）用户
- 超级管理员可以新增商户
- 超级管理员可以管理（查看/删除）商户
- 用户可以给购买过的商品打分

## 建表SQL
See [CREATE_DB_TABLES.txt](https://github.com/GoodManWEN/GOUP25-7640/blob/main/misc/CREATE_DB_TABLES.txt) for further reference


## 项目设计

- 使用前后端分离的MVVM模型构建应用, 包含一个用户商城前端，一个管理页面前端, 和一个后端.
- 后端技术栈: **Python + FastAPI**
- 前端技术栈: **Vue3 + Vite + Pinia**, etc.

#### Data Folder structure
```
├─backend              # 后端工程目录
│  ├─assets
│  |   ├─css
│  |   ├─imgs
│  |   ├─js
│  |   └─png
|  └─main.py
├─frontend_admin       # 前端工程目录 1
│  └─src
│      └─...
├─frontend_mall        # 前端工程目录 2
│  └─src
│      └─...
├─docs
├─misc
├─Dockerfile
└─docker-compose.yml
```


#### Workflow Structure Schema
```
+----------------+     +----------------+
|                |     |                |
|  Frontend      |     |  Frontend      |
|  Admin         |     |  Mall          |
|                |     |                |
+-------+--------+     +-------+--------+
        |                      |
        |                      |
        +----------+-----------+
                   |
                   v
             +-----+-----+
             |           |
             |  Backend  |
             |           |
             +-----+-----+
                   |
                   |
                   v
             +-----+-----+
             |           |
             | Database  |
             |           |
             +-----------+
```

## 完整设计文档

请参考 [Design_zh.md](https://github.com/GoodManWEN/GOUP25-7640/blob/main/docs/design_zh.md) 


## 部署指南

1. 首先，选择合适的操作系统来部署本服务。由于本服务部署依托于docker，建议您使用Linux操作系统。以下演示基于Ubuntu22.04。
2. 安装 `Docker` 和 `Docker compose`. 由于此部分内容不是本章重点，请参考 [Install Docker Engine on Ubuntu](https://docs.docker.com/engine/install/ubuntu/) 
```shell
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done

# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```
3. 检查是否安装成功.
```shell
docker -v
```
4. 克隆本仓库
```shell
git clone https://github.com/GoodManWEN/GOUP25-7640.git
cd GOUP25-7640
```
5. 构建镜像
```shell
docker build -t app .
```
6. 开启（Database等）完整服务
```shell
docker compose up
```
7. 如果一切顺利，您将可以在 `http://127.0.0.1:8080`访问服务

## API 接口文档

[API Documentation](https://github.com/GoodManWEN/GOUP25-7640/blob/main/docs/api_design.md)
