import { Component } from '@angular/core';
import { Location } from '@angular/common';
import { Router } from '@angular/router';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss'],
})
export class HeaderComponent {
  constructor(private location: Location, private router: Router) {}

  back() {
    this.location.back();
  }
  next() {
    this.location.forward();
  }
}
