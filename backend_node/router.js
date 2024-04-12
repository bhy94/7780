const express = require('express');
const router = express.Router();
const { get_user_info_handler, get_product_info_handler, login_handler, logout_handler, create_order_handler, user_recieve_order_handler, request_payment_handler, request_user_orders_handler, user_register_handler, user_deposit_handler } = require('./views');

router.get('/', (req, res) => {
    res.send('Hello World!');
});

// GET
router.get('/api/users/info', get_user_info_handler);
router.get('/api/products/info', get_product_info_handler);

// POST
router.post('/api/login', login_handler);
router.post('/api/logout', logout_handler);
router.post('/api/products', logout_handler);
router.post('/api/users/orders/create', create_order_handler);
router.post('/api/orders/recieve', user_recieve_order_handler);
router.post('/api/payments/pay', request_payment_handler);
router.post('/api/users/orders', request_user_orders_handler);
router.post('/api/register', user_register_handler);
router.post('/api/users/deposit', user_deposit_handler);

module.exports = router;