import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-not-found',
  template: `
  <div class="container p-2">
  <div class="card p-3" data-aos="zoom-in" data-aos-duration="500">
    <img
      src="assets/images/not-found.svg"
      class="card-img-top p-1"
      style="width: 200px; margin: auto"
    />
    <div class="card-body">
      <h2 class="card-title text-center">Not found ...</h2>
      <hr />
      <div class="text-center">
        <button class="btn dodger-blue-bg text-white m-a" routerLink="">
          Go home
        </button>
      </div>
    </div>
  </div>
</div>

  `,
})
export class NotFoundComponent { }
