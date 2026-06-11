const express = require('express');
const app = express();
const port = process.env.PORT || 3000;

app.use(express.urlencoded({ extended: true }));

let sonKonum = "Veri bekleniyor...";

app.post('/update', (req, res) => {
    const { lat, lon } = req.body;
    sonKonum = `${lat},${lon}`;
    console.log("Yeni konum alındı:", sonKonum);
    res.send("OK");
});

app.get('/get-konum', (req, res) => {
    res.send(sonKonum);
});

app.listen(port, () => console.log(`Sunucu ${port} portunda çalışıyor`));

