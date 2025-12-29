import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { StoreItem } from '../model/store-item';
import { ItemsApiService } from '../services/items-api.service';

@Component({
  selector: 'app-manager-page',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './manager-page.component.html',
  styleUrl: './manager-page.component.css'
})

export class ManagerPageComponent implements OnInit {
  addItemForm: FormGroup;

  storeItems$!: Observable<StoreItem[]>;
  totalItems$!: Observable<number>;
  rentedCount$!: Observable<number>;
  availableCount$!: Observable<number>;

  search = '';
  stockFilter: 'all' | 'high' | 'medium' | 'low' = 'all';

  constructor(private fb: FormBuilder,
              private itemsApi: ItemsApiService) {
    this.addItemForm = this.fb.group({
      name: ['', Validators.required],
      description: ['', Validators.required],
      stock: [0, [Validators.required, Validators.min(1)]]
    });
  }

  ngOnInit() {
    this.storeItems$ = this.itemsApi.getStoreItems();

    this.totalItems$ = this.storeItems$.pipe(
      map(items => items.length)
    );

    this.rentedCount$ = this.storeItems$.pipe(
      map(items =>
        items.reduce((sum, i) => sum + (i.stock - i.available), 0)
      )
    );

    this.availableCount$ = this.storeItems$.pipe(
      map(items =>
        items.reduce((sum, i) => sum + i.available, 0)
      )
    );

  }

  filteredItems$(items: StoreItem[]): StoreItem[] {
    return items.filter(item => {
      const textMatch =
        item.name.toLowerCase().includes(this.search.toLowerCase()) ||
        item.description.toLowerCase().includes(this.search.toLowerCase());

      if (!textMatch) return false;

      const ratio = item.available / item.stock;

      switch (this.stockFilter) {
        case 'high': return ratio > 0.6;
        case 'medium': return ratio > 0.3 && ratio <= 0.6;
        case 'low': return ratio <= 0.3;
        default: return true;
      }
    });
  }

  /* ---------- Form getters ---------- */

  get itemName() {
    return this.addItemForm.get('name');
  }

  get itemDescription() {
    return this.addItemForm.get('description');
  }

  get itemStock() {
    return this.addItemForm.get('stock');
  }

  /* ---------- Actions ---------- */

  stockLevel(item: StoreItem) {
    const ratio = item.available / item.stock;
    if (ratio > 0.6) return 'high';
    if (ratio > 0.3) return 'medium';
    return 'low';
  }

  editItem(item: StoreItem) {
    alert(`Edit item: ${item.name}`);
  }

  exportData() {
    alert('Exporting inventory data...');
  }

  generateReport() {
    alert('Generating monthly report...');
  }

  bulkUpdate() {
    alert('Bulk update items...');
  }

  addItem() {
    if (this.addItemForm.invalid) {
      this.addItemForm.markAllAsTouched();
      return;
    }

    const { name, description, stock } = this.addItemForm.value;

    this.itemsApi.addNewItemToStore(name, description, stock).subscribe({
      next: () => console.log('Item added successfully'),
      error: err => console.error('Failed to add item', err)
    });

    this.addItemForm.reset({ stock: 0 });
  }

  deleteItem(item: StoreItem) {
    this.itemsApi.deleteItemFromStore(item.name).subscribe({
      next: () => console.log('Item deleted successfully'),
      error: err => console.error('Failed to delete item', err)
    });
  }
}
