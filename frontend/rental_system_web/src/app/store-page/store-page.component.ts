import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import {Observable} from 'rxjs';
import { map } from 'rxjs/operators';
import {ItemCardComponent} from '../item-card/item-card.component';
import { StoreItem } from '../model/store-item';
import {ItemsApiService} from '../services/items-api.service';

@Component({
  selector: 'app-store-page',
  standalone: true,
  imports: [ CommonModule, ItemCardComponent ],
  templateUrl: './store-page.component.html',
  styleUrl: './store-page.component.css'
})

export class StorePageComponent implements OnInit {
  storeItems: StoreItem[] = [
    { id: 1, name: 'Camera', description: 'DSLR Camera', available: 3, stock: 5 },
    { id: 2, name: 'Drill', description: 'Electric drill', available: 5, stock: 5 },
  ];

  someData$: Observable<any> | undefined;

  constructor(private itemsApi: ItemsApiService) {
    console.log("Creating data api service");
  }

  ngOnInit() {
    this.someData$ = this.itemsApi.getStoreItems();
  }

  logItem(item:StoreItem): void{
    console.log(item);
  }

}
