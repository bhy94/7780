from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from permissions import authentication

from models import * #
from models import RESPONSE #
from permissions import authentication #
from utils import parse_tag_names # 
from copy import deepcopy
from typing import Annotated, Literal
import datetime
import uuid 
import os

async def read_root(request: Request):
    pool = request.app.state.pool
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT 42;")
            value = await cur.fetchone()
            return {"Hello": value}
        

async def router_catch_all(request: Request, full_path: str, destination: Literal["1", "2"]):
    file_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "assets"))
    if destination == "1":
        return FileResponse(os.path.join(file_dir, "index1.html"))
    else:
        return FileResponse(os.path.join(file_dir, "index2.html"))

async def routing_single_file(request: Request, file_name: str):
    file_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "assets/"))
    # file_path_ = os.path.join(file_dir, file_name)
    file_path_ = file_dir + file_name
    # print(file_dir, file_path_, file_name)


    # 检查文件扩展名，以确定是否是JavaScript文件
    if file_name.endswith(".js"):
        return FileResponse(file_path_, media_type="application/javascript")
    elif file_name.endswith(".css"):
        return FileResponse(file_path_, media_type="text/css")
    elif file_name.endswith(".png"):
        return FileResponse(file_path_, media_type="image/png")
    elif file_name.endswith(".jpg"):
        return FileResponse(file_path_, media_type="image/jpeg")
    else:
        # 对于其他类型的文件，FileResponse会尝试自动确定正确的media_type
        return FileResponse(file_path_)

