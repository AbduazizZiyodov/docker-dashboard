import { Component } from '@angular/core';
import { Location } from '@angular/common';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss'],
})
export class HeaderComponent {
  constructor(private location: Location) {}

  back() {
    this.location.back();
  }
  next() {
    this.location.forward();
  }
}
