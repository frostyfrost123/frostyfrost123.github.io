import express, { Request, Response } from 'express';
import cors from 'cors';

const app = express();
app.use(express.json());

app.use(cors({ origin: '*', allowedHeaders: '*' }));

interface DepositPostbackRequest {
    userId: string;
    amount: number;
    currencyCode: string;
    transactionId: string;
}

app.post('/v1/wallet/deposit-postback', (req: Request, res: Response) => {
    const apiKey = req.header('X-API-KEY');
    const { userId, amount, transactionId }: DepositPostbackRequest = req.body;

    if (!apiKey || apiKey !== 'secretValue') {
        return res.status(401).send('Unauthorized');
    }

    if (amount === undefined || amount === null || amount <= 0) {
        return res.status(400).send('Amount must be positive');
    }
    const newTokens = Math.ceil(amount * 2.5);
    increaseUserBalance(userId, newTokens);
    return res.status(200).send('OK');
});

app.listen(8080, () => console.log('Server running on port 8080'));
