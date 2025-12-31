import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, Validators, FormGroup } from '@angular/forms';
import { ActivatedRoute, RouterModule, Router } from '@angular/router';
import {UsersApiService} from '../services/users-api.service';

@Component({
  selector: 'app-login-page',
  imports: [CommonModule, ReactiveFormsModule, RouterModule],
  templateUrl: './login-page.component.html',
  styleUrl: './login-page.component.css'
})
export class LoginPageComponent {
  loginForm : FormGroup;

  constructor(private fb: FormBuilder,
              private router: Router,
              private route: ActivatedRoute,
              private usersApi: UsersApiService) {
    this.loginForm = this.fb.nonNullable.group({
      username: ['', Validators.required],
      password: ['', Validators.required]
    });
  }

  get username() { return this.loginForm.get('username'); }
  get password() { return this.loginForm.get('password'); }

  submitLogin() {
    if (this.loginForm.invalid) {
      this.loginForm.markAllAsTouched();
      return;
    }

    const { username, password } = this.loginForm.getRawValue();

    // read redirect from query params
    const redirectUrl = this.route.snapshot.queryParamMap.get('redirect');

    this.usersApi.loginUser(username, password).subscribe({
      next: () => {
        console.log('Login success');

        if (redirectUrl) {
          // redirect to original requested page
          this.router.navigateByUrl(redirectUrl);
        } else {
          // default fallback
          this.router.navigateByUrl('/store');
        }
      },
      error: err => console.error('Login failed', err)
    });
  }
}
