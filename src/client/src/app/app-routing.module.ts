import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { MenuComponent } from '@core/menu/menu.component';
import { repositoryUrlMatcher } from '@core/url_matcher';
import { LogsComponent } from '@components/logs/logs.component';
import { AboutComponent } from '@components/about/about.component';
import { PullMenuComponent } from '@image/pull-menu/pull-menu.component';
import { PullListComponent } from '@image/pull-list/pull-list.component';
import { PullImageComponent } from '@image/pull-image/pull-image.component';
import { ImageListComponent } from '@image/image-list/image-list.component';
import { NotFoundComponent } from '@components/not-found/not-found.component';
import { ImageDetailedComponent } from '@image/image-detailed/image-detailed.component';
import { ContainerListComponent } from '@containers/container-list/container-list.component';

const routes: Routes = [
  { path: '', component: MenuComponent },
  { path: 'about', component: AboutComponent },
  { path: 'logs/:id', component: LogsComponent },
  { path: 'images', component: ImageListComponent },
  { path: 'pull-list', component: PullListComponent },
  { path: 'pull-images', component: PullMenuComponent },
  { path: 'images/:id', component: ImageDetailedComponent },
  { path: 'containers', component: ContainerListComponent },
  { matcher: repositoryUrlMatcher, component: PullImageComponent },

  { path: '**', component: NotFoundComponent },
  
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
