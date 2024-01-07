import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { ContainersComponent } from '@containers/containers.component'

const routes: Routes = [{
  path: 'containers',
  component: ContainersComponent
}];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
