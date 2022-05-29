import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { MenuComponent } from './core/menu/menu.component';
import { ContainersComponent } from './core/containers/containers.component';
import { ImagesComponent } from './core/images/images.component';
import { NotFoundComponent } from './components/not-found/not-found.component';

const routes: Routes = [
  { path: '', component: MenuComponent },
  { path: 'containers', component: ContainersComponent },
  { path: 'images', component: ImagesComponent },
  { path: '**', component: NotFoundComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
