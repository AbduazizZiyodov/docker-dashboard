import { ToastrService } from 'ngx-toastr';
import { ActivatedRoute } from '@angular/router';
import { Component, OnInit } from '@angular/core';

import { Image } from '@models/image';
import { ImageService } from '@services/image.service';

@Component({
  selector: 'app-pull-image',
  templateUrl: './pull-image.component.html',
  styleUrls: ['./pull-image.component.scss'],
})
export class PullImageComponent implements OnInit {
  repoTags!: string[];
  imageInfo!: Image | null;
  isLoading: boolean = true;
  isPulling: boolean = false;
  selectedTag: any;
  pulledVersions!: Image[];
  repository: string = this.route.snapshot.params['repository'];
  constructor(
    private toastr: ToastrService,
    private route: ActivatedRoute,
    private imageService: ImageService
  ) {}

  ngOnInit(): void {
    let limit: number = 1;
    this.imageService
      .searchImages(this.repository, limit)
      .subscribe((image: Image[]) => {
        this.imageInfo = image ? image[0] : null;
        this.imageService.getImages().subscribe((images: Image[]) => {
          this.pulledVersions = images.filter(
            (image: Image) => image.name == this.repository
          );
        });
      });

    this.imageService
      .getAllTags(this.repository)
      .subscribe((repoTags: string[]) => {
        this.repoTags = repoTags;
        this.isLoading = false;
        this.removePulledTags();
      });
  }

  removePulledTags() {
    let pulledTags: string[] = [];

    this.pulledVersions.forEach((image) => {
      pulledTags.push(String(image.tag));
    });

    this.repoTags = this.repoTags.filter(
      (tag: string) => !pulledTags.includes(tag)
    );
  }

  pullImage() {
    this.isPulling = true;
    this.toastr.warning('Pulling ...');
    this.imageService
      .pullImage(this.repository, this.selectedTag)
      .subscribe((pulledImage: Image) => {
        this.isPulling = false;
        this.toastr.success(`Image ${this.repository} is pulled!`);
        this.pulledVersions.push(pulledImage);
        this.selectedTag = null;
        this.removePulledTags();
      });
  }
}
