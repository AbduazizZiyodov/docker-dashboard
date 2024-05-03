import { Component, OnInit } from '@angular/core';
import { ImageService } from '@services/image.service'
import { Image } from '@models/image'
import { IMAGE_CONFIG } from '@angular/common';

@Component({
  selector: 'app-create-containers',
  templateUrl: './create-containers.component.html',
  styleUrl: './create-containers.component.scss'
})
export class CreateContainersComponent implements OnInit {
  selectedImage: Image = {} as Image;
  images: Image[] = [] as Image[];
  imageOptions: any;
  constructor(private imageService: ImageService) { }


  ngOnInit(): void {
    this.imageService.all().subscribe((data: Image[]) => {
      this.images = data;
      for (let image of data) {
        this.imageOptions[image.name + ":" + image.tag] = image.short_id
      }
    })
  }
}
