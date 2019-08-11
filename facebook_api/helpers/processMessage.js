const API_AI_TOKEN = '457b41645fa14fdca0606a315b73543c';
const apiAiClient = require('apiai')(API_AI_TOKEN);
const FACEBOOK_ACCESS_TOKEN = 'EAAKHZBfVStz4BAIMt0s41RPSZC567cCLsEwKj0oJld4fKz4YOYOr6S5HXB2vcptY8Lk4voqyLJJXupCiHiNPhDUZAzBA0wFwDfvu6J4oZA6dZA8oOaf0Yt42ouSBWiZARToLBvlBV3AocENANM117jSR5cX9u4lOLcYfVoeLZA1SIm2129XAOw7';
const request = require('request');
const sendTextMessage = (senderId, text) => {
 request({
 url: 'https://graph.facebook.com/v2.6/me/messages',
 qs: { access_token: FACEBOOK_ACCESS_TOKEN },
 method: 'POST',
 json: {
 recipient: { id: senderId },
 message: { text },
 }
 });
};
module.exports = (event) => {
 const senderId = event.sender.id;
 const message = event.message.text;
const apiaiSession = apiAiClient.textRequest(message, {sessionId: 'messenger_webhook'});
apiaiSession.on('response', (response) => {
 const result = response.result.fulfillment.speech;
sendTextMessage(senderId, result);
console.log('sent');
 });
apiaiSession.on('error', error => console.log(error));
 apiaiSession.end();
};
