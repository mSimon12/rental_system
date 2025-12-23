import { Component, OnInit, signal } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-item-details-page',
  imports: [RouterModule],
  templateUrl: './item-details-page.component.html',
  styleUrl: './item-details-page.component.css'
})
export class ItemDetailsPageComponent {

  itemId!: string;

  // Mock data for now (replace with API later)
  product = signal({
    name: 'Camera Canon EOS',
    description: 'High quality DSLR camera, perfect for travel and events.',
    available: 3,
    stock: 5,
    comments: [
      'Great camera!',
      'Worked perfectly for my trip'
    ]
  });

  rating = signal(0);

  constructor(private route: ActivatedRoute) {}

  ngOnInit() {
    this.itemId = this.route.snapshot.paramMap.get('id')!;
    // later: fetch product by id
  }

  setRating(value: number) {
    this.rating.set(value);
  }

  rentItem() {
    console.log('Rent item', this.itemId);
  }

  returnItem() {
    console.log('Return item', this.itemId);
  }
}
