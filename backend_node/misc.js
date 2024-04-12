const db = require('./database');


// db.getConnection((err, connection) => {});

// 查询
db.query('SELECT user_id FROM users WHERE user_username = ? AND user_password = ?;', ['alice1', 'alice1123'], (err, results) => {
    console.log(results[0]);
});

// // 释放连接
// db.getConnection((err, connection) => {
//     connection.release();
// });


// function create_random_uuid() {
//     return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
//         const r = Math.random() * 16 | 0;
//         const v = c == 'x' ? r : (r & 0x3 | 0x8);
//         return v.toString(16);
//     });
// }

// for (let i = 0; i < 10; i++) {
//     console.log(create_random_uuid());
// }
// const d = new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString().slice(0, 19).replace('T', ' ');
// console.log(d)