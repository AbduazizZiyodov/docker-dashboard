import { ToastrService } from 'ngx-toastr';
import { ClipboardService } from 'ngx-clipboard';
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { MdbModalRef, MdbModalService } from 'mdb-angular-ui-kit/modal';
import { Image } from '@models/image';
import { ModalData } from '@models/modal';
import { ImageService } from '@services/image.service';
import { ModalComponent } from '@components/modal/modal.component';
import { Container } from '@angular/compiler/src/i18n/i18n_ast';

@Component({
  selector: 'app-image',
  templateUrl: './image.component.html',
  styleUrls: ['./image.component.scss'],
})
export class ImageComponent implements OnInit {
  imageId: string = this.route.snapshot.params['id'];
  image!: Image;
  isLoading: boolean = false;
  modalRef: MdbModalRef<ModalComponent> | null = null;

  constructor(
    private route: ActivatedRoute,
    private toastr: ToastrService,
    private imageService: ImageService,
    private clipboardService: ClipboardService,
    private modalService: MdbModalService
  ) {}

  ngOnInit(): void {
    this.getImage();
  }

  getImage() {
    this.isLoading = true;
    this.imageService.getImage(this.imageId).subscribe((data: Image) => {
      this.image = data;
      this.isLoading = false;
    });
  }

  copyId(content: string) {
    this.clipboardService.copyFromContent(content);
    this.toastr.success('Copied!');
  }

  getContainerByImage(image_id: string) {
    this.imageService.getContainersByImage(image_id).subscribe((data) => {
      let modalData: ModalData = {
        is_container_modal: true,
        title: 'Containers',
        containers: data,
      };

      this.modalRef = this.modalService.open(ModalComponent, {
        data: {
          data: modalData,
        },
      });
    });
  }

  getConfirmModal(image: Image) {
    let modalData: ModalData = {
      title: 'Delete Image',
      resource: image,
      is_delete_image_modal: true,
    };

    this.modalRef = this.modalService.open(ModalComponent, {
      data: {
        data: modalData,
      },
    });
  }
}
