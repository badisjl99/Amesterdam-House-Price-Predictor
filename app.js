const express = require('express');
const axios = require('axios');
const bodyParser = require('body-parser');
const cors = require('cors'); 

const app = express();
const port = 3000;

app.use(cors());


app.use(bodyParser.json());


app.post('/predict', (req, res) => {
    const data = {
        zip: req.body.zip,
        area: req.body.area,
        room: req.body.room
    };

    
    axios.post('http://localhost:5000/predict', data)
        .then(response => {
            // Send the predicted price as a response to the client
            res.json({ predicted_price: response.data.predicted_price });
        })
        .catch(error => {
            console.error('error', error.message);
            res.status(500).json({ error: 'Internal Server Error' });
        });
});


app.get('/', (req, res) => {
    res.sendFile(__dirname + '/index.html');
});

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
