import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { Image } from '@models/image';
import { ImageService } from '@services/image.service';
import { MdbModalRef, MdbModalService } from 'mdb-angular-ui-kit/modal';
import { ModalComponent } from 'src/app/components/modal/modal.component';
import { ClipboardService } from 'ngx-clipboard';

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
    private router: Router,
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

  deleteImage(image: Image) {
    this.imageService.deleteImage(image.short_id).subscribe((data) => {
      this.toastr.error(`Image ${image.name} deleted!`);
      this.router.navigate(['images']);
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
