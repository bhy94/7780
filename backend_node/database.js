const mysql = require('mysql');
const pool = mysql.createPool({
    host: 'db1',
    port: 3306,
    user: 'root',
    password: '123456',
    database: 'shop',
});

module.exports = pool;