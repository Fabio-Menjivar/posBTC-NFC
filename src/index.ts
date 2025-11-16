import express, {Request, Response} from 'express';

import 'dotenv/config';

const app = express();
const port = process.env.SERVER_PORT || 3000;

app.use(express.json());

import paymentRoutes from './routes/payments.routes';

app.get('/', (req: Request, res: Response) => {
    res.send("server working");
});

app.use(paymentRoutes);

app.listen(port, () => {
    console.log(`server running on port ${port}`);
});