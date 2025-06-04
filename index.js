const { default: makeWASocket, useSingleFileAuthState } = require('@adiwajshing/baileys');
const axios = require('axios');
const fs = require('fs');
const path = require('path');

// Auth state
const { state, saveState } = useSingleFileAuthState(path.join(__dirname, './auth_info.json'));

async function startBot() {
    const sock = makeWASocket({
        auth: state,
        printQRInTerminal: true,
    });

    sock.ev.on('creds.update', saveState);

    sock.ev.on('messages.upsert', async ({ messages }) => {
        const msg = messages[0];
        if (!msg.message) return;

        const from = msg.key.remoteJid;
        const text = msg.message.conversation || msg.message.extendedTextMessage?.text || '';

        if (/^\d{13}$/.test(text)) {
            try {
                const response = await axios.get(`https://famofc.kesug.com/apis/fbi.php?cnic=${text}`);
                await sock.sendMessage(from, { text: response.data });
            } catch (error) {
                await sock.sendMessage(from, { text: '❌ Failed to fetch data. Try again later.' });
            }
        } else {
            await sock.sendMessage(from, { text: '📥 Please send a valid 13-digit CNIC number without dashes.' });
        }
    });
}

startBot();
