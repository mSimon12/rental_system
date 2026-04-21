import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ItemDetailsPageComponent } from './item-details-page.component';

describe('ItemDetailsPageComponent', () => {
  let component: ItemDetailsPageComponent;
  let fixture: ComponentFixture<ItemDetailsPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ItemDetailsPageComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ItemDetailsPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
