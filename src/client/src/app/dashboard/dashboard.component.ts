import { Component, OnInit } from '@angular/core';

import { DashboardService } from '@services/dashboard.service'
import { DashboardInfo } from '@models/dashboard'

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.scss'
})
export class DashboardComponent implements OnInit {
  dashboardInfo!: DashboardInfo;

  constructor(private dashboardService: DashboardService) { }

  ngOnInit(): void {
    this.dashboardService.getDashboardInfo().subscribe((data: DashboardInfo) => {
      this.dashboardInfo = data;
    })
  }
}
