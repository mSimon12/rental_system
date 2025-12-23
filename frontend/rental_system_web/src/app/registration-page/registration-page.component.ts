import { Component } from '@angular/core';
import {FormBuilder, FormGroup, Validators, AbstractControl, ReactiveFormsModule} from '@angular/forms';
import {CommonModule} from '@angular/common';
import {RouterModule} from '@angular/router';

@Component({
  selector: 'app-registration-page',
  imports: [CommonModule, ReactiveFormsModule, RouterModule],
  templateUrl: './registration-page.component.html',
  styleUrl: './registration-page.component.css'
})
export class RegistrationPageComponent {
  registerForm: FormGroup;

  constructor(private fb: FormBuilder) {
    this.registerForm = this.fb.group({
      username: ['', [Validators.required, Validators.minLength(3)]],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required]],
      password2: ['', [Validators.required]]
    }, { validators: this.passwordsMatch });
  }

  // ---- getters (avoid private access issues)
  get username() { return this.registerForm.get('username'); }
  get email() { return this.registerForm.get('email'); }
  get password() { return this.registerForm.get('password'); }
  get password2() { return this.registerForm.get('password2'); }

  // ---- submit
  submit() {
    if (this.registerForm.invalid) {
      this.registerForm.markAllAsTouched();
      return;
    }

    console.log(this.registerForm.value);
    // call API here
  }

  // ---- custom validator
  passwordsMatch(group: AbstractControl) {
    const p1 = group.get('password')?.value;
    const p2 = group.get('password2')?.value;
    return p1 === p2 ? null : { passwordsMismatch: true };
  }

  // ---- password strength
  passwordStrength() {
    const value = this.password?.value || '';
    if (!value) return null;

    let strength = 0;
    const rules = [
      value.length >= 8,
      /[A-Z]/.test(value),
      /[a-z]/.test(value),
      /\d/.test(value),
      /[!@#$%^&*()_,.?":{}|<>]/.test(value)
    ];

    strength = rules.filter(Boolean).length;

    if (strength < 3) return { text: 'Weak password', class: 'strength-weak' };
    if (strength < 5) return { text: 'Medium password', class: 'strength-medium' };
    return { text: 'Strong password ✓', class: 'strength-strong' };
  }


}
