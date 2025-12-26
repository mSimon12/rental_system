import { TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { provideHttpClientTesting } from '@angular/common/http/testing';

import { ItemsApiService } from './items-api.service';

describe('ItemsApiService', () => {
  let service: ItemsApiService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        provideHttpClient(),
        provideHttpClientTesting()
      ]
    });

    service = TestBed.inject(ItemsApiService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
