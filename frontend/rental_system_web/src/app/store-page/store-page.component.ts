import { Component } from '@angular/core';
import {ItemCardComponent} from '../item-card/item-card.component';
import { StoreItem } from '../model/store-item';

@Component({
  selector: 'app-store-page',
  imports: [
    ItemCardComponent
  ],
  templateUrl: './store-page.component.html',
  styleUrl: './store-page.component.css'
})
export class StorePageComponent {
  storeItems: StoreItem[] = [
    { id: 1, name: 'Camera', description: 'DSLR Camera', available: 3, stock: 5 },
    { id: 2, name: 'Drill', description: 'Electric drill', available: 5, stock: 5 },
  ];

}
