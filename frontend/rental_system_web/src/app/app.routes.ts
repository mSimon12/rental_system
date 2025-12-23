import { Routes } from '@angular/router';
import { StorePageComponent } from './store-page/store-page.component'
import { ManagerPageComponent} from './manager-page/manager-page.component';

export const routes: Routes = [
  { path: '', redirectTo: 'store', pathMatch: 'full' },
  { path: 'store', component: StorePageComponent },
  { path: 'manager', component: ManagerPageComponent },
  { path: '**', redirectTo: 'index' }
];
