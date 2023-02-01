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
  styleUrls: ['./containers-modal.component.scss'],
})
export class ContainersModalComponent implements OnInit {
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
  constructor(private containerService: ContainerService) {}

  ngOnInit(): void {}

  getStatus(key: keyof Status) {
    return this.status[key];
  }
}
