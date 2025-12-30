import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { APIInterface } from './api-interface';
import { forkJoin, Observable, of } from 'rxjs';
import { switchMap, map } from 'rxjs/operators';
import { StoreItem } from '../model/store-item';

@Injectable({ providedIn: 'root' })
export class ItemsApiService extends APIInterface {

  constructor(http: HttpClient) {
    super(http);
  }

  /* =====================
   * ItemsInterface
   * ===================== */

  getItemInfo(itemId: string): Observable<StoreItem> {
    return this.http.get<any>(`${this.apiEndpoint}/items/${itemId}`).pipe(
      map(item => ({
        id: Number(item.id),
        name: item.name,
        description: item.description ?? '',
        stock: Number(item.stock_size ?? 0),   // ✅ normalize here
        available: Number(item.available ?? 0)
      }))
    );
  }

  getItemsIdMap(): Observable<{ id: string }[]> {
    return this.http.get<{ id: string }[]>(`${this.apiEndpoint}/items/`);
  }

  getStoreItems(): Observable<StoreItem[]> {
    return this.getItemsIdMap().pipe(
      switchMap(items => {
        if (!items || items.length === 0) {
          return of([]);
        }

        const requests = items.map(item =>
          this.getItemInfo(item.id)
        );

        return forkJoin(requests);
      })
    );
  }

  addNewItemToStore(
    name: string,
    description: string,
    stock: number
  ): Observable<void> {
    return this.http.post<void>(
      `${this.apiEndpoint}/items/`,
      { name, description, stock },
      this.getAuthOptions()
    );
  }

  deleteItemFromStore(itemName: string): Observable<void> {
    return this.http.delete<void>(
      `${this.apiEndpoint}/items/`,
      {
        ...this.getAuthOptions(),
        body: { name: itemName }
      }
    );
  }

  rentItem(itemId: string, clientId: string): Observable<void> {
    return this.http.put<void>(
      `${this.apiEndpoint}/items/${itemId}/rent`,
      { user_id: clientId },
      this.getAuthOptions()
    );
  }

  returnItem(itemId: string, clientId: string): Observable<void> {
    return this.http.put<void>(
      `${this.apiEndpoint}/items/${itemId}/return`,
      { user_id: clientId },
      this.getAuthOptions()
    );
  }
}
