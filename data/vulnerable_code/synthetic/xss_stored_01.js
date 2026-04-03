const express = require('express');
const app = express();
const comments = [];

app.use(express.urlencoded({ extended: true }));

app.post('/comment', (req, res) => {
    /* BUG: comment body stored and rendered without sanitization */
    comments.push({ author: req.body.author, text: req.body.text });
    res.redirect('/comments');
});

app.get('/comments', (req, res) => {
    let html = '<html><body><h1>Comments</h1>';
    for (const c of comments) {
        /* BUG: user content inserted directly into HTML */
        html += `<div><b>${c.author}</b>: ${c.text}</div>`;
    }
    html += '</body></html>';
    res.send(html);
});

app.listen(3000);
