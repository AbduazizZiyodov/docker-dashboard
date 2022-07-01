import { Component, OnInit } from '@angular/core';
import { Location } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { environment } from '@env';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss'],
})
export class HeaderComponent implements OnInit {
  isRunning: boolean = false;

  constructor(private location: Location, private http: HttpClient) {}

  back() {
    this.location.back();
  }
  next() {
    this.location.forward();
  }
  ngOnInit(): void {
    this.testAPI();
  }

  testAPI() {
    this.http
      .get(environment.apiUrl.replace('api', ''))
      .subscribe((res: any) => {
        if (res == 'ok') {
          this.isRunning = true;
        }
      });
  }
}
