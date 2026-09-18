const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf-8');
const match = html.match(/<script>(.*?)<\/script>/s);
if (match) {
    fs.writeFileSync('script.js', match[1]);
}
