import { Injectable }           from '@angular/core';
import { Observable }           from 'rxjs';
import { CanDeactivate,
         ActivatedRouteSnapshot,
         RouterStateSnapshot }  from '@angular/router';
import { ReviewsComponent } from './modules/reviews/reviews.component';
import { StatsComponent } from './modules/stats/stats.component';


@Injectable({ providedIn: 'root' })
export class CanDeactivateStats implements CanDeactivate<StatsComponent> {

  canDeactivate(
    component: StatsComponent,
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot
  ): Observable<boolean> | boolean {
    // you can just return true or false synchronously
    if (StatsComponent.dataLoaded == true) {
      return true;
    }
    // or, you can also handle the guard asynchronously, e.g.
    // asking the user for confirmation.
  }
}
