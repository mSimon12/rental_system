import { HttpClient, HttpHeaders } from '@angular/common/http';

export abstract class APIInterface {
  protected readonly DEFAULT_API_URL = 'http://localhost:5001/api';
  protected apiEndpoint: string;
  protected headers: HttpHeaders | null = null;

  protected constructor(protected http: HttpClient) {
    this.apiEndpoint = (window as any).__env?.API_URL || this.DEFAULT_API_URL;
  }

  setToken(token: string | null): void {
    if (token) {
      this.headers = new HttpHeaders({
        Authorization: `Bearer ${token}`
      });
    }
  }

  clearToken(): void {
    this.headers = null;
  }

  protected getAuthOptions() {
    return this.headers ? { headers: this.headers } : {};
  }
}
