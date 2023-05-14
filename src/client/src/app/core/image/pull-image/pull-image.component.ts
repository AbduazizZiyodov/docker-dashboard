import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

import { environment } from '@env';
import { Image } from '@models/image';
import { webSocket } from 'rxjs/webSocket';
import { ImageService } from '@services/image.service';
@Component({
  selector: 'app-pull-image',
  templateUrl: './pull-image.component.html',
})
export class PullImageComponent implements OnInit {
  tags: string[] = [];
  imageInfo!: Image | null;
  isLoading: boolean = true;
  selectedTag: string = 'latest';
  pulledVersions!: Image[];
  repository: string = this.route.snapshot.params['repository'];
  ws = webSocket(`${environment.wsUrl}/images/pull`);

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private imageService: ImageService
  ) {}

  ngOnInit(): void {
    this.performSearch();
    this.fetchImages();
  }

  fetchImages(): void {
    this.imageService.getImages().subscribe((images: Image[]) => {
      this.pulledVersions = images.filter(
        (image: Image) => image.name == this.repository
      );
      this.isLoading = false;
    });
  }

  performSearch(): void {
    let limit: number = 1;
    this.imageService
      .searchImages(this.repository, limit)
      .subscribe((image: Image[]) => {
        this.imageInfo = image ? image[0] : null;
      });
  }

  addImageToTasks(): void {
    this.ws.next({
      repository: this.repository,
      tag: this.selectedTag,
      action: 'add',
    });

    this.ws.asObservable().subscribe((data: any) => {
      this.router.navigate(['pull-list']);
    });
  }

  ngOnDestroy() {
    this.ws.complete();
  }
}
