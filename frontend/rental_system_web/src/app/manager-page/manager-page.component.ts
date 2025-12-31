import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Observable, BehaviorSubject } from 'rxjs';
import { map, switchMap } from 'rxjs/operators';
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

  private refresh$ = new BehaviorSubject<void>(undefined);
  storeItems$!: Observable<StoreItem[]>;
  summary$!: Observable<{
    totalItems: number;
    rentedCount: number;
    availableCount: number;
  }>;

  search = '';
  stockFilter: 'all' | 'high' | 'medium' | 'low' = 'all';

  constructor(private fb: FormBuilder,
              private itemsApi: ItemsApiService) {
    this.addItemForm = this.fb.group({
      name: ['', Validators.required],
      description: [''],
      stock: [0, [Validators.required, Validators.min(1)]]
    });
  }

  ngOnInit() {
    this.storeItems$ = this.refresh$.pipe(
      switchMap(() => this.itemsApi.getStoreItems())
    );

    this.summary$ = this.storeItems$.pipe(
      map(items => {
        const totalItems = items.length;

        const rentedCount = items.reduce((sum, item) => {
          const stock = Number(item.stock ?? 0);
          const available = Number(item.available ?? 0);
          return sum + Math.max(stock - available, 0);
        }, 0);

        const availableCount = items.reduce((sum, item) => {
          const available = Number(item.available ?? 0);
          return sum + Math.max(available, 0);
        }, 0);

        return {
          totalItems,
          rentedCount,
          availableCount
        };
      })
    );
  }

  refreshStoreItems(): void {
    this.refresh$.next();
  }

  filteredItems$(items: StoreItem[]): StoreItem[] {
    return items.filter(item => {
      console.log(item)
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
      next: () => {
        this.refreshStoreItems();
        console.log('Item added successfully')
      },
      error: err => console.error('Failed to add item', err)
    });

    this.addItemForm.reset({ stock: 0 });
  }

  deleteItem(item: StoreItem) {
    this.itemsApi.deleteItemFromStore(item.name).subscribe({
      next: () => {
        this.refreshStoreItems();
        console.log('Item deleted successfully')
      },
      error: err => console.error('Failed to delete item', err)
    });
  }
}
