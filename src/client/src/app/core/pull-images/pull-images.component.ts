import { Component } from '@angular/core';
import { ToastrService } from 'ngx-toastr';
import { FormControl, FormGroup, Validators } from '@angular/forms';

import { Image } from '@models/image';
import { ImageService } from '@services/image.service';

@Component({
  selector: 'app-pull-images',
  templateUrl: './pull-images.component.html',
  styleUrls: ['./pull-images.component.scss'],
})
export class PullImagesComponent {
  searchResults!: Image[];
  pulledImages!: string[];
  searchForm!: FormGroup;
  pulledImage!: Image;
  isLoading: boolean = false;

  constructor(
    private imageService: ImageService,
    private toastr: ToastrService
  ) {
    this.searchForm = new FormGroup({
      searchTerm: new FormControl('', [
        Validators.required,
        Validators.minLength(3),
      ]),
    });
  }

  getSearchResults() {
    this.isLoading = true;
    let searchTerm = this.searchForm.getRawValue()['searchTerm'];

    this.imageService.getImages().subscribe((data: Image[]) => {
      this.pulledImages = data.map((image: Image) => {
        return image.name.split(':')[0];
      });
    });

    this.imageService.searchImages(searchTerm).subscribe((data: Image[]) => {
      this.searchResults = this.prepareSearchResults(data);
      this.isLoading = false;
    });
  }

  prepareSearchResults(results: Image[]) {
    results.forEach((image: Image) => {
      image.is_pulled = this.pulledImages.includes(image.name);
    });

    return results;
  }

  pullImage(image: Image) {
    image.is_pulling = true;
    this.toastr.warning('Image is pulling ...');
    this.imageService.pullImage(image.name).subscribe((data: any) => {
      this.markAsPulled(image.name);
      image.is_pulling = false;
    });
  }

  markAsPulled(repository: string) {
    for (let image of this.searchResults) {
      if (image.name == repository) {
        image.is_pulled = true;
      }
    }
    this.toastr.success('Image is pulled!');
  }

  get searchTerm() {
    return this.searchForm.get('searchTerm');
  }
}
