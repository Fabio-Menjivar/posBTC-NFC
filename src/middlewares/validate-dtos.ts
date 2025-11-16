import { plainToInstance } from "class-transformer";
import { validate } from "class-validator";
import { Request, Response, NextFunction } from "express";

export function validateDTO(dtoClass: any) {
  return async (req: Request, res: Response, next: NextFunction) => {
    const dto = plainToInstance(dtoClass, req.body);
    const errors = await validate(dto, {whitelist: true, forbidNonWhitelisted: true});

    if (errors.length > 0) {
      return res.status(400).json({
        message: "Validation failed",
        errors: errors.map(err => ({
          property: err.property,
          constraints: err.constraints
        }))
      });
    }

    next();
  };
}
