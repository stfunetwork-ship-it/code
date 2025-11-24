// moderation.js — Node/Express / Socket.IO style pseudocode

const mutedUserIds = new Set();   // persist in DB for production
const tempMutes = new Map();      // userId -> unmuteTimestamp

function isMuted(userId) {
  const ts = tempMutes.get(userId);
  if (mutedUserIds.has(userId)) return true;
  if (ts && Date.now() < ts) return true;
  if (ts && Date.now() >= ts) {
    tempMutes.delete(userId);
  }
  return false;
}

const keywordList = ['buy now', 'free money', 'threaten', 'kill']; // configurable

function matchesKeyword(text) {
  const l = text.toLowerCase();
  return keywordList.some(k => l.includes(k));
}

// socket message handler
io.on('connection', (socket) => {
  socket.on('send_message', ({ userId, text }) => {
    if (isMuted(userId)) {
      socket.emit('message_blocked', { reason: 'muted' });
      return;
    }
    if (matchesKeyword(text)) {
      // warn & temp mute
      tempMutes.set(userId, Date.now() + 10 * 60 * 1000); // 10 min
      socket.emit('warn', { message: 'Your message violates rules and you are temporarily muted.'});
      return;
    }
    // broadcast message normally
    io.emit('message', { userId, text });
  });
});

// Admin endpoints
app.post('/admin/mute', (req, res) => {
  const { userId } = req.body;
  mutedUserIds.add(userId);
  res.send({ ok: true });
});
