import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { MenuComponent } from './core/menu/menu.component';
import { ContainersComponent } from './core/containers/containers.component';

const routes: Routes = [
  { path: '', component: MenuComponent },
  { path: 'containers', component: ContainersComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
