import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { APIInterface } from './api-interface';
import { Observable, BehaviorSubject, of  } from 'rxjs';
import { tap, map, catchError } from 'rxjs/operators';
import { jwtDecode } from 'jwt-decode';
import { CookieService } from 'ngx-cookie-service';
import { ItemsApiService } from '../services/items-api.service';

interface JwtPayload {
  sub: string;
}

@Injectable({ providedIn: 'root' })
export class UsersApiService extends APIInterface {

  private currentUserSubject = new BehaviorSubject<{
    user_logged_in: boolean;
    username: string | null;
    is_admin: boolean;
  }>({
    user_logged_in: false,
    username: null,
    is_admin: false
  });

// Expose it as an observable for components
  currentUser$ = this.currentUserSubject.asObservable();

  constructor(
    http: HttpClient,
    private itemsApi: ItemsApiService,
    private cookieService: CookieService
  ) {
    super(http);
  }

  getUsersList(): Observable<any> {
    return this.http.get(
      `${this.apiEndpoint}/users`,
      this.getAuthOptions()
    );
  }

  getUserById(userId: string): Observable<any> {
    return this.http.get(`${this.apiEndpoint}/users/${userId}`, this.getAuthOptions());
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

  loginUser(username: string, password: string): Observable<boolean> {
    return this.http.post<any>(`${this.apiEndpoint}/users/login`, { username, password }).pipe(
      tap(data => {
        const token = data.access_token;
        const expires = new Date();
        expires.setMinutes(expires.getMinutes() + 10);

        this.cookieService.set('access_token_cookie', token, {
          path: '/',
          expires,
          secure: true,
          sameSite: 'Strict'
        });

        this.setToken(token);
        this.itemsApi.setToken(token);

        // Update the BehaviorSubject
        this.updateCurrentUserInfo().subscribe(userInfo => {
          this.currentUserSubject.next(userInfo);
        });

      }),
      map(() => true)
    );
  }

  logoutUser(): Observable<any> {
    return this.http.post(`${this.apiEndpoint}/users/logout`, {}, this.getAuthOptions()).pipe(
      tap(() => {
        this.cookieService.delete('access_token_cookie', '/');

        // Update the BehaviorSubject
        this.currentUserSubject.next({
          user_logged_in: false,
          username: null,
          is_admin: false
        });


        this.clearToken()
        this.itemsApi.clearToken();

      })
    );
  }

  private updateCurrentUserInfo() {
    const token = this.cookieService.get('access_token_cookie');
    if (!token) {
      return of({
        user_logged_in: false,
        username: null,
        is_admin: false
      });
    }

    try {
      // Decode JWT
      const decoded: JwtPayload = jwtDecode(token);
      const userId = decoded.sub;

      // Fetch user from backend
      return this.getUserById(userId).pipe(
        map(user => ({
          user_logged_in: true,
          username: user.username,
          is_admin: user.role === 'Admin'
        })),
        catchError(() =>
          of({
            user_logged_in: false,
            username: null,
            is_admin: false
          })
        )
      );

    } catch (err) {
      console.error('Invalid token', err);
      return of({
        user_logged_in: false,
        username: null,
        is_admin: false
      });
    }
  }

}
