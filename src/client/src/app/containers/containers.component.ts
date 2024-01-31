import { Component, OnInit } from '@angular/core';

import { Message } from 'primeng/api';
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

  startContainer(container: Container) {
    this.messageService.add({
      severity: 'info',
      summary: 'Starting',
      detail: `Starting container ${container.name}`,
    });
    this.isLoading = true;

    this.containerService
      .start(container.id)
      .subscribe((data: ContainerActionStatusResponse) => {
        if (data.status == ContainerStatus.running) {
          this.messageService.add({
            severity: 'success',
            summary: 'Started',
            detail: `Container ${container.name} started`,
          });
        }
        this.loadContainers();
      });

  }

  stopContainer(container: Container) {
    this.messageService.add({
      severity: 'error',
      summary: 'Stopping',
      detail: `Stopping container ${container.name}`,
    });
    this.isLoading = true;
    this.containerService
      .stop(container.id)
      .subscribe((data: ContainerActionStatusResponse) => {
        if (data.status == ContainerStatus.exited) {
          this.messageService.add({
            severity: 'warn',
            summary: 'Stopped',
            detail: `Container ${container.name} is stopped`,
          });
        }
        this.loadContainers();
      });
  }

  pauseContainer(container: Container) {
    this.messageService.add({
      severity: 'error',
      summary: 'Stopping',
      detail: `Stopping container ${container.name}`,
    });
    this.isLoading = true;
    this.containerService
      .pause(container.id)
      .subscribe((data: ContainerActionStatusResponse) => {
        if (data.status == ContainerStatus.paused) {
          this.messageService.add({
            severity: 'info',
            summary: 'Paused',
            detail: `Container ${container.name} is paused`,
          });
        }
        this.loadContainers();
      });
  }

  killContainer() {
    this.messageService.add({
      severity: 'info',
      summary: 'Killing',
      detail: `Killing container ${this.selectedContainer.name}`,
    });
    this.isLoading = true;
    this.isVisible = false;

    this.containerService
      .kill(this.selectedContainer.id, this.selectedSignal.code)
      .subscribe((data: ContainerActionStatusResponse) => {
        if (data.status == ContainerStatus.exited) {
          this.messageService.add({
            severity: 'warn',
            summary: 'Killed',
            detail: `Container ${this.selectedContainer.name} is killed`,
          });
        }
        this.loadContainers();
      });
  }

  openContainerKillDialog(container: Container) {
    this.isVisible = true;
    this.selectedContainer = container;
  }

  getContainerStatus(status: string): string {
    let tempStatus: string | undefined = STATUS_SEVERITY.get(status);
    if (tempStatus != undefined) {
      return tempStatus;
    }
    return "primary"
  }
}

