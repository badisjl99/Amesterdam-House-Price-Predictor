const express = require('express');
const axios = require('axios');
const bodyParser = require('body-parser');
const cors = require('cors'); // Import the cors middleware

const app = express();
const port = 3000;

// Use cors middleware
app.use(cors());

// Parse incoming JSON requests
app.use(bodyParser.json());

// Your existing /predict route
app.post('/predict', (req, res) => {
    const data = {
        zip: req.body.zip,
        area: req.body.area,
        room: req.body.room
    };

    // Send a POST request to your Python Flask API
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

// Serve your HTML file or render a template
app.get('/', (req, res) => {
    res.sendFile(__dirname + '/index.html');
});

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
