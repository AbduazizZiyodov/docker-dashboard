import { Component, OnInit } from '@angular/core';
import { ImageService } from '@services/image.service';
import { Image } from '@models/image';


@Component({
  selector: 'app-images',
  templateUrl: './images.component.html',
  styleUrls: ['./images.component.scss'],
})
export class ImagesComponent implements OnInit {
  images!: Image[];
  constructor(
    private imageService: ImageService,
  ) {}

  ngOnInit(): void {
    this.getImages();
  }

  getImages() {
    this.imageService.getImages().subscribe((images: Image[]) => {
      this.images = images;
    });
  }

}
