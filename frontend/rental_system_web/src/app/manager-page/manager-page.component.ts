import { Component, computed, signal} from '@angular/core';
import { CommonModule } from '@angular/common';
import { StoreItem } from '../model/store-item';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-manager-page',
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './manager-page.component.html',
  styleUrl: './manager-page.component.css'
})
export class ManagerPageComponent {
  addItemForm: FormGroup;

  constructor(private fb: FormBuilder) {
    this.addItemForm = this.fb.group({
      name: ['', Validators.required],
      description: ['', Validators.required],
      stock: [0, [Validators.required, Validators.min(1)]]
    });
  }

  get itemName() {
    return this.addItemForm.get('name');
  }

  get itemDescription() {
    return this.addItemForm.get('description');
  }

  get itemStock() {
    return this.addItemForm.get('stock');
  }


  search = signal('');
  stockFilter = signal<'all' | 'high' | 'medium' | 'low'>('all');

  items = signal<StoreItem[]>([
    {
      id: 0,
      name: 'Camera',
      description: 'DSLR camera',
      stock: 10,
      available: 7
    },
    {
      id: 1,
      name: 'Tripod',
      description: 'Professional tripod',
      stock: 5,
      available: 2
    },
    {
      id: 2,
      name: 'Microphone',
      description: 'Studio microphone',
      stock: 4,
      available: 1
    }
  ]);

  totalItems = computed(() => this.items().length);
  rentedCount = computed(
    () => this.items().reduce((s, i) => s + (i.stock - i.available), 0)
  );
  availableCount = computed(
    () => this.items().reduce((s, i) => s + i.available, 0)
  );

  filteredItems = computed(() => {
    return this.items().filter(item => {
      const textMatch =
        item.name.toLowerCase().includes(this.search()) ||
        item.description.toLowerCase().includes(this.search());

      if (!textMatch) return false;

      const ratio = item.available / item.stock;

      switch (this.stockFilter()) {
        case 'high':
          return ratio > 0.6;
        case 'medium':
          return ratio > 0.3 && ratio <= 0.6;
        case 'low':
          return ratio <= 0.3;
        default:
          return true;
      }
    });
  });

  stockLevel(item: StoreItem) {
    const ratio = item.available / item.stock;
    if (ratio > 0.6) return 'high';
    if (ratio > 0.3) return 'medium';
    return 'low';
  }

  editItem(item: StoreItem) {
    alert(`Edit item: ${item.name}`);
  }

  deleteItem(item: StoreItem) {
    this.items.set(this.items().filter(i => i.id !== item.id));
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

    const {name, description, stock} = this.addItemForm.value;

    console.log(name, description, stock);

    this.addItemForm.reset({stock: 0});
  }
}
