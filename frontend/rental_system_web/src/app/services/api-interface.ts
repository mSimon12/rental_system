import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from '../../environments/environment';

export abstract class APIInterface {
  // Same-origin API via Nginx reverse proxy
  protected apiEndpoint = environment.apiUrl;
  protected headers: HttpHeaders | null = null;

  protected constructor(protected http: HttpClient) {}

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
