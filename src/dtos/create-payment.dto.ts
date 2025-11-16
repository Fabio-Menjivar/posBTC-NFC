import { IsInt, IsString } from "class-validator";

export class CreatePaymentDTO {
    @IsString()
    cardUID!: string;

    @IsInt()
    merchantWalletId!: number;

    @IsInt()
    amount!: number;
}