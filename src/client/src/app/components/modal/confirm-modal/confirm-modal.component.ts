import { Component, Input } from '@angular/core';
import { ModalData } from '@models/modal';
import { Image } from '@models/image';
import { ImageService } from '@services/image.service';
import { ToastrService } from 'ngx-toastr';
import { Router } from '@angular/router';
import { ContainerService } from '@services/container.service';

@Component({
  selector: 'app-confirm-modal',
  templateUrl: './confirm-modal.component.html',
})
export class ConfirmModalComponent {
  @Input() data!: ModalData | undefined;

  constructor(
    private imageService: ImageService,
    private toastr: ToastrService,
    private router: Router,
    private containerService: ContainerService
  ) {}

  delete() {
    if (this.data?.modal_type == 'delete_image_modal') {
      this.deleteImage(this.data.resource);
    } else if (this.data?.modal_type == 'delete_container_modal') {
      this.deleteContainer(this.data.resource?.id);
    }
  }

  deleteContainer(container_id: string | any) {
    this.containerService
      .deleteContainer(container_id)
      .subscribe((res: any) => {
        this.toastr.error(`Container ${container_id} deleted!`);
        this.data?.modalRef?.close(container_id);
      });
  }

  deleteImage(image: Image | any) {
    this.imageService.deleteImage(image.short_id).subscribe((data) => {
      this.toastr.error(`Image ${image.name + ':' + image.tag} deleted!`);
      this.router.navigate(['images']);
      this.data?.modalRef?.close();
    });
  }
}
