import { Component, OnInit } from '@angular/core';

import { Message } from 'primeng/api';

import { Container } from '@models/container';
import { ContainerService } from '@services/container.service';
import { MessageService } from 'primeng/api';


@Component({
  selector: 'app-containers',
  templateUrl: './containers.component.html',
  styleUrl: './containers.component.scss'
})
export class ContainersComponent implements OnInit {
  containers!: Container[];
  messages!: Message[];

  constructor(
    private containerService: ContainerService, private messageService: MessageService
  ) { }

  showSuccess() {
    this.messageService.add({ severity: 'success', summary: 'Success', detail: 'Message Content' });
  }

  showInfo() {
    this.messageService.add({ severity: 'info', summary: 'Info', detail: 'Message Content' });
  }

  showWarn() {
    this.messageService.add({ severity: 'warn', summary: 'Warn', detail: 'Message Content' });
  }

  showError() {
    this.messageService.add({ severity: 'error', summary: 'Error', detail: 'Message Content' });
  }

  startContainer() {
    console.log("HELLO", this.messages)
    this.messages = [
      { severity: 'success', summary: 'Success', detail: 'Message Content', life: 0 }
    ];
  }

  ngOnInit(): void {
    this.containerService.all()
      .subscribe((data: Container[]) => {
        this.containers = data.reverse();
      });
  }


  getContainerStatus(status: string): string {
    switch (status) {
      case 'created':
        return 'warning';
      case 'dead':
        return 'danger'
      case 'running':
        return 'success'
      case 'restarting':
        return 'warning';
      case 'exited':
        return 'danger';
      case 'removing':
        return 'danger'
      default:
        return 'primary'
    }
  }
}
