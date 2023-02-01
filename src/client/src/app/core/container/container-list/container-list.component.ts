import { ToastrService } from 'ngx-toastr';
import { ClipboardService } from 'ngx-clipboard';
import { Component, OnInit } from '@angular/core';
import { MdbModalRef, MdbModalService } from 'mdb-angular-ui-kit/modal';

import { Status } from '@models/status';
import { Container } from '@models/container';
import { ContainerService } from '@services/container.service';
import { ModalComponent } from '@components/modal/modal.component';

import { Subscription, timer } from 'rxjs';
import { switchMap } from 'rxjs/operators';

@Component({
  selector: 'app-container-list',
  templateUrl: './container-list.component.html',
  styleUrls: ['./container-list.component.scss'],
})
export class ContainerListComponent implements OnInit {
  containers!: Container[];
  timerSubscription!: Subscription;
  modalRef: MdbModalRef<ModalComponent> | null = null;

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
    private clipboardService: ClipboardService,
    private modalService: MdbModalService
  ) {}

  ngOnInit(): void {
    this.timerSubscription = timer(0, 3000)
      .pipe(switchMap(() => this.containerService.getContainers()))
      .subscribe((data: Container[]) => {
        this.containers = data.reverse();
      });
  }

  startContainer(container_id: string) {
    this.containerService
      .startStoppedContainer(container_id)
      .subscribe((res: any) => {
        this.changeStatus('running', container_id);
        this.toastr.success(`Container ${container_id} started!`);
      });
  }

  stopContainer(container_id: string) {
    this.containerService.stopContainer(container_id).subscribe((res: any) => {
      this.changeStatus('exited', container_id);
      this.toastr.warning(`Container ${container_id} stopped!`);
    });
  }

  getConfirmModal(container: Container) {
    this.modalRef = this.modalService.open(ModalComponent, {
      data: {
        data: {
          title: 'Delete Container',
          resource: container,
          modal_type: 'delete_container_modal',
        },
      },
    });

    this.modalRef.onClose.subscribe((container_id: any) => {
      this.containers = this.containers.filter(
        (container) => container.id != container_id
      );
    });
  }

  changeStatus(status: string, container_id: string) {
    this.containers.forEach((container: Container) => {
      if (container.short_id == container_id) {
        container.status = status;
      }
    });
  }

  getStatus(key: keyof Status) {
    return this.status[key];
  }

  copyId(content: string) {
    this.clipboardService.copyFromContent(content);
    this.toastr.success('Copied!');
  }

  ngOnDestroy() {
    this.timerSubscription.unsubscribe();
  }
}
