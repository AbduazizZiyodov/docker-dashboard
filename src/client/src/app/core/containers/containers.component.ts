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
  selector: 'app-containers',
  templateUrl: './containers.component.html',
  styleUrls: ['./containers.component.scss'],
})
export class ContainersComponent implements OnInit {
  containers!: Container[];
  timerSubscription!: Subscription;
  subscription!: Subscription;
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
    this.subscription = timer(0, 1000)
      .pipe(switchMap(() => this.containerService.getContainers()))
      .subscribe((data: Container[]) => {
        this.containers = data.reverse();
      });
  }

  ngOnDestroy() {
    this.subscription.unsubscribe();
  }

  startContainer(container_id: string) {
    return this.containerService
      .startStoppedContainer(container_id)
      .subscribe((res: any) => {
        this.changeStatus('running', container_id);
        this.toastr.success(`Container ${container_id} started!`);
      });
  }

  stopContainer(container_id: string) {
    return this.containerService
      .stopContainer(container_id)
      .subscribe((res: any) => {
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

  changeStatus(to: string, container_id: string) {
    for (let container of this.containers) {
      if (container.short_id == container_id) {
        container.status = to;
      }
    }
  }

  getStatus(key: keyof Status) {
    return this.status[key];
  }
  copyId(content: string) {
    this.clipboardService.copyFromContent(content);
    this.toastr.success('Copied!');
  }
}
