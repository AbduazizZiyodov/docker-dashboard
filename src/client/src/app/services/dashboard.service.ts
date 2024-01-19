import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { DashboardInfo } from '@models/dashboard'
@Injectable({
  providedIn: 'root'
})
export class DashboardService {

  private api: string = 'http://127.0.0.1:2120/api';

  constructor(private http: HttpClient) { }


  getDashboardInfo() {
    return this.http.get<DashboardInfo>(`${this.api}/stats/dashboard`);
  }
}



