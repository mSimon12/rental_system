import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { APIInterface} from './api-interface';
import { Observable } from 'rxjs';

@Injectable({providedIn: 'root'})
export class UsersApiService extends APIInterface{

  constructor(http: HttpClient) {
    super(http);
  }

  /* =====================
   * UserInterface
   * ===================== */

  getUsersList(): Observable<any> {
    return this.http.get(
      `${this.apiEndpoint}/users`,
      this.getAuthOptions()
    );
  }

  getUserById(userId: string): Observable<any> {
    return this.http.get(
      `${this.apiEndpoint}/users/${userId}`,
      this.getAuthOptions()
    );
  }

  addUser(username: string, email: string, password: string): Observable<any> {
    return this.http.post(
      `${this.apiEndpoint}/users`,
      { username, email, password }
    );
  }

  deleteUser(userInfo: any): Observable<any> {
    return this.http.post(
      `${this.apiEndpoint}/users`,
      userInfo,
      this.getAuthOptions()
    );
  }

  loginUser(username: string, password: string): Observable<any> {
    return this.http.post(
      `${this.apiEndpoint}/users/login`,
      { username, password }
    );
  }

  logoutUser(userId: string): Observable<any> {
    return this.http.post(
      `${this.apiEndpoint}/users/${userId}/logout`,
      {},
      this.getAuthOptions()
    );
  }
}
