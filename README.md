# GROUP25-7640

An implementation of a basic multi-user mall and its management panel, both front-end and back-end, along with the description of its database rational design. Uses `Python` & `Typescript` technology.

#### Github Source:
[https://github.com/GoodManWEN/GOUP25-7640](https://github.com/GoodManWEN/GOUP25-7640)

#### Documentation in Chinese:

[中文文档](https://github.com/GoodManWEN/GOUP25-7640/blob/main/docs/README_zh.md)

## Group Member
- 23462426 F.Q Wen (Report & Documentation & Developer)
- 23455543 Cheung Chun Shing (Backend Developer)
- 23450274 Liu Bo (Backend Developer)
- 23418990 ZHOU Guangyu (Frontend User Mall Developer)
- 23430389 CHEN Dexi (Frontend Admin Panel Developer)


## Online DEMO
[https://comp7640.wendemoapi.site](https://comp7640.wendemoapi.site)
- **Mall**: `comp7640.wendemoapi.site/`
- **Admin Panel**: `comp7640.wendemoapi.site/panel/login/`
- Default User/pass: `alice`/`alice123`
- Default Vendor/pass: `xiaomi`/`xiaomi123`
- Default Supervisor: `admin`/`admin`


## ER-Diagram
![](https://github.com/GoodManWEN/GOUP25-7640/blob/main/misc/ERD-v2.png?raw=true)

#### Description of ER-Diagram
- Each **user** may have 0 or many **orders**
- Each **order** must belonged to a **user**

- Each **order** can have many **products** 
- Each **product** can be included in many **orders**

- Each **product** can be labelled with 0 or up to 3 tags
- Each **tag** can be label to many **products**

- Each **vendor** can provide 0 or many **products**
- Each **product** must be provided by at least 1 vendor

- Not captured in this ER diagram: 3 tables for permission control

## Main Functional Achievement

- Front end allows user registration
- The back end allows administrators to add merchants
- Merchants can add products
- Users can browse products.
- Users can search for products by tags, supporting the intersection of multiple tags.
- Users can search for products by merchant and only view products from the corresponding merchant.
- Users can purchase products
- Users can add products to the shopping cart, each order can contain products from different merchants
- Users can cancel orders before they are shipped
- Users can cancel part of an order or the entire order
- Merchants can cancel orders before they are shipped
- Merchants can cancel part of an order or the entire order
- Merchants can ship specified orders and enter a tracking number
- Merchants can manage (add/view/delete) all their products
- Users can view their personal information on the front end
- Users can recharge through recharge channels
- Super administrators can add users
- Super administrators can manage (view/delete) users
- Super administrators can add merchants
- Super administrators can manage (view/delete) merchants
- Users can rate products they have purchased

## Create Table SQL
See [CREATE_DB_TABLES.txt](https://github.com/GoodManWEN/GOUP25-7640/blob/main/misc/CREATE_DB_TABLES.txt) for further reference


## Project Design

- Designed with the front-end and back-end separation application model using MVVM, it includes a user-end for user use, a vendor-end for merchants (and administrators), and a server backend.
- Backend technology stack: **Python + FastAPI**
- Frontend technology stack: **Vue3 + Vite + Pinia**, etc.

#### Data Folder structure
```
├─backend              # Backend Project Folder
│  ├─assets
│  |   ├─css
│  |   ├─imgs
│  |   ├─js
│  |   └─png
|  └─main.py
├─frontend_admin       # Frontend Project Folder 1
│  └─src
│      └─...
├─frontend_mall        # Frontend Project Folder 2
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

## Full Design Documentation

See [Design.md](https://github.com/GoodManWEN/GOUP25-7640/blob/main/docs/design.md) for further reference


## Deployment Guidelines

1. First, select the correct operating system. Since this application relies on Docker deployment, we recommend that you deploy the service on a Linux system, the following is an example of how to deploy the service on `Ubuntu 22.04`.
2. Install `Docker` and its plugin `Docker compose`. Since this section is not the focus of this chapter, please visit [Install Docker Engine on Ubuntu](https://docs.docker.com/engine/install/ubuntu/) for more details.
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
3. Check if install successed.
```shell
docker -v
```
4. Clone this repo to local:
```shell
git clone https://github.com/GoodManWEN/GOUP25-7640.git
cd GOUP25-7640
```
5. Build Docker Image:
```shell
docker build -t app .
```
6. Start servce with docker compose
```shell
docker compose up
```
7. If everything goes well, you will be able to access the service at `http://127.0.0.1:8080`

## API Documentation

[API Documentation](https://github.com/GoodManWEN/GOUP25-7640/blob/main/docs/api_design.md)

.

.

.


