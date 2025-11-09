import express, {Request, Response} from 'express';

import dotenv from 'dotenv';
dotenv.config();

const app = express();
const port = process.env.SERVER_PORT || 3000;

app.get('/', (req: Request, res: Response) => {
    res.send("server working");
});

app.listen(port, () => {
    console.log('server running on port 3000');
});