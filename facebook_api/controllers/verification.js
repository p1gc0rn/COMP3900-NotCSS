module.exports = (req, res) => {
 const hubChallenge = req.query['hub.challenge'];
const hubMode = req.query['hub.mode'];
 const verifyTokenMatches = (req.query['hub.verify_token'] === 'messenger_webhook');
if (hubMode && verifyTokenMatches) {
 res.status(200).send(hubChallenge);
 console.log('Verified');
 } else {
 res.status(403).end();
 }
};
