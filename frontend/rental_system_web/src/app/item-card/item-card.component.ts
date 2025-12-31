import { Component, Input } from '@angular/core';
import { RouterModule } from '@angular/router';
import { StoreItem } from '../model/store-item';

@Component({
  selector: 'app-item-card',
  imports: [RouterModule],
  templateUrl: './item-card.component.html',
  styleUrl: './item-card.component.css'
})
export class ItemCardComponent {
  @Input({ required: true })
  item!: StoreItem;

  constructor() {
  }
}
