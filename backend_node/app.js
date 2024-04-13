const express = require('express');
const app = express();
const router = require('./router');
const cookieParser = require('cookie-parser');



// use express.json() middleware to parse JSON bodies
app.use(express.json());
// use router
app.use(router);
// use cookieParser middleware
app.use(cookieParser());
// routing static files
app.use(express.static('assets'));

app.listen(8080, () => {
    console.log('Server is running on http://localhost:8080');
});
