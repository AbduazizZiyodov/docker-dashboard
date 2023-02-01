import { Component, OnInit } from '@angular/core';

import { Image } from '@models/image';
import { ImageService } from '@services/image.service';
import { Observable, shareReplay } from 'rxjs';

@Component({
  selector: 'app-image-list',
  templateUrl: './image-list.component.html',
})
export class ImageListComponent implements OnInit {
  images$ = new Observable<Image[]>();
  constructor(private imageService: ImageService) {}

  ngOnInit(): void {
    this.images$ = this.imageService.getImages().pipe(shareReplay(1));
  }
}
