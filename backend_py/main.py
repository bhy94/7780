from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.staticfiles import StaticFiles
from loguru import logger

import asyncio 
import aiomysql 
from permissions import aes_decryption #
from utils import load_config # 
import base64
from routing import Router #
import os
from views import routing_single_file, router_catch_all # 
from functools import partial
from utils import init_database_process #

config = load_config()
app = FastAPI(
    docs_url='/docs' if config["app"]["DEBUG"] else None, 
    redoc_url='/redoc' if config["app"]["DEBUG"] else None
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config["app"]["ORIGINS"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
if not config["app"]["DEBUG"]:
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=config["app"]["TRUST_HOSTS"])

@app.on_event("startup") 
async def startup():
    loop = asyncio.get_event_loop()
    config = load_config()
    app.state.config = config
    sensitive = base64.b64decode(config["mysql"]["MYSQL_PASSWORD"])
    sensitive = aes_decryption(sensitive, b"nobody knows").decode("utf-8")
    while True:
        logger.info("new connection to mysql")
        try:
            pool = await aiomysql.create_pool(
                host=config["mysql"]["MYSQL_HOST"], 
                port=config["mysql"]["MYSQL_PORT"], 
                user=config["mysql"]["MYSQL_USER"], 
                password=sensitive, 
                db="mysql", 
                autocommit=True,
                loop=loop
            )
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute("SELECT 42;")
                    r = await cur.fetchone()
            break
        except Exception as e:
            await asyncio.sleep(3)
    try:
        app.state.pool = await aiomysql.create_pool(
            host=config["mysql"]["MYSQL_HOST"], 
            port=config["mysql"]["MYSQL_PORT"], 
            user=config["mysql"]["MYSQL_USER"], 
            password=sensitive, 
            db=config["mysql"]["MYSQL_DB"], 
            autocommit=True,
            loop=loop
        )
    except Exception as e:
        pool = await aiomysql.create_pool(
            host=config["mysql"]["MYSQL_HOST"], 
            port=config["mysql"]["MYSQL_PORT"], 
            user=config["mysql"]["MYSQL_USER"], 
            password=sensitive, 
            db="mysql", 
            autocommit=True,
            loop=loop
        )
        await init_database_process(pool)
    finally:
        ...
    app.state.pool = await aiomysql.create_pool(
        host=config["mysql"]["MYSQL_HOST"], 
        port=config["mysql"]["MYSQL_PORT"], 
        user=config["mysql"]["MYSQL_USER"], 
        password=sensitive, 
        db=config["mysql"]["MYSQL_DB"], 
        autocommit=True,
        loop=loop
    )

@app.on_event("shutdown")
async def shutdown():
    app.state.pool.close()
    await app.state.pool.wait_closed()

Router(app).install()
run_dir = os.path.dirname(__file__)
# app.mount("/", StaticFiles(directory=os.path.join(run_dir, 'assets')), name="static")

# 递归绑定静态文件夹
def bind_statics(app, path_):
    base_dir = os.path.abspath(os.path.dirname(__file__))
    for root, dirs, files in os.walk(path_):
        for file in files:
            fp = os.path.abspath(os.path.join(root, file))
            fp = fp.replace(base_dir, '').replace('\\', '/').replace(f'/assets', '')
            app.get(fp)(partial(routing_single_file, file_name=fp))

bind_statics(app, os.path.join(run_dir, 'assets'))
app.get("/panel/{full_path:path}")(partial(router_catch_all, destination="2"))
app.get("/{full_path:path}")(partial(router_catch_all, destination="1"))

# Run app
# uvicorn main:app --port 8080 --reload