import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations'

import { AppComponent } from './app.component';
import { AppRoutingModule } from './app-routing.module';

// PrimeNG modules
import { TagModule } from 'primeng/tag'
import { MenuModule } from 'primeng/menu';
import { CardModule } from 'primeng/card';
import { BadgeModule } from 'primeng/badge';
import { ToastModule } from 'primeng/toast';
import { MessageService } from 'primeng/api';
import { TableModule } from 'primeng/table';
import { AvatarModule } from 'primeng/avatar'
import { ButtonModule } from 'primeng/button';
import { ListboxModule } from 'primeng/listbox';
import { SidebarModule } from 'primeng/sidebar';
import { MenubarModule } from 'primeng/menubar';
// Components
import { ContainersComponent } from '@containers/containers.component';

@NgModule({
  declarations: [
    AppComponent,
    ContainersComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    AppRoutingModule,
    CommonModule,
    HttpClientModule,
    CardModule,
    ButtonModule,
    MenubarModule,
    ToastModule,
    AvatarModule,
    SidebarModule,
    TableModule,
    TagModule,
    ListboxModule,
    MenuModule,
    BadgeModule
  ],
  providers: [MessageService],
  bootstrap: [AppComponent]
})
export class AppModule { }
