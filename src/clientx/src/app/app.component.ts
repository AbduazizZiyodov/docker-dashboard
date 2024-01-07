import { Component, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';

// Import PrimeNG modules
import { CardModule } from 'primeng/card';
import { ButtonModule } from 'primeng/button';
import { MenubarModule } from 'primeng/menubar';
import { MenuItem, PrimeNGConfig } from 'primeng/api';

import { ThemeService } from './services/theme.service';
import { ToastModule } from 'primeng/toast';
import { SidebarModule } from 'primeng/sidebar';
import { Sidebar } from 'primeng/sidebar';
import {AvatarModule} from 'primeng/avatar'
@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    CommonModule,
    RouterOutlet,
    ButtonModule,
    ToastModule,
    CardModule,
    MenubarModule,
    SidebarModule,
    AvatarModule

  ],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {
  isDark: boolean = false;
  items: MenuItem[] | undefined;
  sidebarVisible: boolean = false;
  @ViewChild('sidebarRef') sidebarRef!: Sidebar;

  closeCallback(e: Event): void {
    this.sidebarRef.close(e);
  }


  constructor(
    private primengConfig: PrimeNGConfig,
    private themeService: ThemeService
  ) { }

  changeTheme() {
    this.isDark = !this.isDark;
    this.themeService.switchTheme(this.isDark ? 'dark' : 'light');
  }

  ngOnInit() {
    this.primengConfig.ripple = true;
    this.items = [
      {
        label: 'Containers',
        icon: 'fa-solid fa-box-open',
        routerLink: 'containers',
        items: [
          {
            label: 'Create',
            icon: 'fa-regular fa-square-plus',
          }
        ]
      },
      {
        label: 'Images',
        icon: 'fa-regular fa-file',
        items: [
          {
            label: 'Pull',
            icon: 'fa-solid fa-cloud-arrow-down'
          }
        ]
      },
      {
        label: 'Volumes',
        icon: 'fa-solid fa-hard-drive',
        items: [
          {
            label: 'Create',
            icon: 'fa-solid fa-folder-plus'
          }
        ]
      },
      {
        label: 'Swarm Mode',
        icon: 'fa-solid fa-server',
        items: [
          {
            label: 'Somting',
            icon: 'pi pi-fw pi-pencil',
          }
        ]
      },
      {
        label: 'About',
        icon: 'fa-solid fa-circle-info'
      }
    ];
  }

}
