import { Injectable }           from '@angular/core';
import { Observable }           from 'rxjs';
import { CanDeactivate,
         ActivatedRouteSnapshot,
         RouterStateSnapshot }  from '@angular/router';
import { ReviewsComponent } from './modules/reviews/reviews.component';


@Injectable({ providedIn: 'root' })
export class CanDeactivateGuard implements CanDeactivate<ReviewsComponent> {

  canDeactivate(
    component: ReviewsComponent,
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot
  ): Observable<boolean> | boolean {
    // you can just return true or false synchronously
    if (ReviewsComponent.pieChartLoaded == true) {
      return true;
    }
    // or, you can also handle the guard asynchronously, e.g.
    // asking the user for confirmation.
  }
}
