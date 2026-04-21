import { Component } from '@angular/core';
import { RouterOutlet, Router } from '@angular/router';
import {HeaderComponent} from './header/header.component';
import { FooterComponent} from './footer/footer.component';
import { UsersApiService } from './services/users-api.service';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, HeaderComponent, FooterComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'rental_system_web';

  constructor(
    private usersApi: UsersApiService,
    private router: Router
  ) {
    this.usersApi.currentUser$.subscribe(user => {
      if (!user.user_logged_in) {
        this.router.navigate(['/store']);
      }
    });
  }
}
