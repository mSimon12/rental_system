import { Component, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { RouterModule } from '@angular/router';
import {BehaviorSubject, Observable} from 'rxjs';
import {ItemsApiService} from '../services/items-api.service';
import { UsersApiService } from '../services/users-api.service';
import {switchMap} from 'rxjs/operators';

@Component({
  selector: 'app-item-details-page',
  imports: [CommonModule, RouterModule],
  templateUrl: './item-details-page.component.html',
  styleUrl: './item-details-page.component.css'
})
export class ItemDetailsPageComponent implements OnInit {
  private refresh$ = new BehaviorSubject<void>(undefined);
  itemId!: string;
  itemInfo: Observable<any> | undefined;
  userInfo!: any;

  comments= [
    'Great camera!',
    'Worked perfectly for my trip'
  ]
  rating = signal(0);

  constructor(private route: ActivatedRoute,
              private router: Router,
              private itemsApi: ItemsApiService,
              private usersApi: UsersApiService) {}

  ngOnInit() {
    this.itemId = this.route.snapshot.paramMap.get('id')!;
    this.usersApi.currentUser$.subscribe(u => this.userInfo = u);

    this.itemInfo = this.refresh$.pipe(
      switchMap(() => this.itemsApi.getItemInfo(this.itemId))
    );

  }

  refreshStoreItems(): void {
    this.refresh$.next();
  }

  setRating(value: number) {
    this.rating.set(value);
  }


  rentItem() {
    if (!this.userInfo.user_logged_in) {
        this.router.navigate(['/login'], {
          queryParams: { redirect: `/store/${this.itemId}` }
        });
        return;
    }

    this.itemsApi.rentItem(this.itemId, this.userInfo.userId).subscribe({
      next: () => {
        this.refreshStoreItems();
        console.log('Item rented successfully')
      },
      error: err => console.error('Failed to add item', err)
    });

    console.log('Rent item', this.itemId);
  }

  returnItem() {
    if (!this.userInfo.user_logged_in) {
      this.router.navigate(['/login'], {
        queryParams: { redirect: `/store/${this.itemId}` }
      });
      return;
    }

    this.itemsApi.returnItem(this.itemId, this.userInfo.userId).subscribe({
      next: () => {
        this.refreshStoreItems();
        console.log('Item returned successfully')
      },
      error: err => console.error('Failed to add item', err)
    });
  }
}
