import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Router } from '@angular/router';
import {UsersApiService} from '../services/users-api.service';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './header.component.html',
  styleUrl: './header.component.css'
})
export class HeaderComponent implements OnInit {
  userInfo!: any;

  constructor(
    private usersApi: UsersApiService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.usersApi.currentUser$.subscribe(u => this.userInfo = u);
  }

  submitLogout() {
    this.usersApi.logoutUser().subscribe({
      next: () => {
        console.log('Logged out successfully');
        this.router.navigate(['/store']);
      },
      error: err => {
        console.error('Logout failed', err);
      }
    });
  }

}
