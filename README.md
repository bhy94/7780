# GROUP29-7780-Group-Assignment-2

An implementation of a basic E-shop with its management panel, where you can explore products and pay for them with paypal(sandbox) if you like.

#### Github Source:
[https://github.com/GoodManWEN/GOUP25-7640](https://github.com/bhy94/7780)

## Group Member
- 23462264 Yiming Hong (Scrum Master)
- 23439327 Haolin Liu (Vise Scrum Master)
- 23462426 Fuquan Wen (Developer & Tester)
- 23458836 Hongyi Bian (Developer)


## Online DEMO
[https://7780.wendemoapi.site/](https://7780.wendemoapi.site/)
- **E-shop**: `7780.wendemoapi.site/`
- **Admin Panel**: `7780.wendemoapi.site/panel/login/`
- Default User/pass: `alice`/`alice123`
- Default Vendor/pass: `test`/`test123`

## Main Functional Implemented

- User Registration
- User Login and Logout
- Landing Page & Team Information (About Us)
- Product Display Page
- Add products to cart
- Placing Orders
- Paying for orders (notification of payment failure if balance is insufficient)
- Adding funds via PayPal
- Add products through the admin panel
- View all PayPal recharge records in the admin panel

## ER-Diagram
![](https://github.com/bhy94/7780/blob/main/misc/ERD-v2.png?raw=true)

## Project Design

- Designed with the front-end and back-end separation application model using MVVM, including two independent projects, namely the e-shop application and its associated management panel.
- The technology stack used for the online store includes **Vue3 + Vite + Pinia** + **node + Express.js**.
- The administration panel is built by python.


#### Data Folder structure
```
├─backend_node            # E-shop Folder
│  ├─assets
│  |   └─...
│  ├─router.js
│  ├─views.js
│  ├─database.js
│  └─app.js
├─backend_py              # Admin Panel Folder
│  ├─assets
│  |   └─...
|  └─main.py
├─frontend_admin          # Frontend Project Folder 1
│  └─src
│      └─...
├─frontend_mall           # Frontend Project Folder 2
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
|  Mall          |     |  Admin         |
|                |     |                |
+-------+--------+     +-------+--------+
        |                      |
        |                      |
+----------------+     +----------------+
|                |     |                |
|  Node+Express  |     |  Admin         |
|  Backend       |     |  Backend       |
|                |     |                |
+-------+--------+     +-------+--------+
        |                      |
        |                      |
        +----------+-----------+
                   |
                   v
             +-----+-----+
             |           |
             | Database  |
             |           |
             +-----------+
```

## Full Design Documentation

See [Design.md](https://github.com/bhy94/7780/blob/main/docs/design.md) for further reference


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
git clone https://github.com/bhy94/7780.git
cd 7780
```
5. Build Docker Image 1:
```shell
docker build -t mapp .
```
6. Build Docker Image 2:
```shell
cd backend_node
docker build -t tapp .
cd ..
```
7. Start servce with docker compose
```shell
docker compose up -d
```
8. Combining e-shop and admin panel with nginx reverse proxy. An example config file is as follow:
```conf
# /etc/nginx/sites-available/example.com
server {
    listen 443 ssl;
    server_name example.com;

    # SSL configuration
    ssl_certificate /path/to/your/certificate.crt;    # 
    ssl_certificate_key /path/to/your/private.key;    # 
    ssl_protocols TLSv1.2 TLSv1.3;                    # use TLS protocal
    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';
    ssl_prefer_server_ciphers on;

    # Static files
    root /var/www/html;
    index index.html index.htm;

    # Log file position
    access_log /var/log/nginx/example.com.access.log;
    error_log /var/log/nginx/example.com.error.log;

    # Handel Admin_panel stream
    location /api/ {
        proxy_pass http://127.0.0.1:8083;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Handel E-shop stream
    location / {
        proxy_pass http://127.0.0.1:8085;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name example.com;
    return 301 https://$server_name$request_uri;
}
```
9. If everything goes well, you will be able to access the service at `example.com` or localhost.

## API Documentation

[API Documentation](https://github.com/bhy94/7780/blob/main/docs/api_design.md)
