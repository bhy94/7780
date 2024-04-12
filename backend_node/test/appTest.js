const chai = require('chai');
const chaiHttp = require('chai-http');
const { expect } = chai;
const app = require('../app'); // 确保你的Express app可以被引入

chai.use(chaiHttp);

describe('API Integration Tests', () => {
    // 测试用户注册
    describe('POST /register', () => {
        it('should register a new user', (done) => {
            chai.request(app)
                .post('/register')
                .send({ username: 'newuser', password: 'newpassword', email: 'newuser@example.com' })
                .end((err, res) => {
                    expect(res).to.have.status(201);
                    expect(res.body).to.have.property('message', 'User registered successfully');
                    done();
                });
        });
    });

    // 测试用户登录
    describe('POST /login', () => {
        it('should login the user', (done) => {
            chai.request(app)
                .post('/login')
                .send({ username: 'testuser', password: 'password' })
                .end((err, res) => {
                    expect(res).to.have.status(200);
                    expect(res.body).to.have.property('token');
                    done();
                });
        });
    });

    // 测试获取用户信息
    describe('GET /user-info', () => {
        it('should get user information', (done) => {
            chai.request(app)
                .get('/user-info')
                .set('Authorization', 'Bearer token') // 假设需要token
                .end((err, res) => {
                    expect(res).to.have.status(200);
                    expect(res.body).to.be.an('object');
                    done();
                });
        });
    });

    // 测试用户登出
    describe('POST /logout', () => {
        it('should logout the user', (done) => {
            chai.request(app)
                .post('/logout')
                .end((err, res) => {
                    expect(res).to.have.status(200);
                    expect(res.body).to.have.property('message', 'User logged out successfully');
                    done();
                });
        });
    });

    // 测试创建订单
    describe('POST /create-order', () => {
        it('should create an order', (done) => {
            chai.request(app)
                .post('/create-order')
                .send({ productId: '123', quantity: 2 })
                .end((err, res) => {
                    expect(res).to.have.status(201);
                    expect(res.body).to.have.property('orderId');
                    done();
                });
        });
    });

    // 测试请求支付
    describe('POST /request-payment', () => {
        it('should request payment for an order', (done) => {
            chai.request(app)
                .post('/request-payment')
                .send({ orderId: '1234' })
                .end((err, res) => {
                    expect(res).to.have.status(200);
                    expect(res.body).to.have.property('paymentUrl');
                    done();
                });
        });
    });

    // 测试用户接收订单
    describe('POST /receive-order', () => {
        it('should mark an order as received', (done) => {
            chai.request(app)
                .post('/receive-order')
                .send({ orderId: '1234' })
                .end((err, res) => {
                    expect(res).to.have.status(200);
                    expect(res.body).to.have.property('message', 'Order marked as received');
                    done();
                });
        });
    });

    // 测试请求用户订单
    describe('GET /user-orders', () => {
        it('should get all orders for a user', (done) => {
            chai.request(app)
                .get('/user-orders')
                .set('Authorization', 'Bearer token') // 假设需要token
                .end((err, res) => {
                    expect(res).to.have.status(200);
                    expect(res.body).to.be.an('array');
                    done();
                });
        });
    });

    // 测试用户存款
    describe('POST /deposit', () => {
        it('should deposit money into user account', (done) => {
            chai.request(app)
                .post('/deposit')
                .send({ amount: 100 })
                .end((err, res) => {
                    expect(res).to.have.status(200);
                    expect(res.body).to.have.property('balance');
                    done();
                });
        });
    });
});