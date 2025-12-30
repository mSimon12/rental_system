import { Routes } from '@angular/router';
import { StorePageComponent } from './store-page/store-page.component'
import { LoginPageComponent} from './login-page/login-page.component';
import { RegistrationPageComponent } from './registration-page/registration-page.component';
import {ItemDetailsPageComponent} from './item-details-page/item-details-page.component';
import { ManagerPageComponent} from './manager-page/manager-page.component';
import { AdminGuard } from './guards/admin.guard';

export const routes: Routes = [
  { path: '', redirectTo: 'store', pathMatch: 'full' },
  { path: 'login', component: LoginPageComponent },
  { path: 'register', component: RegistrationPageComponent },
  { path: 'store', component: StorePageComponent },
  { path: 'store/:id', component: ItemDetailsPageComponent },
  {
    path: 'manager',
    component: ManagerPageComponent,
    canActivate: [AdminGuard]
  },
  { path: '**', redirectTo: 'index' }
];
