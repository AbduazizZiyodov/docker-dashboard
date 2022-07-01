import { Injectable } from '@angular/core';
import {
  HttpEvent,
  HttpHandler,
  HttpInterceptor,
  HttpRequest,
  HttpErrorResponse,
} from '@angular/common/http';
import { Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { catchError } from 'rxjs/operators';
import { Observable, of, throwError } from 'rxjs';

@Injectable()
export class HttpInterceptorService implements HttpInterceptor {
  constructor(private router: Router, private toastr: ToastrService) {}

  intercept(
    request: HttpRequest<any>,
    next: HttpHandler
  ): Observable<HttpEvent<any>> {
    return next.handle(request).pipe(
      catchError((httpError) => {
        let handled: boolean = false;

        if (httpError instanceof HttpErrorResponse) {
          switch (httpError.status) {
            case 404:
              this.router.navigate(['**'], {
                skipLocationChange: true,
              });
              handled = true;
              break;
            case 409:
              this.toastr.error(
                'Another container is using this image!',
                'Conflict'
              );
              handled = true;
              break;

            case 500:
              this.toastr.error(httpError.error.detail, 'Server Error', {
                timeOut: 5000,
              });
              handled = true;
              break;

            default:
              this.toastr.error(httpError.error.detail, 'Error!');
              handled = true;
              break;
          }
        }
        if (handled) {
          return of(httpError);
        } else {
          return throwError(httpError);
        }
      })
    );
  }
}
