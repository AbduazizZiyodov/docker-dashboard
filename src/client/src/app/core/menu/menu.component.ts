import { Component } from '@angular/core';
import { Location } from '@angular/common';
import { Router } from '@angular/router';

@Component({
  selector: 'app-menu',
  templateUrl: './menu.component.html',
  styleUrls: ['./menu.component.scss'],
})
export class MenuComponent {
  hideSize: string = '30px';
  showSize: string = '250px';
  isHidden: boolean = false;

  constructor(private location: Location, private router: Router) {}

  back() {
    this.location.back();
  }
  next() {
    this.location.forward();
  }

  hideOrShow(sidebar: HTMLDivElement, content: HTMLDivElement): void {
    sidebar.style.width = content.style.marginLeft = this.isHidden
      ? this.showSize
      : this.hideSize;

    this.isHidden = !this.isHidden;
  }
}
