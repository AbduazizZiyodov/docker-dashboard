import { Component, OnInit } from '@angular/core';
import { ImageService } from '../services/image.service';
import { ToastrService } from 'ngx-toastr';
import { ClipboardService } from 'ngx-clipboard';
import { Image } from '../models/image';
import { MdbModalRef, MdbModalService } from 'mdb-angular-ui-kit/modal';
import { ModalComponent } from 'src/app/components/modal/modal.component';

@Component({
  selector: 'app-images',
  templateUrl: './images.component.html',
  styleUrls: ['./images.component.scss'],
})
export class ImagesComponent implements OnInit {
  images!: Image[];
  modalRef: MdbModalRef<ModalComponent> | null = null;

  constructor(
    private imageService: ImageService,
    private clipboardService: ClipboardService,
    private toastr: ToastrService,
    private modalService: MdbModalService
  ) {}

  ngOnInit(): void {
    this.getImages();
  }

  getImages() {
    this.imageService.getImages().subscribe((images: Image[]) => {
      this.images = images;
    });
  }

  copyId(content: string) {
    this.clipboardService.copyFromContent(content);
    this.toastr.success('Copied!');
  }

  deleteImage(image_id: string) {
    this.imageService.deleteImage(image_id).subscribe((data) => {
      this.getImages();
      this.toastr.error(`Image ${image_id} deleted!`);
    });
  }
  getContainerByImage(image_id: string) {
    this.imageService.getContainersByImage(image_id).subscribe((data) => {
      this.modalRef = this.modalService.open(ModalComponent, {
        data: {
          containers: data,
        },
      });
    });
  }
}
