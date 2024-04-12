from views import *
from fastapi.responses import JSONResponse
from functools import partial

class Router:

    def __init__(self, app):
        self.app = app
    
    def install(self):
        
        self.app.get("/api/products/info", response_class=JSONResponse)(get_product_info_handler)
        self.app.get("/api/users/info", response_class=JSONResponse)(get_user_info_handler)
        self.app.get("/api/vendors/info", response_class=JSONResponse)(get_vendor_info_handler)
        self.app.get("/api/vendors/deposits", response_class=JSONResponse)(get_deposits_handler)

        self.app.post("/api/login", response_class=JSONResponse)(login_handler)
        self.app.post("/api/logout", response_class=JSONResponse)(logout_handler)
        self.app.post("/api/register", response_class=JSONResponse)(user_register)
        self.app.post("/api/products", response_class=JSONResponse)(request_products_handler)
        self.app.post("/api/users/orders/create", response_class=JSONResponse)(create_order_handler)
        self.app.post("/api/payments/pay", response_class=JSONResponse)(request_payment_handler)
        self.app.post("/api/users/orders", response_class=JSONResponse)(request_user_orders_handler)
        self.app.post("/api/orders/delete", response_class=JSONResponse)(user_cancel_order_handler)
        self.app.post("/api/orders/recieve", response_class=JSONResponse)(user_recieve_order_handler)
        self.app.post("/api/users/deposit", response_class=JSONResponse)(user_deposit_handler)
        self.app.post("/api/vendors/products", response_class=JSONResponse)(request_vendor_products_handler)
        self.app.post("/api/vendors/products/create", response_class=JSONResponse)(create_product_handler)
        self.app.post("/api/vendors/products/delete", response_class=JSONResponse)(delete_product_handler)
        self.app.post("/api/vendors/orders/express", response_class=JSONResponse)(express_order_handler)
        self.app.post("/api/vendors/orders", response_class=JSONResponse)(request_vendor_orders_handler)
        self.app.post("/api/vendors/orders/delete", response_class=JSONResponse)(delete_order_handler)

        # sudo 
        self.app.post("/api/admin/users", response_class=JSONResponse)(partial(admin_person_list_handler, entity="users"))
        self.app.post("/api/admin/vendors", response_class=JSONResponse)(partial(admin_person_list_handler, entity="vendors"))
        self.app.post("/api/admin/users/create", response_class=JSONResponse)(admin_user_create_handler)
        self.app.post("/api/admin/users/delete", response_class=JSONResponse)(admin_person_delete_handler)
        self.app.post("/api/admin/vendors/create", response_class=JSONResponse)(admin_vendor_create_handler)
        self.app.post("/api/admin/vendors/delete", response_class=JSONResponse)(admin_person_delete_handler)

        # front-end
        # self.app.get("/")(read_root)
        