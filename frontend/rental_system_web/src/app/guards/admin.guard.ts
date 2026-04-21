import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { map, take } from 'rxjs/operators';
import { UsersApiService} from '../services/users-api.service';

export const AdminGuard: CanActivateFn = () => {
  const usersApi:UsersApiService = inject(UsersApiService);
  const router:Router = inject(Router);

  return usersApi.currentUser$.pipe(
    take(1),
    map(user => {
      if (user.user_logged_in && user.is_admin) {
        return true;
      }

      router.navigate(['/login']);
      return false;
    })
  );
};
