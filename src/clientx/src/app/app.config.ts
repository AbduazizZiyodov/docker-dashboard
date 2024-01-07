import { ApplicationConfig } from '@angular/core';
import { provideRouter } from '@angular/router';

import { routes } from './app.routes';
import { provideHttpClient } from '@angular/common/http';
import { MessageService } from 'primeng/api';
import { provideAnimations } from '@angular/platform-browser/animations'
export const appConfig: ApplicationConfig = {
  providers: [provideRouter(routes), provideHttpClient(), MessageService, provideAnimations()],
};
