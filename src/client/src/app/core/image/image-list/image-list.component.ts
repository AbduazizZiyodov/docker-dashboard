import { Component, OnInit } from '@angular/core';

import { Image } from '@models/image';
import { ImageService } from '@services/image.service';

@Component({
  selector: 'app-image-list',
  templateUrl: './image-list.component.html',
  styleUrls: ['./image-list.component.scss'],
})
export class ImageListComponent implements OnInit {
  images!: Image[];
  constructor(private imageService: ImageService) {}

  ngOnInit(): void {
    this.imageService.getImages().subscribe((images: Image[]) => {
      this.images = images;
    });
  }
}
