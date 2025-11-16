import { Request, Response } from "express";
import { CreatePaymentDTO } from "../dtos/create-payment.dto";
import axios from 'axios';
import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();

const LNBITS_API_URL = process.env.LNBITS_API_URL || 'https://demo.lnbits.com';

const paymentsController = {
    pay: async (req: Request<{}, {}, CreatePaymentDTO>, res: Response) => {
        const {cardUID, merchantWalletId, amount} = req.body;

        try {
            // obtener invoice key de la wallet del comercio para generar factura

            const merchantWallet = await prisma.wallet.findFirst({
                where: {
                    id: merchantWalletId
                },
                select: {
                    invoiceKey: true
                }
            });

            if (!merchantWallet) {
                return res.status(404).json({
                    message: 'wallet del comercio no encontrada'
                });
            }

            // generar factura usando la invoice key:

            const invoiceResponse = await axios.post(
                `${LNBITS_API_URL}/api/v1/payments`,
                {
                    out: false,
                    amount,
                    memo: 'Test payment'
                }, 
                {
                    headers: {
                        'X-Api-Key': merchantWallet.invoiceKey,
                        'Content-Type': 'application/json'
                    }
                }
            );

            const invoice = invoiceResponse.data; // seria bueno usar un dto para validar lo que devuelve lnbits

            // obtener la clave de admin de la wallet del cliente para pagar

            const clientWallet = await prisma.wallet.findFirst({
                where: {
                    cards: {
                        some: {
                            uid: cardUID
                        }
                    }
                },
                select: {
                    adminKey: true
                }
            });

            if (!clientWallet) {
                return res.status(404).json({
                    message: "wallet del cliente no encontrada"
                })
            };

            // generar pago

            const paymentResponse = await axios.post(
                `${LNBITS_API_URL}/api/v1/payments`,
                {
                    out: true,
                    bolt11: invoice.bolt11 // aqui seria bueno que invoice fuera una instancia de un dto
                }, 
                {
                    headers: {
                        'X-Api-Key': clientWallet.adminKey,
                        'Content-Type': 'application/json'
                    }
                }
            );

            const payment = paymentResponse.data;

            res.status(200).json({message: 'pago exitoso', payment});

        } catch (error) {
            console.error(error)
            res.status(500).json({message: 'Internal server error'});
        }

    }
}

export default paymentsController;