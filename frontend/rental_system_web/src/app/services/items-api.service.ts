import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { APIInterface} from './api-interface';
import { forkJoin, Observable, of } from 'rxjs';
import { switchMap, map } from 'rxjs/operators';

@Injectable({providedIn: 'root'})
export class ItemsApiService extends APIInterface{

  constructor(http: HttpClient) {
    super(http);
  }

  /* =====================
   * ItemsInterface
   * ===================== */

  getItemInfo(itemId: string): Observable<any> {
    return this.http.get(`${this.apiEndpoint}/items/${itemId}`);
  }

  getItemsIdMap(): Observable<any> {
    return this.http.get(`${this.apiEndpoint}/items/`);
  }

  getStoreItems(): Observable<any> {
    return this.getItemsIdMap().pipe(
      switchMap(items => {
        if (!items || items.length === 0) {
          return of([]);
        }

        const requests = items.map((item: { id: string; }) =>
          this.getItemInfo(item.id)
        );

        return forkJoin(requests);
      })
    );
  }

  addNewItemToStore(newItem: any): Observable<any> {
    return this.http.post(
      `${this.apiEndpoint}/items`,
      newItem,
      this.getAuthOptions()
    );
  }

  deleteItemFromStore(itemName: string): Observable<any> {
    return this.http.delete(
      `${this.apiEndpoint}/items/`,
      {
        ...this.getAuthOptions(),
        body: { item: itemName }
      }
    );
  }

  rentItem(itemId: string, clientId: string): Observable<any> {
    return this.http.put(
      `${this.apiEndpoint}/items/${itemId}/rent`,
      { user_id: clientId },
      this.getAuthOptions()
    );
  }

  returnItem(itemId: string, clientId: string): Observable<any> {
    return this.http.put(
      `${this.apiEndpoint}/items/${itemId}/return`,
      { user_id: clientId },
      this.getAuthOptions()
    );
  }
}
