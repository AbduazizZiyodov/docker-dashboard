import { Component, OnInit } from '@angular/core';

import { Message } from 'primeng/api';

import { Container } from '@models/container';
import { ContainerService } from '@services/container.service';
import { MessageService } from 'primeng/api';


interface StatusFilter {
  label: string
  value: string

}

@Component({
  selector: 'app-containers',
  templateUrl: './containers.component.html',
  styleUrl: './containers.component.scss'
})
export class ContainersComponent implements OnInit {
  containers!: Container[];
  messages!: Message[];
  selectedContainers!: Container[];
  statuses: StatusFilter[] = [
    { label: 'Exited', value: 'exited' },
    { label: 'Running', value: 'running' }
  ];

  constructor(
    private containerService: ContainerService,
    private messageService: MessageService
  ) { }


  ngOnInit(): void {
    this.loadContainers()
  }

  loadContainers() {
    this.containerService.all()
      .subscribe((data: Container[]) => {
        this.containers = data.reverse();
      });
  }

  startContainers() {
    console.log(this.selectedContainers)

    for (let container of this.selectedContainers) {
      this.messageService.add({ severity: 'info', summary: 'Starting', detail: `Starting container ${container.name}` });
      this.containerService.startStoppedContainer(container.id).subscribe((data: any) => {
        if (data.started) {
          this.messageService.add({ severity: 'success', summary: 'Started', detail: `Container ${container.name} started` });
        }
        this.loadContainers()
      })
    }

  }
  stopContainers() {
    for (let container of this.selectedContainers) {
      this.messageService.add({ severity: 'info', summary: 'Stopping', detail: `Stopping container ${container.name}` });
      this.containerService.stopContainer(container.id).subscribe((data: any) => {
        if (data.stopped) {
          this.messageService.add({ severity: 'warn', summary: 'Stopped', detail: `Container ${container.name} is stopped` });
        }
        this.loadContainers()
      })
    }
  }


  getContainerStatus(status: string): string {
    switch (status.toLowerCase()) {
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
