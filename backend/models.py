from pydantic import BaseModel
from typing import List, Optional, Literal

RESPONSE = {
    "code": 200,
    "data": {
        "success": 1,
        "message": "",
    }
}

class LoginItem(BaseModel):
    username: str
    password: str
    destination: Literal["back_end", "front_end"]

class LogoutItem(BaseModel):
    user_id: int

class RequestProductsItem(BaseModel):
    tags: str
    vendor_id: Optional[int] 

class OrderProductItem(BaseModel):
    product_id: int
    quantity: int

class OrdersCreateItem(BaseModel):
    user_id: int
    items: List[OrderProductItem]

class PaymentItem(BaseModel):
    user_id: int
    order_id: int

class RequestUserOrdersItem(BaseModel):
    user_id: int

class CancelOrderItem(BaseModel):
    user_id: int
    order_id: int

class RequestDepositItem(BaseModel):
    user_id: int
    balance_add: float

class RequestVendorProductsItem(BaseModel):
    vendor_id: int

class CreateProductItem(BaseModel):
    vendor_id: int
    product_name: str
    product_cover: str
    product_info: str
    tags: str
    price: float

class DeleteProductItem(BaseModel):
    vendor_id: int
    product_id: int

class ExpressItem(BaseModel):
    vendor_id: int
    order_id: int
    express_number: str

class RequestVemdorOrdersItem(BaseModel):
    vendor_id: int

class DeleteOrderItem(BaseModel):
    vendor_id: int
    order_id: int

class DeleteUserItem(BaseModel):
    user_id: int
    vendor_id: int
    role: Literal["users", "vendors"]


class CreateUserItem(BaseModel):
    user_username: str
    user_password: str
    user_display_name: str
    address: str
    avatar: str
    telephone_number: str

class CreateVendorItem(BaseModel):
    vendor_username: str
    vendor_password: str
    vendor_display_name: str
    origin_address: str
    avatar: str