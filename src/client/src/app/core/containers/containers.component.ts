import { Component, OnInit } from '@angular/core';
import { ClipboardService } from 'ngx-clipboard';
import {  ToastrService } from 'ngx-toastr';
import { Container } from '../models/container';
import { ContainerService } from '../services/container.service';

interface Status {
  created: string;
  restarting: string;
  running: string;
  removing: string;
  paused: string;
  exited: string;
  dead: string;
}

@Component({
  selector: 'app-containers',
  templateUrl: './containers.component.html',
  styleUrls: ['./containers.component.scss'],
})
export class ContainersComponent implements OnInit {
  containers!: Container[];
  status: Status = {
    created: 'success',
    restarting: 'warning',
    running: 'success',
    removing: 'danger',
    paused: 'secondary',
    exited: 'danger',
    dead: 'danger',
  };

  constructor(
    private containerService: ContainerService,
    private toastr: ToastrService,
    private clipboardService: ClipboardService
  ) {}

  ngOnInit(): void {
    this.getContainers();
  }

  getContainers() {
    this.containerService.getContainers().subscribe((data: Container[]) => {
      this.containers = data.reverse();
    });
  }
  deleteContainer(container_id: string) {
    return this.containerService
      .deleteContainer(container_id)
      .subscribe((res: any) => {
        this.getContainers();
        this.toastr.error(`Container ${container_id} deleted!`);
      });
  }

  startContainer(container_id: string) {
    return this.containerService
      .startStoppedContainer(container_id)
      .subscribe((res: any) => {
        this.getContainers();
        this.toastr.success(`Container ${container_id} started!`);
      });
  }

  stopContainer(container_id: string) {
    return this.containerService
      .stopContainer(container_id)
      .subscribe((res: any) => {
        this.getContainers();
        this.toastr.warning(`Container ${container_id} stopped!`);
      });
  }

  getStatus(key: keyof Status) {
    return this.status[key];
  }
  copyId(content: string) {
    this.clipboardService.copyFromContent(content);
    this.toastr.success('Copied!');
  }
}
