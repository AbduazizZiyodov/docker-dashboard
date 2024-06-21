import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations'
import { AppComponent } from './app.component';
import { AppRoutingModule } from './app-routing.module';
// Third party
import { ClipboardModule } from 'ngx-clipboard';

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
import { PanelModule } from 'primeng/panel';
import { DialogModule } from 'primeng/dialog';
import { ToolbarModule } from 'primeng/toolbar'
import { TooltipModule } from 'primeng/tooltip';
import { DividerModule } from 'primeng/divider';
import { ListboxModule } from 'primeng/listbox';
import { SidebarModule } from 'primeng/sidebar';
import { DropdownModule } from 'primeng/dropdown';
import { FieldsetModule } from 'primeng/fieldset'
import { StyleClassModule } from 'primeng/styleclass';
import { InputTextModule } from 'primeng/inputtext';
import { PanelMenuModule } from 'primeng/panelmenu';
import { TieredMenuModule } from 'primeng/tieredmenu';
import { InputGroupModule } from 'primeng/inputgroup';
import { InputNumberModule } from 'primeng/inputnumber';
import { InputGroupAddonModule } from 'primeng/inputgroupaddon';
import { ProgressSpinnerModule } from 'primeng/progressspinner';
// Components
import { ContainersComponent } from '@containers/containers.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { CreateContainersComponent } from './create-containers/create-containers.component';


@NgModule({
  declarations: [
    AppComponent,
    ContainersComponent,
    DashboardComponent,
    CreateContainersComponent,

  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    AppRoutingModule,
    CommonModule,
    HttpClientModule,
    CardModule,
    ButtonModule,
    ToastModule,
    AvatarModule,
    SidebarModule,
    TableModule,
    TagModule,
    ListboxModule,
    MenuModule,
    BadgeModule,
    TieredMenuModule,
    PanelModule,
    DividerModule,
    PanelMenuModule,
    DropdownModule,
    ToolbarModule,
    FieldsetModule,
    TooltipModule,
    DialogModule,
    FormsModule,
    RouterModule,
    InputTextModule,
    InputNumberModule,
    InputGroupModule,
    InputGroupAddonModule,
    StyleClassModule,
    ProgressSpinnerModule,
    ClipboardModule
  ],
  providers: [MessageService],
  bootstrap: [AppComponent]
})
export class AppModule { }
