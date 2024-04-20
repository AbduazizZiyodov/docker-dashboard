import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { DashboardComponent } from './dashboard/dashboard.component';
import { ContainersComponent } from './containers/containers.component'
import { CreateContainersComponent } from './create-containers/create-containers.component';

const routes: Routes = [
  {
    path: '',
    component: DashboardComponent
  },
  {
    path: 'containers',
    component: ContainersComponent,
  },
  {
    path: 'containers/new',
    component: CreateContainersComponent,
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
