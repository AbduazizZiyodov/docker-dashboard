import { Component, Input, OnInit } from '@angular/core';
import { ModalData } from '@models/modal';
import { ContainerService } from '@core/services/container.service';

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
  selector: 'app-containers-modal',
  templateUrl: './containers-modal.component.html',
})
export class ContainersModalComponent {
  @Input() data!: ModalData;

  status: Status = {
    created: 'success',
    restarting: 'warning',
    running: 'success',
    removing: 'danger',
    paused: 'secondary',
    exited: 'danger',
    dead: 'danger',
  };

  getStatus(key: keyof Status) {
    return this.status[key];
  }
}
