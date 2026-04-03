const http = require('http');
const url = require('url');

const server = http.createServer((req, res) => {
    const query = url.parse(req.url, true).query;
    // BUG: user input inserted into HTML without escaping
    const name = query.name || 'World';
    res.writeHead(200, {'Content-Type': 'text/html'});
    res.end(`<html><body><h1>Hello, ${name}!</h1></body></html>`);
});

server.listen(3000);
