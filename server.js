const express = require('express');
const axios = require('axios');
const app = express();
const cors = require('cors');
app.use(cors());

app.use(express.json());

// Define route for the frontend to send code to the backend server
app.post('/execute', async (req, res) => {
    const { language, code, testcases } = req.body;

    // Check if required fields are provided
    if (!language || !code || !testcases) {
        return res.status(400).json({ error: 'Please provide language, code, and testcases' });
    }

    try {
        // Send request to the router service
        const response = await axios.post('http://localhost:8080/run', { language, code, testcases });
        res.status(response.status).json(response.data);
    } catch (error) {
        res.status(500).json({
            error: 'Execution service is unavailable',
            details: error.message
        });
    }
});

const PORT = process.env.PORT || 4000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
