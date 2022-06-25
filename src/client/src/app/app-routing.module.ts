import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { MenuComponent } from '@core/menu/menu.component';
import { ContainersComponent } from '@core/containers/containers.component';
import { ImagesComponent } from '@core/images/images.component';
import { NotFoundComponent } from '@components/not-found/not-found.component';
import { PullImagesComponent } from '@core/pull-images/pull-images.component';
import { ImageComponent } from '@core/image/image.component';
import { LogsComponent } from '@components/logs/logs.component';
import { AboutComponent } from '@components/about/about.component';

const routes: Routes = [
  { path: '', component: MenuComponent },
  { path: 'containers', component: ContainersComponent },
  { path: 'images', component: ImagesComponent },
  { path: 'images/:id', component: ImageComponent },
  { path: 'pull-images', component: PullImagesComponent },
  { path: 'logs/:id', component: LogsComponent },
  { path: 'about', component: AboutComponent },
  { path: '**', component: NotFoundComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
