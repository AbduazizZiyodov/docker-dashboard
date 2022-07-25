import { UrlMatchResult, UrlSegment } from '@angular/router';

export function repositoryUrlMatcher(url: UrlSegment[]): UrlMatchResult | null {
  /*
    Match repository
        pull/nginx <-- nginx is repo
        pull/dpage/pgadmin <-- dpage/pgadmin is also repo not ROUTE!
  */
  const result: UrlMatchResult = {
    consumed: url,
    posParams: {},
  };
  let matched: boolean = false;

  if (url[0].path == 'pull' && url.length > 1) {
    if (url.length == 2) {
      // like -> pull/nginx
      result.posParams = {
        repository: new UrlSegment(url[1].path, {}),
      };
      matched = true;
    }

    if (url.length == 3) {
      // like -> pull/dpage/pgadmin
      result.posParams = {
        repository: new UrlSegment(`${url[1].path}/${url[2].path}`, {}),
      };
      matched = true;
    }
    return matched ? result : null;
  }

  return null;
}