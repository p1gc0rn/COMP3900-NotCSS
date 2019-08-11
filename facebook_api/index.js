const express = require('express');
const bodyParser = require('body-parser');
const app = express();
const port = 8765;

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.listen(port, () => console.log('Webhook server is listening on port'));

const verificationController = require('./controllers/verification');
const messageWebhookController = require('./controllers/messageWebhook');
app.get('/', verificationController);
app.post('/', messageWebhookController);
