import express, {Router} from 'express';

import paymentsController from '../controllers/payments.controller';
import { validateDTO } from '../middlewares/validate-dtos';
import { CreatePaymentDTO } from '../dtos/create-payment.dto';

const router: Router = express.Router();

router.post('/payments', validateDTO(CreatePaymentDTO), paymentsController.pay);

export default router;