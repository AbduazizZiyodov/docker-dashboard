import { UrlMatchResult, UrlSegment } from '@angular/router';

export function repositoryUrlMatcher(url: UrlSegment[]): UrlMatchResult | null {
  const result: UrlMatchResult = {
    consumed: url,
    posParams: {},
  };
  let matched: boolean = false;

  if (url[0].path == 'pull' && url.length > 1) {
    if (url.length == 2) {
      result.posParams = {
        repository: new UrlSegment(url[1].path, {}),
      };
      matched = true;
    }

    if (url.length == 3) {
      result.posParams = {
        repository: new UrlSegment(`${url[1].path}/${url[2].path}`, {}),
      };
      matched = true;
    }
    return matched ? result : null;
  }

  return null;
}