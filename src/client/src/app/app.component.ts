import * as AOS from 'aos';
import { Component, OnInit } from '@angular/core';
import { Location } from '@angular/common';

@Component({
  selector: 'app-root',
  template: `<app-menu></app-menu>`,
})
export class AppComponent implements OnInit {
  title = 'client';
  constructor(private location: Location) { }
  ngOnInit(): void {
    AOS.init();
  }
  back() {
    this.location.back();
  }
  next() {
    this.location.forward();
  }
}
