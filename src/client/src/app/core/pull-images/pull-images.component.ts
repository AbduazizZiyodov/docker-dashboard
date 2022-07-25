import { Component } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';

import { Image } from '@models/image';
import { ImageService } from '@services/image.service';

@Component({
  selector: 'app-pull-images',
  templateUrl: './pull-images.component.html',
  styleUrls: ['./pull-images.component.scss'],
})
export class PullImagesComponent {
  pulledImage!: Image;
  searchForm!: FormGroup;
  searchResults!: Image[];
  pulledImages!: string[];
  isLoading: boolean = false;

  constructor(private imageService: ImageService) {
    this.searchForm = new FormGroup({
      searchTerm: new FormControl('', [
        Validators.required,
        Validators.minLength(3),
      ]),
      limit: new FormControl(10, []),
    });
  }

  getSearchResults() {
    this.isLoading = true;
    this.searchResults = [];
    let searchTerm = this.searchForm.getRawValue()['searchTerm'];
    let limit = this.searchForm.getRawValue()['limit'];

    this.imageService
      .searchImages(searchTerm, limit)
      .subscribe((data: Image[]) => {
        this.searchResults = data;
        this.isLoading = false;
      });
  }

  isValidLimit(): boolean {
    let limit = parseInt(this.limit?.value);
    if (0 < limit && limit <= 100) {
      return Number.isInteger(parseInt(this.limit?.value));
    }
    return false;
  }
  get searchTerm() {
    return this.searchForm.get('searchTerm');
  }

  get limit() {
    return this.searchForm.get('limit');
  }
}
