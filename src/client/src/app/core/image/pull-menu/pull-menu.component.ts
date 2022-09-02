import { Component } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';

import { Image } from '@models/image';
import { ImageService } from '@services/image.service';

@Component({
  selector: 'app-pull-menu',
  templateUrl: './pull-menu.component.html',
  styleUrls: ['./pull-menu.component.scss'],
})
export class PullMenuComponent {
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

  getSearchResults(): void {
    this.isLoading = true;
    this.searchResults = [];
    let limit = this.searchForm.getRawValue()['limit'];
    let searchTerm = this.searchForm.getRawValue()['searchTerm'];

    this.imageService
      .searchImages(searchTerm, limit)
      .subscribe((data: Image[]) => {
        this.searchResults = data;
        this.isLoading = false;
      });
  }

  validateLimit(): boolean {
    let limit = parseInt(this.limit?.value);
    return 0 < limit && limit <= 100 ? Number.isInteger(limit) : false;
  }
  
  get searchTerm() {
    return this.searchForm.get('searchTerm');
  }

  get limit() {
    return this.searchForm.get('limit');
  }
}
