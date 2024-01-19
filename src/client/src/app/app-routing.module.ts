import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { ContainersComponent } from './containers/containers.component'
import { DashboardComponent } from './dashboard/dashboard.component';

const routes: Routes = [
  {
    path: '',
    component: DashboardComponent
  },
  {
    path: 'containers',
    component: ContainersComponent
  }];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
