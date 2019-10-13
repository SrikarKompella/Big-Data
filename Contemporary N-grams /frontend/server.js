const express = require('express');

const app = express();
const port = process.env.PORT || 3000;

app.use(express.static('build'));

app.get('/', function(req, res) {
  res.sendFile('build/index.html');
});

app.listen(port, () => console.log(`Listening on port ${port}`));
