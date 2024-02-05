import { Component, OnInit } from '@angular/core';

import { ConfirmationService, Message } from 'primeng/api';
import { MessageService } from 'primeng/api';

import { ContainerService } from '@services/container.service';
import { Container, ContainerActionStatusResponse, ContainerStatus } from '@models/container';


const STATUS_SEVERITY: Map<string, string> = new Map<string, string>(
  [
    ["created", 'warning'],
    ['dead', 'danger'],
    ['running', 'success'],
    ['restarting', 'warning'],
    ['exited', 'danger'],
    ['removing', 'danger']
  ]
)

interface Signal {
  name: string,
  code: string;
}
const killSignals: Signal[] = [
  { name: "SIGINT", code: "SIGINT" },
  { name: "SIGHUP", code: "SIGHUP" },
  { name: "SIGQUIT", code: "SIGQUIT" },
  { name: "SIGKILL", code: "SIGKILL" },
  { name: "SIGTERM", code: "SIGTERM" },
  { name: "SIGSTOP", code: "SIGSTOP" }
];

@Component({
  selector: 'app-containers',
  templateUrl: './containers.component.html',
  styleUrl: './containers.component.scss',
})
export class ContainersComponent implements OnInit {
  isLoading: boolean = true;
  isVisible: boolean = false;
  messages: Message[] = [] as Message[];
  containers: Container[] = [] as Container[];
  selectedContainer: Container = {} as Container;

  selectedSignal!: Signal;
  signalOptions: Signal[] = killSignals;

  constructor(
    private containerService: ContainerService,
    private messageService: MessageService
  ) { }

  ngOnInit(): void {
    this.loadContainers();
  }

  loadContainers() {
    this.containerService.all().subscribe((data: Container[]) => {
      this.containers = data.reverse();
      this.isLoading = false;
    });
  }

  containerAction(container: Container, action: string): void {
    this.messageService.add({
      severity: 'info',
      detail: `Requested action '${action}' for container ${container.name}`,
      life: 1000
    });

    let request;
    switch (action) {
      case 'start':
        request = this.containerService.start(container.short_id);
        break;
      case 'stop':
        request = this.containerService.stop(container.short_id);
        break;
      case 'pause':
        request = this.containerService.pause(container.short_id);
        break;
    }

    request?.subscribe((data: ContainerActionStatusResponse) => {
      this.messageService.add({
        severity: 'success',
        summary: 'Processed',
        detail: `Container ${container.name} status is '${data.status}'`,
      });

      for (let containerToUpdate of this.containers) {
        if (containerToUpdate.short_id == container.short_id) {
          containerToUpdate.status = data.status;
        }
      }
    });
  }

  getContainerStatus(status: string): string {
    let tempStatus: string | undefined = STATUS_SEVERITY.get(status);
    if (tempStatus != undefined) {
      return tempStatus;
    }
    return "primary"
  }
}

