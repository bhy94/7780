const db = require('./database');


function create_random_uuid() {
  // 生成一个随机的UUID
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        const r = Math.random() * 16 | 0;
        const v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

function get_user_info_handler(req, res) {
  // 获取指定用户信息（单个）
    const user_id = req.params.user_id;
    const auth = req.auth;
    const user_id_real = auth.rid;
    if (!(user_id == user_id_real && auth.role == 'user')) {
        res.status(403).send('Invalid user_id');
        return;
    }

    db.query('SELECT user_id, user_username, user_display_name, avatar, address, telephone_number, balance FROM users WHERE user_id = ?;', [user_id], (err, results) => {
        if (err) {
            res.status(500).send('Internal Server Error');
            return;
        }
        if (results.length <= 0) {
            res.json({
                success: 0,
                message: 'no such user'
            });
            return;
        }
        const ret = results[0];
        res.json({
          code: 200,
          data: {
            success: 1,
            message: "",
            user_id: ret[0],
            user_username: ret[1],
            user_display_name: ret[2],
            avatar: ret[3],
            address: ret[4],
            telephone_number: ret[5],
            balance: ret[6]
          }
        });
    });
}

function get_product_info_handler(req, res) {
  // 获取指定商品信息（单个）
    const product_id = req.query.product_id;
    db.query('SELECT product_id, product_name, product_cover, product_info, price, product_score FROM products WHERE product_id = ?;', [product_id], (err, results) => {
        if (err) {
            res.status(500).send('Internal Server Error');
            return;
        }
        if (results.length <= 0) {
            res.json({
              code: 200,
              data: {
                success: 0,
                message: 'no such product'
              }
            });
            return;
        }
        const ret = results[0];
        db.query('SELECT tag_name FROM tags WHERE tag_id IN (SELECT DISTINCT tag_id FROM tag_product_rel WHERE product_id = ?);', [product_id], (err, results) => {
            if (err) {
                res.status(500).send('Internal Server Error');
                return;
            }
            const tags = results.map(x => x.tag_name);
            db.query('SELECT vendor_id, vendor_display_name, avatar, origin_address FROM vendors WHERE vendor_id IN (SELECT DISTINCT vendor_id FROM vendor_product_rel WHERE product_id = ?);', [product_id], (err, results) => {
                if (err) {
                    res.status(500).send('Internal Server Error');
                    return;
                }
                const ress = results[0];
                let address = '';
                if (ress) {
                    address = ress.origin_address;
                }
                res.json({
                  code: 200,
                  data: {
                    success: 1,
                    message: "",
                    tags: tags,
                    vendor_id: ress.vendor_id,
                    vendor_display_name: ress.vendor_display_name,
                    vendor_avatar: ress.avatar,
                    origin_address: address,
                    product_id: ret.product_id,
                    product_name: ret.product_name,
                    product_cover: [ret.product_cover],
                    product_info: ret.product_info,
                    price: ret.price,
                    product_score: ret.product_score
                  }
                });
            });
        });
    });
}


function login_handler(req, res) {
  // 登录
    const item = req.body;
    const destination = item.destination;
    if (destination == 'front_end') {
        db.query('SELECT user_id FROM users WHERE user_username = ? AND user_password = ?;', [item.username, item.password], (err, results) => {
            if (err) {
                res.status(403).send('Internal Server Error');
                return;
            }
            const uid = results[0];
            if (uid != undefined) {
              const uiduid = uid.user_id
                const uuid_ = create_random_uuid();
                const expire_time = new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString().slice(0, 19).replace('T', ' ');
                db.query('INSERT INTO login_status_user (user_id, token, expire_time) VALUES (?, ?, ?);', [uiduid, uuid_, expire_time], (err, results) => {
                    if (err) {
                        res.status(500).send('Internal Server Error');
                        return;
                    }
                    res.json({
                      code: 200,
                      data: {
                        success: 1,
                        message: "",
                        user_id: uiduid,
                        token: uuid_,
                        role: 'user'
                      }
                    });
                });
            } else {
                res.json({
                  code: 200,
                  data: {
                    success: 0,
                    message: "",
                    user_id: 0,
                    token: "",
                    role: 'user'
                  }
                });
            }
        })
    } else {
            db.query('SELECT vendor_id FROM vendors WHERE vendor_username = ? AND vendor_password = ?;', [item.username, item.password], (err, results) => {
                if (err) {
                    res.status(500).send('Internal Server Error');
                    return;
                }
                const vid = results[0];
                if (vid) {
                  res.json({
                    code: 200,
                    data: {
                      success: 0,
                      message: "",
                      user_id: 0,
                      token: "",
                      role: 'user'
                    }
                  });
                }
            });
    }
}

function logout_handler(req, res) {
  // 登出  
  const role = req.cookies.role;
    const rid = req.cookies.user_id;
    const sid = req.cookies.token;
    let table = '';
    let col = '';
    if (role == 'admin') {
        table = 'login_status_admin';
        col = 'admin_id';
    } else if (role == 'vendor') {
        table = 'login_status_vendor';
        col = 'vendor_id';
    } else if (role == 'user') {
        table = 'login_status_user';
        col = 'user_id';
    } else {
        res.status(503).send('Invalid role');
        return;
    }
    db.query(`DELETE FROM ${table} WHERE ${col} = ? AND token = ?;`, [rid, sid], (err, results) => {
        if (err) {
            res.status(500).send('Internal Server Error');
            return;
        }
        let delete_success = false;
        if (results.affectedRows > 0) {
            delete_success = true;
        }
        res.json({
          code: 200,
          data: {
            success: 1,
            message: "",
          }
        });
    });
}

function create_order_handler(req, res) {
  // 创建订单  
  
  const order_details = req.body;

    if (order_details.items.length <= 0) {
        res.status(400).send('No items in order');
        return;
    }
    const order_time = new Date(Date.now()).toISOString().slice(0, 19).replace('T', ' ');
    let items = order_details.items;
    if (items.length <= 0) {
        res.status(400).send('No items in order');
        return;
    }


    const items2 = [];
    for (let item of items) {
        item = JSON.parse(JSON.stringify(item))
        let new_item = {
            product_id: item.product_id,
            quantity: item.quantity,
            price: 0,
            total_price: 0
        }
        db.query('SELECT price FROM products WHERE product_id = ?;', [new_item.product_id], (err, results) => {
            if (err) {
                res.status(500).send('Internal Server Error');
                return;
            }
            let price = results[0];
            
            if (price == undefined) {
              res.status(400).send('No items in order');
              return;
            }
            price = price.price
            new_item.price = price;
            new_item.total_price = price * new_item.quantity;
        });
        items2.push(new_item);
    }
    items = items2;

    const all_total_price = items.reduce((acc, cur) => acc + cur.total_price, 0);
    if (items.length == 1) {
        db.query('INSERT INTO orders (user_id, parent_order_id, product_id, quantity, total_price, place_time, status, express_number) VALUES (?, 0, ?, ?, ?, ?, "placed", "");', [order_details.user_id, items[0].product_id, items[0].quantity, items[0].total_price, order_time], (err, results) => {
            if (err) {
                res.status(500).send('Internal Server Error');
            }
            
            db.query('UPDATE orders SET parent_order_id = ? WHERE order_id = ?;', [results.insertId, results.insertId], (err, results) => {
                if (err) {
                    res.status(500).send('Internal Server Error');
                }
            });
        });
    } else {
        db.query('INSERT INTO orders (user_id, parent_order_id, product_id, quantity, total_price, place_time, status, express_number) VALUES (?, 0, ?, 0, ?, ?, "placed", "");', [order_details.user_id, items[0].product_id, all_total_price, order_time], (err, results) => {
            if (err) {
                res.status(500).send('Internal Server Error');
                return;
            }
            const order_id = results.insertId;
            db.query('UPDATE orders SET parent_order_id = ? WHERE order_id = ?;', [order_id, order_id], (err, results) => {
                if (err) {
                    res.status(500).send('Internal Server Error');
                    return;
                }
            });
            const values = items.map(item => [order_details.user_id, order_id, item.product_id, item.quantity, item.total_price, order_time]);
            db.query('INSERT INTO orders (user_id, parent_order_id, product_id, quantity, total_price, place_time, status, express_number) VALUES ?;', [values], (err, results) => {
                if (err) {
                    res.status(500).send('Internal Server Error');
                    return;
                }
            });
        });
        return res.json({
          code: 200,
          data: {
            success: 1,
            message: ""
          }
        });
      }
}



function user_recieve_order_handler(req, res) {
  // 用户确认收货
    const item = req.body;
    const order_id = item.order_id;
    db.query('UPDATE orders SET status = "recieved" WHERE order_id = ? and status="shipping";', [order_id], (err, results) => {
        if (err) {
            res.status(500).send('Internal Server Error');
            return;
        }
        const a = results.affectedRows;
        db.query('UPDATE orders SET status = "recieved" WHERE parent_order_id = ? and status="shipping";', [order_id], (err, results) => {
            if (err) {
                res.status(500).send('Internal Server Error');
                return;
            }
            const b = results.affectedRows;
            if (a + b > 0) {
                res.json({
                  code: 200,
                  data: {
                    success: 1,
                    message: ""
                  }
                });
            } else {
                res.json({
                  code: 400,
                  data: {
                    success: 0,
                    message: ""
                  }
                });
            }
        });
    });
}

function request_payment_handler(req, res) {
  // 请求支付
    const payment = req.body;
    const user_id = payment.user_id;
    console.log(user_id);

    const order_id = payment.order_id;
    db.query('SELECT parent_order_id, total_price FROM orders WHERE order_id = ? and status="placed";', [order_id], (err, results) => {
        if (err) {
            res.status(500).send('Internal Server Error');
            return;
        }
        const total_price = results[0];
        if (total_price == undefined) {
            res.json({
              code: 400,
              data: {
                success: 0,
                message: "No such order"
              }
            });
            return;
        }
        const parent_order_id = total_price.parent_order_id;
        const total_price_ = total_price.total_price;
        if (parent_order_id != order_id) {
            res.json({
              code: 400,
              data: {
                success: 0,
                message: "Not a parent order"
              }
            });
            return;
        }
        db.query('SELECT balance FROM users WHERE user_id = ?;', [user_id], (err, results) => {
            if (err) {
                res.status(500).send('Internal Server Error');
                return;
            }
            const balance = results[0];
            if (balance == undefined) {
                res.json({
                  code: 400,
                  data: {
                    success: 0,
                    message: "No such user"
                  }
                });
                return;
            }
            const balance_ = balance.balance;
            if (balance_ < total_price_) {
                res.json({
                  code: 200,
                  data: {
                    success: 0,
                    message: "Insufficient balance"
                  }
                });
                return;
            }
            db.query('UPDATE users SET balance = balance - ? WHERE user_id = ?;', [total_price_, user_id], (err, results) => {
                if (err) {
                    res.status(500).send('Internal Server Error');
                    return;
                }
                if (results.affectedRows <= 0) {
                    res.json({
                      code: 200,
                      data: {
                        success: 0,
                        message: ""
                      }
                    });
                    return; 
                  }
                });
            db.query('UPDATE orders SET status = "paid" WHERE order_id = ? and status="placed";', [order_id], (err, results) => {
                if (err) {
                    res.status(500).send('Internal Server Error');
                    return;
                }
                if (results.affectedRows <= 0) {
                    res.json({
                      code: 200,
                      data: {
                        success: 0,
                        message: ""
                      }
                    });
                    return; 
                  }
                });

              });
            })
}


function request_user_orders_handler(req, res) {
  // 获取用户订单信息（批量）
    const item = req.body;
    const user_id = item.user_id;

    db.query('SELECT a.order_id, a.parent_order_id, a.product_id, a.quantity, a.total_price, a.place_time, a.status , b.product_name, a.express_number FROM orders a LEFT JOIN products b ON a.product_id = b.product_id WHERE user_id = ?;', [user_id], (err, results) => {
        if (err) {
            res.status(500).send('Internal Server Error');
            return;
        }
        const orders = results;
        const result = {};
        for (let order of orders) {
            let target = result[order.parent_order_id];
            if (target == undefined) {
                target = {
                    order_id: null,
                    total_price: null,
                    place_time: null,
                    status: null,
                    items: []
                };
            }
            if (target.order_id == null) {
                express_number = order.express_number;
            }
            target.order_id = order.parent_order_id;
            target.total_price = order.total_price;
            target.place_time = order.place_time;
            target.status = order.status;
            target.items.push({
                order_id: order.order_id,
                product_id: order.product_id,
                quantity: order.quantity,
                total_price: order.total_price,
                place_time: order.place_time,
                status: order.status,
                product_name: order.product_name,
                express_number: express_number
            });
            result[order.parent_order_id] = target;
        }
        for (let key in result) {
            if (result[key].items.length > 1) {
                for (let idx in result[key].items) {
                    if (result[key].items[idx].quantity == 0) {
                        result[key].items.splice(idx, 1);
                        break;
                    }
                }
            }
        }
        res.json({
          code: 200,
          data: {
            orders: Object.values(result)
          }
        });
    });
}


function user_register_handler(req, res) {
  // 用户注册
    const item = req.body;
    db.query('SELECT user_id FROM users WHERE user_username = ?;', [item.user_username], (err, results) => {
        if (err) {
            res.status(500).send('Internal Server Error');
            return;
        }
        if (results.length > 0) {
            res.json({
              code: 200,
              data: {
                success: 0,
                message: "Username already exists"
              }
            });
            return;
        }
        db.query('INSERT INTO users (user_username, user_password, user_display_name, avatar, address, telephone_number, balance) VALUES (?, ?, ?, ?, ?, ?, 0);', [item.user_username, item.user_password, item.user_display_name, item.avatar, item.address, item.telephone_number], (err, results) => {
            if (err) {
                res.status(500).send('Internal Server Error');
                return;
            }
            res.json({
              code: 200,
              data: {
                success: 1,
                message: ""
              }
            });
        });
    });
}


function user_deposit_handler(req, res) {
  // 用户充值
    const item = req.body;
    const user_id = item.user_id;

    if (item.balance_add <= 0) {
        res.json({
          code: 200,
          data: {
            success: 0
          }
        });
        return;
    }
    db.query('UPDATE users SET balance = balance + ? WHERE user_id = ?;', [item.balance_add, user_id], (err, results) => {
        if (err) {
            res.status(500).send('Internal Server Error');
            return;
        }
        const a = results.affectedRows;
        db.query('INSERT INTO deposits (user_id, balance_add, pporder_id) VALUES (?, ?, ?);', [user_id, item.balance_add, item.pporder_id], (err, results) => {
            if (err) {
                res.status(500).send('Internal Server Error');
                return;
            }
            const b = results.affectedRows;
            if (a + b > 0) {
                res.json({
                  code: 200,
                  data: {
                    success: 1
                  }
                });
            } else {
                res.json({
                  code: 200,
                  data: {
                    success: 0
                  }
                });
            }
        });
    });
}

module.exports = {
    get_user_info_handler,
    get_product_info_handler,
    login_handler,
    logout_handler,
    create_order_handler,
    user_recieve_order_handler,
    request_payment_handler,
    request_user_orders_handler,
    user_register_handler,
    user_deposit_handler
};