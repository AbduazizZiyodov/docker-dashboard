import { Component, OnInit } from '@angular/core';
import { ModalData } from '@models/modal';
import { MdbModalRef } from 'mdb-angular-ui-kit/modal';

@Component({
  selector: 'app-modal',
  templateUrl: './modal.component.html',
})
export class ModalComponent implements OnInit {
  data!: ModalData;
  constructor(public modalRef: MdbModalRef<ModalComponent>) {}

  ngOnInit(): void {
    this.data.modalRef = this.modalRef;
  }
}
