import { ToastrService } from 'ngx-toastr';
import { ActivatedRoute } from '@angular/router';
import { ClipboardService } from 'ngx-clipboard';
import { Component, OnInit } from '@angular/core';
import { MdbModalRef, MdbModalService } from 'mdb-angular-ui-kit/modal';

import { Image } from '@models/image';
import { Container } from '@models/container';
import { ImageService } from '@services/image.service';
import { ModalComponent } from '@components/modal/modal.component';

@Component({
  selector: 'app-image-detailed',
  templateUrl: './image-detailed.component.html',
})
export class ImageDetailedComponent implements OnInit {
  imageId: string = this.route.snapshot.params['id'];
  image!: Image;
  isLoading: boolean = true;
  modalRef: MdbModalRef<ModalComponent> | null = null;

  constructor(
    private route: ActivatedRoute,
    private toastr: ToastrService,
    private imageService: ImageService,
    private clipboardService: ClipboardService,
    private modalService: MdbModalService
  ) {}

  ngOnInit(): void {
    this.imageService.getImage(this.imageId).subscribe((image: Image) => {
      this.image = image;
      this.isLoading = false;
    });
  }

  getContainerByImage(image_id: string) {
    this.imageService
      .getContainersByImage(image_id)
      .subscribe((containers: Container[]) => {
        this.modalRef = this.modalService.open(ModalComponent, {
          data: {
            data: {
              title: 'Containers',
              containers: containers,
              modal_type: 'containers_modal',
            },
          },
        });
      });
  }

  getDeleteModal(image: Image) {
    this.modalRef = this.modalService.open(ModalComponent, {
      data: {
        data: {
          title: 'Delete Image',
          resource: image,
          modal_type: 'delete_image_modal',
        },
      },
    });
  }

  getRunContainerModal(image: Image) {
    this.modalRef = this.modalService.open(ModalComponent, {
      data: {
        data: {
          title: 'Run Container',
          resource: image,
          modal_type: 'run_container_modal',
        },
      },
    });
  }

  copyId(content: string) {
    this.clipboardService.copyFromContent(content);
    this.toastr.success('Copied!');
  }
}
