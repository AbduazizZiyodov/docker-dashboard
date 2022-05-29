import { Component, OnInit } from '@angular/core';
import { MdbModalRef } from 'mdb-angular-ui-kit/modal';
import { Container } from 'src/app/core/models/container';

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
  selector: 'app-modal',
  templateUrl: './modal.component.html',
  styleUrls: ['./modal.component.scss'],
})
export class ModalComponent implements OnInit {
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
  constructor(public modalRef: MdbModalRef<ModalComponent>) {}

  ngOnInit(): void {
    console.log(this.containers);
  }

  getStatus(key: keyof Status) {
    return this.status[key];
  }
}
