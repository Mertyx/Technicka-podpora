const express = require('express');
const cors = require('cors');

const app = express();

app.use(cors());
app.use(express.json());

app.post('/chat', (req, res) => {
    const { message, student, email } = req.body;

    console.log(`Dotaz od: ${student}, zpráva: ${message}`);

    let replyText = "";
    if (message.toLowerCase().includes("platba")) {
        replyText = "Platbu můžete provést kartou nebo převodem na účet.";
    } else if (message.toLowerCase().includes("vraceni") || message.toLowerCase().includes("vrátit")) {
        replyText = "Zboží můžete vrátit do 14 dnů bez udání důvodu.";
    } else {
        replyText = `Ahoj ${student}, tvůj dotaz ("${message}") jsme přijali na tvém vlastním backendu!`;
    }

    res.json({ reply: replyText });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});