async def login_handler(request: Request, item: LoginItem):
    pool = request.app.state.pool
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            res = deepcopy(RESPONSE)
            if item.destination == "front_end":
                await cur.execute(
                    "SELECT user_id FROM users WHERE user_username = %s AND user_password = %s;", 
                    (item.username, item.password)
                )
                uid = await cur.fetchone()
                print(uid, 'zz', item)
                if uid:
                    uuid_ = str(uuid.uuid4())
                    expire_time = (datetime.datetime.now()+datetime.timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")
                    await cur.execute("INSERT INTO login_status_user (user_id, token, expire_time) VALUES (%s, %s, %s);", (uid[0], uuid_, expire_time))
                    await conn.commit()
                    res["data"]["user_id"] = uid[0]
                    res["data"]["token"] = uuid_
                    res["data"]["role"] = "user"
                    return res
            elif item.destination == "back_end":
                config = request.app.state.config
                if item.username == config["app"]["ADMIN_USERNAME"] and item.password == config["app"]["ADMIN_USERNAME"]:
                    uuid_ = str(uuid.uuid4())
                    expire_time = (datetime.datetime.now()+datetime.timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")
                    await cur.execute("INSERT INTO login_status_admin (admin_id, token, expire_time) VALUES (%s, %s, %s);", (1, uuid_, expire_time))
                    await conn.commit()
                    res["data"]["vendor_id"] = 1
                    res["data"]["token"] = uuid_
                    res["data"]["role"] = "admin"
                    return res
                # else normal vendor
                await cur.execute(
                    "SELECT vendor_id FROM vendors WHERE vendor_username = %s AND vendor_password = %s;", 
                    (item.username, item.password)
                )
                vid = await cur.fetchone()
                if vid:
                    res["data"]["vendor_id"] = vid[0]
                    uuid_ = str(uuid.uuid4())
                    expire_time = (datetime.datetime.now()+datetime.timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")
                    await cur.execute("INSERT INTO login_status_vendor (vendor_id, token, expire_time) VALUES (%s, %s, %s);", (vid[0], uuid_, expire_time))
                    await conn.commit()
                    res["data"]["token"] = uuid_
                    res["data"]["role"] = "vendor"
                    return res
                # else
                res["code"] = 403
                res["data"]["success"] = 0
                return res
            else:
                res["code"] = 503
                res["data"]["success"] = 0
                return res


async def logout_handler(request: Request, auth: Annotated[dict, Depends(authentication)]):
    role = auth["role"]
    rid = auth["rid"]
    sid = auth["sid"]

    if role == "admin":
        table = "login_status_admin"
        col = "admin_id"
    elif role == "vendor":
        table = "login_status_vendor"
        col = "vendor_id"
    elif role == "user":
        table = "login_status_user"
        col = "user_id"
    else:
        raise HTTPException(status_code=503, detail="Invalid role")
    
    pool = request.app.state.pool
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(f"DELETE FROM {table} WHERE {col}=%s AND token=%s", (rid, sid))
            delete_success = False
            if cur.rowcount > 0:
                delete_success = True
            await conn.commit()

    res = deepcopy(RESPONSE)
    if delete_success:
        res["data"]["success"] = 1
    else:
        res["data"]["success"] = 0
    return res


async def user_register(request: Request, item: CreateUserItem):

    res = deepcopy(RESPONSE)
    pool = request.app.state.pool
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            try:
                await cur.execute("SELECT user_id FROM users WHERE user_username = %s;", (item.user_username,))
                if (await cur.fetchone()) is not None:
                    res["code"] = 400
                    res["data"]["success"] = 0
                    res["data"]["message"] = "Username already exists"
                    return res
                await cur.execute("INSERT INTO users (user_username, user_password, user_display_name, avatar, address, telephone_number, balance) VALUES (%s, %s, %s, %s, %s, %s, 0);", (item.user_username, item.user_password, item.user_display_name, item.avatar, item.address, item.telephone_number))
                await conn.commit()
                return res
            except Exception as e:
                res["data"]["success"] = 0
                res["data"]["message"] = "Display username already exists"
                return res


async def request_products_handler(request: Request, item: RequestProductsItem, auth: Annotated[dict, Depends(authentication)]):
    tags = parse_tag_names(item.tags)
    if len(tags) > 10:
        raise HTTPException(status_code=400, detail="Too many tags")
    vendor_id = item.vendor_id

    if vendor_id is not None:
        bias_sql = """
        product_id IN (
            SELECT DISTINCT product_id FROM vendor_product_rel WHERE vendor_id = %s
        )
        """

    pool = request.app.state.pool
    products = []
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            print(len(tags))
            if len(tags) == 0:
                await cur.execute(f"""
                    SELECT product_id, product_name, product_cover, price FROM products 
                    {
                        "WHERE" + bias_sql if vendor_id is not None else ""
                    }
                    ORDER BY product_id DESC LIMIT 100;
                """, (vendor_id,) if vendor_id is not None else ())
                products = await cur.fetchall()
            else:
                await cur.execute(f"""
                    SELECT product_id, product_name, product_cover, price FROM products WHERE product_id IN (
                        SELECT tpr.product_id
                        FROM tag_product_rel AS tpr
                        JOIN tags AS t ON tpr.tag_id = t.tag_id
                        WHERE t.tag_name IN ({''.join(['%s, ']*len(tags))[:-2]})
                        GROUP BY tpr.product_id
                        HAVING COUNT(DISTINCT t.tag_name) = {len(tags)}
                    ) {
                        "AND" + bias_sql if vendor_id is not None else ""
                    }
                    ORDER BY product_id DESC LIMIT 100;
                """, tuple(tags) if vendor_id is None else tuple([*tags, vendor_id]))
                products = list(await cur.fetchall())
    res = deepcopy(RESPONSE)
    res["data"]["products"] = products
    return res

async def get_product_info_handler(request: Request, product_id: int):
    res = deepcopy(RESPONSE)

    pool = request.app.state.pool
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT product_id, product_name, product_cover, product_info, price, product_score FROM products WHERE product_id = %s", (product_id,))
            ret = await cur.fetchone()
            if ret is None or len(ret) <= 0:
                res["data"]["success"] = 0
                res["data"]["message"] = "no such product"
                return res
            # else
            # tags
            product_id = ret[0]
            await cur.execute("SELECT tag_name FROM tags WHERE tag_id IN (SELECT DISTINCT tag_id FROM tag_product_rel WHERE product_id = %s);", (product_id,))
            tags = await cur.fetchall()
            tags = list(map(lambda x: x[0], tags))
            # address
            await cur.execute("SELECT vendor_id, vendor_display_name, avatar, origin_address FROM vendors WHERE vendor_id IN (SELECT DISTINCT vendor_id FROM vendor_product_rel WHERE product_id = %s);", (product_id,))
            ress = await cur.fetchone()
            try:
                vendor_id = ress[0]
                vendor_display_name = ress[1]
                vendor_avatar = ress[2]
                address = ress[3]
            except:
                address = ''
            res["data"]["tags"] = tags
            res["data"]["vendor_id"] = vendor_id
            res["data"]["vendor_display_name"] = vendor_display_name
            res["data"]["vendor_avatar"] = vendor_avatar
            res["data"]["origin_address"] = address
            res["data"]["product_id"] = product_id
            res["data"]["product_name"] = ret[1]
            res["data"]["product_cover"] = [ret[2], ]
            res["data"]["product_info"] = ret[3]
            res["data"]["price"] = ret[4]
            res["data"]["product_score"] = ret[5]
            return res

async def create_order_handler(request: Request, order_details: OrdersCreateItem, auth: Annotated[dict, Depends(authentication)]):
    user_id = order_details.user_id
    user_id_real = auth["rid"]
    if not (user_id == user_id_real and auth['role'] =='user'):
        raise HTTPException(status_code=403, detail="Invalid user_id")

    if len(order_details.items) <= 0:
        raise HTTPException(status_code=400, detail="No items in order")

    order_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    items = list(map(dict, order_details.items))
    if len(items) <= 0:
        raise HTTPException(status_code=400, detail="No items in order")

    res = deepcopy(RESPONSE)
    pool = request.app.state.pool
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            for item in items:
                await cur.execute("SELECT price FROM products WHERE product_id = %s;", (item["product_id"],))
                price = await cur.fetchone()
                if price is None:
                    raise HTTPException(status_code=400, detail="No such product")
                price = price[0]
                item["price"] = price
                item["total_price"] = price * item["quantity"]
            
            all_total_price = sum(map(lambda x: x["total_price"], items))
            # await cur.execute("SELECT balance FROM users WHERE user_id = %s;", (user_id,))
            # balance = await cur.fetchone()
            # if balance is None:
            #     res['code'] = 400
            #     res["data"]["success"] = 0
            #     res["data"]["message"] = "No such user"
            # balance = balance[0]
            # if balance < all_total_price:
            #     res["data"]["success"] = 0
            #     res["data"]["message"] = "Insufficient balance"
            #     return res
            if len(items) == 1:
                await cur.execute("""
                    INSERT INTO orders (user_id, parent_order_id, product_id, quantity, total_price, place_time, status, express_number) VALUES (%s, 0, %s, %s, %s, %s, "placed", "");
                """, (order_details.user_id, items[0]["product_id"], items[0]["quantity"], items[0]["total_price"], order_time))
                await cur.execute("UPDATE orders SET  parent_order_id = %s WHERE order_id = %s", (cur.lastrowid, cur.lastrowid))
            else:
                await cur.execute("""
                    INSERT INTO orders (user_id, parent_order_id, product_id, quantity, total_price, place_time, status, express_number) VALUES (%s, 0, %s, 0, %s, %s, "placed", "");
                """, (order_details.user_id, items[0]["product_id"], all_total_price, order_time))
                order_id = cur.lastrowid
                await cur.execute("UPDATE orders SET parent_order_id = %s WHERE order_id = %s", (order_id, order_id))
                await cur.executemany("""
                    INSERT INTO orders (user_id, parent_order_id, product_id, quantity, total_price, place_time, status, express_number) VALUES (%s, %s, %s, %s, %s, %s, "placed", "");
                """, [(order_details.user_id, order_id, item["product_id"], item["quantity"], item["total_price"], order_time) for item in items])
            await conn.commit()

    
    return res

async def request_payment_handler(request: Request, payment: PaymentItem, auth: Annotated[dict, Depends(authentication)]):
    user_id = payment.user_id
    user_id_real = auth["rid"]
    if not (user_id == user_id_real and auth['role'] =='user'):
        raise HTTPException(status_code=403, detail="Invalid user_id")

    res = deepcopy(RESPONSE)
    order_id = payment.order_id
    pool = request.app.state.pool
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT parent_order_id, total_price FROM orders WHERE order_id = %s and status='placed';", (order_id,))
            total_price = await cur.fetchone()
            if total_price is None:
                raise HTTPException(status_code=400, detail="No such order")
            parent_order_id, total_price = total_price
            if parent_order_id != order_id:
                raise HTTPException(status_code=400, detail="Not a parent order")
            await cur.execute("SELECT balance FROM users WHERE user_id = %s;", (user_id,))
            balance = await cur.fetchone()
            if balance is None:
                raise HTTPException(status_code=400, detail="No such user")
            balance = balance[0]
            if balance < total_price:
                res["data"]["success"] = 0
                res["data"]["message"] = "Insufficient balance"
                return res
            try:
                await conn.begin()
                await cur.execute("UPDATE users SET balance = balance - %s WHERE user_id = %s;", (total_price, user_id))
                assert cur.rowcount > 0
                await cur.execute("UPDATE orders SET status = 'paid' WHERE order_id = %s and status='placed';", (order_id,))
                assert cur.rowcount > 0
                await cur.execute("UPDATE orders SET status = 'paid' WHERE parent_order_id = %s and status='placed';", (order_id,))
                # 商户收款未做
            except:
                await conn.rollback()
                res["data"]["success"] = 0
            else:
                await conn.commit()
                return res


async def user_recieve_order_handler(request: Request, item: PaymentItem, auth: Annotated[dict, Depends(authentication)]):
    user_id = item.user_id
    user_id_real = auth["rid"]
    if not (user_id == user_id_real and auth['role'] =='user'):
        raise HTTPException(status_code=403, detail="Invalid user_id")

    res = deepcopy(RESPONSE)
    pool = request.app.state.pool
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("UPDATE orders SET status = 'recieved' WHERE order_id = %s and status='shipping';", (item.order_id, ))
            a = cur.rowcount 
            await cur.execute("UPDATE orders SET status = 'recieved' WHERE parent_order_id = %s and status='shipping';", (item.order_id, ))
            b = cur.rowcount 
            
            if (a+b) > 0:
                await conn.commit()
                return res
            else:
                res["code"] = 400
                res["data"]["success"] = 0
                return res

async def get_user_info_handler(request: Request, user_id: int, auth: Annotated[dict, Depends(authentication)]):
    res = deepcopy(RESPONSE)
    user_id_real = auth["rid"]
    if not (user_id == user_id_real and auth['role'] =='user'):
        raise HTTPException(status_code=403, detail="Invalid user_id")

    pool = request.app.state.pool
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT user_id, user_username, user_display_name, avatar, address, telephone_number, balance FROM users WHERE user_id = %s;", (user_id,))
            ret = await cur.fetchone()
            if ret is None or len(ret) <= 0:
                res["data"]["success"] = 0
                res["data"]["message"] = "no such user"
                return res
            res["data"]["user_id"] = ret[0]
            res["data"]["user_username"] = ret[1]
            res["data"]["user_display_name"] = ret[2]
            res["data"]["avatar"] = ret[3]
            res["data"]["address"] = ret[4]
            res["data"]["telephone_number"] = ret[5]
            res["data"]["balance"] = ret[6]
            return res
        
async def get_vendor_info_handler(request: Request, vendor_id: int, auth: Annotated[dict, Depends(authentication)]):
    res = deepcopy(RESPONSE)
    vendor_id_real = auth["rid"]
    print(auth)
    if not (vendor_id == vendor_id_real and auth['role'] =='vendor'):
        raise HTTPException(status_code=403, detail="Invalid vendor_id")

    pool = request.app.state.pool
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT vendor_id, vendor_display_name FROM vendors WHERE vendor_id = %s;", (vendor_id,))
            ret = await cur.fetchone()
            if ret is None or len(ret) <= 0:
                res["data"]["success"] = 0
                res["data"]["message"] = "no such vendor"
                return res
            res["data"]["vendor_id"] = ret[0]
            res["data"]["vendor_display_name"] = ret[1]
            return res

async def request_user_orders_handler(request: Request, item: RequestUserOrdersItem, auth: Annotated[dict, Depends(authentication)]):
    print(auth, item)
    # 暂未完成树形结构划分，不确定前端还是后端做
    user_id = item.user_id
    user_id_real = auth["rid"]
    if not (user_id == user_id_real and auth['role'] =='user'):
        raise HTTPException(status_code=403, detail="Invalid user_id")

    pool = request.app.state.pool
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT a.order_id, a.parent_order_id, a.product_id, a.quantity, a.total_price, a.place_time, a.status , b.product_name, a.express_number FROM orders a LEFT JOIN products b ON a.product_id = b.product_id WHERE user_id = %s;", (user_id,))
            orders = await cur.fetchall()
            res = deepcopy(RESPONSE)
            # res["data"]["orders"] = list(orders)
            # 整理成树形结构
            result = {}
            for order in orders:
                target = result.setdefault(order[1], {
                    "order_id": None,
                    "total_price": None,
                    "place_time": None,
                    "status": None,
                    "items": []
                })
                if target["order_id"] == None:
                    express_number = order[8]
                target["order_id"] = order[1] if target["order_id"] == None else target["order_id"]
                target["total_price"] = order[4] if target["total_price"] == None else target["total_price"]
                target["place_time"] = order[5] if target["place_time"] == None else target["place_time"]
                target["status"] = order[6] if target["status"] == None else target["status"]
                target["items"].append({
                    "order_id": order[0],
                    "product_id": order[2],
                    "quantity": order[3],
                    "total_price": order[4],
                    "place_time": order[5],
                    "status": order[6],
                    "product_name": order[7],
                    "express_number": express_number if order[8] == '' else order[8]
                })
            for key in result.keys():
                if len(result[key]["items"]) > 1:
                    for idx in range(len(result[key]["items"])):
                        if result[key]["items"][idx]["quantity"] == 0:
                            result[key]["items"].pop(idx)
                            break

            res["data"]["orders"] = list(result.values())
            return res

async def user_cancel_order_handler(request: Request, item: CancelOrderItem, auth: Annotated[dict, Depends(authentication)]):
    user_id = item.user_id
    user_id_real = auth["rid"]
    if not (user_id == user_id_real and auth['role'] =='user'):
        raise HTTPException(status_code=403, detail="Invalid user_id")
    
    res = deepcopy(RESPONSE)
    pool = request.app.state.pool
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            try:
                await conn.begin()
                # 已付款余额退款
                await cur.execute("SELECT total_price FROM orders WHERE order_id = %s and user_id = %s and status = 'paid'", (item.order_id, item.user_id))
                total_price = await cur.fetchone()
                if total_price is not None:
                    # raise Exception()
                    total_price = total_price[0]
                    await cur.execute("UPDATE users SET balance = balance + %s WHERE user_id = %s;", (total_price, user_id))
                price_diff = 0
                recover_parent_order_id = 0
                await cur.execute("SELECT parent_order_id, sum(total_price) FROM orders WHERE order_id = %s and user_id = %s and status IN ('placed', 'paid');", (item.order_id, item.user_id))
                r = await cur.fetchone()
                if r is not None:
                    recover_parent_order_id, price_diff = r
                await cur.execute("DELETE FROM orders WHERE order_id = %s and user_id = %s and status IN ('placed', 'paid');", (item.order_id, item.user_id))
                ar1 = cur.rowcount
                await cur.execute("DELETE FROM orders WHERE parent_order_id = %s and user_id = %s and status IN ('placed', 'paid');", (item.order_id, item.user_id))
                ar2 = cur.rowcount
                assert (ar1 + ar2) > 0
                if recover_parent_order_id != 0:
                    await cur.execute("UPDATE orders SET total_price = total_price - %s WHERE order_id = %s AND quantity = 0;", (price_diff, recover_parent_order_id))
            except Exception as e:
                await conn.rollback()
                res["data"]["success"] = 0
                return res 
            else:
                await conn.commit()
                return res


async def user_deposit_handler(request: Request, item: RequestDepositItem, auth: Annotated[dict, Depends(authentication)]):
    user_id = item.user_id
    user_id_real = auth["rid"]
    if not (user_id == user_id_real and auth['role'] =='user'):
        raise HTTPException(status_code=403, detail="Invalid user_id")

    res = deepcopy(RESPONSE)
    if item.balance_add <= 0:
        res["data"]["success"] = 0
        return res
    pool = request.app.state.pool
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("UPDATE users SET balance = balance + %s WHERE user_id = %s;", (item.balance_add, user_id))
            if cur.rowcount > 0:
                await conn.commit()
                return res
            else:
                res["data"]["success"] = 0
                return res


async def request_vendor_products_handler(request: Request, item: RequestVendorProductsItem, auth: Annotated[dict, Depends(authentication)]):
    print(auth, item)
    vendor_id = item.vendor_id
    vendor_id_real = auth["rid"]
    if not (vendor_id == vendor_id_real and auth['role'] =='vendor'):
        raise HTTPException(status_code=403, detail="Invalid vendor_id")

    pool = request.app.state.pool
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT p.product_id, product_name, product_cover, product_info, price, product_score FROM products AS p JOIN vendor_product_rel AS vpr ON p.product_id = vpr.product_id JOIN vendors AS v ON vpr.vendor_id = v.vendor_id WHERE v.vendor_id = %s; ", (vendor_id,))
            products = await cur.fetchall()
            products2 = []
            for product in products:
                product2 = dict(zip(["product_id", "product_name", "product_cover", "product_info", "price", "product_score"], product ))
                await cur.execute("SELECT tag_name FROM tags WHERE tag_id IN (SELECT tag_id FROM tag_product_rel WHERE product_id = %s);", (product[0],))
                tags = await cur.fetchall()
                tags = list(map(lambda x: x[0], tags))
                product2["tags"] = tags
                products2.append(product2)
            res = deepcopy(RESPONSE)
            res["data"]["products"] = products2
            return res


async def create_product_handler(request: Request, item: CreateProductItem, auth: Annotated[dict, Depends(authentication)]):
    vendor_id = item.vendor_id
    vendor_id_real = auth["rid"]
    if not (vendor_id == vendor_id_real and auth['role'] =='vendor'):
        raise HTTPException(status_code=403, detail="Invalid vendor_id")

    tags: List[str] = parse_tag_names(item.tags)
    pool = request.app.state.pool
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            for tag_name in tags:
                try:
                    await cur.execute("""
                        INSERT INTO tags(tag_name) VALUES (%s);
                    """, (tag_name,))
                except:
                    pass 
            await cur.execute(f"SELECT tag_id FROM tags WHERE tag_name IN ({','.join(['%s']*len(tags))});", tuple(tags))
            tag_ids = await cur.fetchall()
            # 本表
            await cur.execute("INSERT INTO products (product_name, product_cover, product_info, price, product_score) VALUES (%s, %s, %s, %s, 5);", (item.product_name, item.product_cover, item.product_info, item.price))
            product_id = cur.lastrowid
            # 标签关系
            await cur.executemany("INSERT INTO tag_product_rel (tag_id, product_id) VALUES (%s, %s);", [(tag_id, product_id) for tag_id in tag_ids])
            # 商户关系
            await cur.execute("INSERT INTO vendor_product_rel (vendor_id, product_id) VALUES (%s, %s);", (vendor_id, product_id))
            await conn.commit()
            res = deepcopy(RESPONSE)
            return res

async def delete_product_handler(request: Request, item: DeleteProductItem, auth: Annotated[dict, Depends(authentication)]):
    vendor_id = item.vendor_id
    vendor_id_real = auth["rid"]
    if not (vendor_id == vendor_id_real and auth['role'] =='vendor'):
        raise HTTPException(status_code=403, detail="Invalid vendor_id")

    pool = request.app.state.pool
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:

            # 可以做有尚存订单的合法性检查，demo里估计没时间展示，未做。

            await cur.execute("DELETE FROM vendor_product_rel WHERE vendor_id = %s AND product_id = %s;", (vendor_id, item.product_id))
            await cur.execute("DELETE FROM tag_product_rel WHERE product_id = %s;", (item.product_id,))
            # tag保留，有溢出问题，不处理
            await cur.execute("DELETE FROM products WHERE product_id = %s;", (item.product_id,))
            if cur.rowcount > 0:
                await conn.commit()
                res = deepcopy(RESPONSE)
                return res
            else:
                res = deepcopy(RESPONSE)
                res["data"]["success"] = 0
                return res

async def express_order_handler(request: Request, item: ExpressItem, auth: Annotated[dict, Depends(authentication)]):
    vendor_id = item.vendor_id
    vendor_id_real = auth["rid"]
    if not (vendor_id == vendor_id_real and auth['role'] =='vendor'):
        raise HTTPException(status_code=403, detail="Invalid vendor_id")

    res = deepcopy(RESPONSE)
    pool = request.app.state.pool
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT DISTINCT vendor_id FROM vendor_product_rel WHERE product_id=(SELECT DISTINCT product_id FROM orders WHERE order_id=%s);", (item.order_id,))
            orders_vendor_id = await cur.fetchone()
            if orders_vendor_id is None or orders_vendor_id[0] != vendor_id:
                raise HTTPException(status_code=403, detail="Invalid vendor_id")
            await cur.execute("UPDATE orders SET express_number = %s, status = 'shipping' WHERE order_id = %s AND status='paid'", (item.express_number, item.order_id))
            if cur.rowcount > 0:
                await cur.execute("SELECT parent_order_id FROM orders WHERE order_id = %s", (item.order_id, ))
                parent_order_id = await cur.fetchone()
                if parent_order_id[0] == item.order_id:
                    # 是母订单
                    await cur.execute("UPDATE orders SET express_number = %s, status = 'shipping' WHERE parent_order_id = %s AND status='paid'", (item.express_number, item.order_id))
                else:
                    # 是子订单
                    await cur.execute("SELECT count(order_id) FROM orders WHERE parent_order_id = %s AND status='paid'", (parent_order_id[0], ))
                    if (await cur.fetchone())[0] == 1:
                        await cur.execute("UPDATE orders SET express_number = %s, status = 'shipping' WHERE order_id = %s AND status='paid'", (item.express_number, parent_order_id[0]))
                await conn.commit()
            else:
                res["data"]["success"] = 0
            return res

async def request_vendor_orders_handler(request: Request, item: RequestVemdorOrdersItem, auth: Annotated[dict, Depends(authentication)]):
    vendor_id = item.vendor_id
    vendor_id_real = auth["rid"]
    if not (vendor_id == vendor_id_real and auth['role'] =='vendor'):
        raise HTTPException(status_code=403, detail="Invalid vendor_id")

    pool = request.app.state.pool
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("""
                SELECT order_id, user_id, parent_order_id, product_id, quantity, total_price, place_time, status, express_number FROM orders WHERE product_id IN (SELECT product_id FROM vendor_product_rel WHERE vendor_id = %s) ORDER BY place_time DESC;
            """, (vendor_id,))
            orders = await cur.fetchall()
            res = deepcopy(RESPONSE)
            res["data"]["orders"] = list([dict(zip(["order_id", "user_id", "parent_order_id", "product_id", "quantity", "total_price", "place_time", "status", "express_number"], order)) for order in orders])
            return res

async def delete_order_handler(request: Request, item: DeleteOrderItem, auth: Annotated[dict, Depends(authentication)]):
    vendor_id = item.vendor_id
    vendor_id_real = auth["rid"]
    if not (vendor_id == vendor_id_real and auth['role'] =='vendor'):
        raise HTTPException(status_code=403, detail="Invalid vendor_id")

    res = deepcopy(RESPONSE)
    pool = request.app.state.pool
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            res = deepcopy(RESPONSE)
    pool = request.app.state.pool
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            try:
                await conn.begin()
                # 已付款余额退款
                await cur.execute("SELECT DISTINCT user_id FROM orders WHERE order_id = %s", (item.order_id,))
                user_id = await cur.fetchone()
                if user_id is None:
                    raise Exception('a')
                user_id = user_id[0]
                await cur.execute("SELECT total_price FROM orders WHERE order_id = %s and status = 'paid' and user_id = %s", (item.order_id, user_id))
                total_price = await cur.fetchone()
                if total_price is not None:
                    total_price = total_price[0]
                    await cur.execute("UPDATE users SET balance = balance + %s WHERE user_id = %s;", (total_price, user_id))
                await cur.execute("DELETE FROM orders WHERE order_id = %s and user_id = %s and status IN ('placed', 'paid');", (item.order_id, user_id))
                ar1 = cur.rowcount
                await cur.execute("DELETE FROM orders WHERE parent_order_id = %s and user_id = %s and status IN ('placed', 'paid');", (item.order_id, user_id))
                ar2 = cur.rowcount
                assert (ar1 + ar2) > 0
            except Exception as e:
                await conn.rollback()
                res["data"]["success"] = 0
                return res 
            else:
                await conn.commit()
                return res

async def admin_person_list_handler(request: Request, auth: Annotated[dict, Depends(authentication)], entity: Literal['users', 'vendors']='users'):
    admin_id_real = auth["rid"]
    if not (admin_id_real == 1 and auth['role'] =='admin'):
        raise HTTPException(status_code=403, detail="Invalid authentication")
    
    res = deepcopy(RESPONSE)
    pool = request.app.state.pool
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            if entity == 'users':
                await cur.execute(f"SELECT user_id, user_display_name, balance FROM users;")
            elif entity == 'vendors':
                await cur.execute(f"""
                    SELECT v.vendor_id, v.vendor_display_name, COUNT(vpr.product_id) AS product_count
                    FROM vendors v
                    LEFT JOIN vendor_product_rel vpr ON v.vendor_id = vpr.vendor_id
                    GROUP BY v.vendor_id;
                """)
            rdata = await cur.fetchall()
            if entity == 'users':
                res["data"]["users"] = list([dict(zip(["user_id", "user_display_name", "balance"], user)) for user in rdata])
            elif entity == 'vendors':
                res["data"]["vendors"] = list([dict(zip(["vendor_id", "vendor_display_name", "product_count"], vendor)) for vendor in rdata])
            return res

async def admin_person_delete_handler(request: Request, item: DeleteUserItem, auth: Annotated[dict, Depends(authentication)]):
    admin_id_real = auth["rid"]
    if not (admin_id_real == 1 and auth['role'] =='admin'):
        raise HTTPException(status_code=403, detail="Invalid authentication")

    entity = item.role
    res = deepcopy(RESPONSE)
    pool = request.app.state.pool
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            if entity == 'users':
                # 未完成订单检查
                await cur.execute("SELECT order_id FROM orders WHERE user_id = %s", (item.user_id,))
                orders = await cur.fetchall()
                if len(orders) > 0:
                    res["data"]["success"] = 0
                    res["data"]["message"] = "User has unfinished orders"
                    return res
                try:
                    await cur.execute("DELETE FROM users WHERE user_id = %s", (item.user_id,))
                    if cur.rowcount > 0:
                        await conn.commit()
                        return res
                    else:
                        res["data"]["success"] = 0
                        return res
                except:
                    res["data"]["success"] = 0
                    return res
            if entity == 'vendors':
                try:
                    await cur.execute("DELETE FROM vendors WHERE vendor_id = %s", (item.vendor_id,))
                    if cur.rowcount > 0:
                        await conn.commit()
                        return res
                    else:
                        res["data"]["success"] = 0
                        return res
                except:
                    res["data"]["success"] = 0
                    return res


async def admin_user_create_handler(request: Request, item: CreateUserItem, auth: Annotated[dict, Depends(authentication)]):
    admin_id_real = auth["rid"]
    if not (admin_id_real == 1 and auth['role'] =='admin'):
        raise HTTPException(status_code=403, detail="Invalid authentication")

    res = deepcopy(RESPONSE)
    pool = request.app.state.pool
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            try:
                await cur.execute("SELECT user_id FROM users WHERE user_username = %s;", (item.user_username,))
                if (await cur.fetchone()) is not None:
                    res["data"]["success"] = 0
                    res["data"]["message"] = "Username already exists"
                    return res
                await cur.execute("INSERT INTO users (user_username, user_password, user_display_name, avatar, address, telephone_number, balance) VALUES (%s, %s, %s, %s, %s, %s, 0);", (item.user_username, item.user_password, item.user_display_name, item.avatar, item.address, item.telephone_number))
                await conn.commit()
                return res
            except Exception as e:
                res["data"]["success"] = 0
                res["data"]["message"] = "Display username already exists"
                return res
            
async def admin_vendor_create_handler(request: Request, item: CreateVendorItem, auth: Annotated[dict, Depends(authentication)]):
    admin_id_real = auth["rid"]
    if not (admin_id_real == 1 and auth['role'] =='admin'):
        raise HTTPException(status_code=403, detail="Invalid authentication")

    res = deepcopy(RESPONSE)
    pool = request.app.state.pool
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            try:
                await cur.execute("SELECT vendor_id FROM vendors WHERE vendor_username = %s;", (item.vendor_username,))
                if (await cur.fetchone()) is not None:
                    res["data"]["success"] = 0
                    res["data"]["message"] = "Username already exists"
                    return res
                await cur.execute("INSERT INTO vendors (vendor_username, vendor_password, vendor_display_name, origin_address, vendor_score, avatar, balance) VALUES (%s, %s, %s, %s, 5, %s, 0);", (item.vendor_username, item.vendor_password, item.vendor_display_name, item.origin_address, item.avatar))
                await conn.commit()
                return res
            except:
                res["data"]["success"] = 0
                return res
            
