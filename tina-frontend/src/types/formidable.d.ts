declare module 'formidable' {
  export class IncomingForm {
    parse(
      req: any,
      callback: (
        err: Error | null,
        fields: { [key: string]: string[] },
        files: { [key: string]: { 
          filepath: string;
          originalFilename?: string;
          mimetype?: string;
          size: number;
        }[] }
      ) => void
    ): void;
  }
}
