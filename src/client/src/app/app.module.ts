import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';
import { HttpClientModule } from '@angular/common/http';
import { HTTP_INTERCEPTORS } from '@angular/common/http';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { AppComponent } from './app.component';
import { AppRoutingModule } from './app-routing.module';

import { MdbTabsModule } from 'mdb-angular-ui-kit/tabs';
import { MdbFormsModule } from 'mdb-angular-ui-kit/forms';
import { MdbModalModule } from 'mdb-angular-ui-kit/modal';
import { MdbRadioModule } from 'mdb-angular-ui-kit/radio';
import { MdbRangeModule } from 'mdb-angular-ui-kit/range';
import { MdbRippleModule } from 'mdb-angular-ui-kit/ripple';
import { MdbTooltipModule } from 'mdb-angular-ui-kit/tooltip';
import { MdbPopoverModule } from 'mdb-angular-ui-kit/popover';
import { MdbCarouselModule } from 'mdb-angular-ui-kit/carousel';
import { MdbCheckboxModule } from 'mdb-angular-ui-kit/checkbox';
import { MdbCollapseModule } from 'mdb-angular-ui-kit/collapse';
import { MdbDropdownModule } from 'mdb-angular-ui-kit/dropdown';
import { MdbScrollspyModule } from 'mdb-angular-ui-kit/scrollspy';
import { MdbAccordionModule } from 'mdb-angular-ui-kit/accordion';
import { MdbValidationModule } from 'mdb-angular-ui-kit/validation';

import { ToastrModule } from 'ngx-toastr';
import { ClipboardModule } from 'ngx-clipboard';
import { NgSelectModule } from '@ng-select/ng-select';

import { HttpInterceptorService } from '@services/http-interceptor.service';

import { MenuComponent } from '@core/menu/menu.component';
import { LogsComponent } from '@components/logs/logs.component';
import { AboutComponent } from '@components/about/about.component';
import { ModalComponent } from '@components/modal/modal.component';
import { FooterComponent } from '@components/footer/footer.component';
import { HeaderComponent } from '@components/header/header.component';
import { PullMenuComponent } from '@image/pull-menu/pull-menu.component';
import { PullImageComponent } from '@image/pull-image/pull-image.component';
import { ImageListComponent } from '@image/image-list/image-list.component';
import { NotFoundComponent } from '@components/not-found/not-found.component';
import { PullListComponent } from './core/image/pull-list/pull-list.component';
import { ConfirmModalComponent } from '@modals/confirm-modal/confirm-modal.component';
import { ImageDetailedComponent } from '@image/image-detailed/image-detailed.component';
import { ContainerListComponent } from '@containers/container-list/container-list.component';
import { ContainersModalComponent } from '@modals/containers-modal/containers-modal.component';
import { RunContainerModalComponent } from '@modals/run-container-modal/run-container-modal.component';

@NgModule({
  declarations: [
    AppComponent,
    MenuComponent,
    LogsComponent,
    ModalComponent,
    FooterComponent,
    HeaderComponent,
    NotFoundComponent,
    ContainersModalComponent,
    ConfirmModalComponent,
    RunContainerModalComponent,
    AboutComponent,
    ContainerListComponent,
    PullMenuComponent,
    PullImageComponent,
    ImageListComponent,
    ImageDetailedComponent,
    PullListComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    RouterModule,
    MdbAccordionModule,
    MdbCarouselModule,
    MdbCheckboxModule,
    MdbCollapseModule,
    MdbDropdownModule,
    MdbFormsModule,
    MdbModalModule,
    MdbPopoverModule,
    MdbRadioModule,
    MdbRangeModule,
    MdbRippleModule,
    MdbScrollspyModule,
    MdbTabsModule,
    MdbTooltipModule,
    MdbValidationModule,
    BrowserAnimationsModule,
    HttpClientModule,
    ToastrModule.forRoot({
      timeOut: 2000,
    }),
    ClipboardModule,
    ReactiveFormsModule,
    FormsModule,
    NgSelectModule,
  ],
  providers: [
    {
      provide: HTTP_INTERCEPTORS,
      useClass: HttpInterceptorService,
      multi: true,
    },
  ],
  bootstrap: [AppComponent],
})
export class AppModule {}
