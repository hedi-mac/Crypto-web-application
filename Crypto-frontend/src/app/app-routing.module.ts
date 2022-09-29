import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { CanDeactivateGuard } from './canDeactivateGuard.component';
import { CanDeactivateStats } from './canDeactivateStats.component';
import { DefaultComponent } from './layouts/default/default.component';
import { StatsComponent } from './modules/stats/stats.component';
import { ReviewsComponent } from './modules/reviews/reviews.component';
import { DashboardComponent } from './modules/dashboard/dashboard.component';
import { InfosComponent } from './modules/infos/infos.component';


const routes: Routes = [{
  path: '',
  component: DefaultComponent,
  children: [{
    path: '',
    component: DashboardComponent
  }, {
    path: 'reviews/:crypto',
    component: ReviewsComponent,
    canDeactivate: [CanDeactivateGuard]
  }, {
    path: 'stats/:duration',
    component: StatsComponent,
    canDeactivate: [CanDeactivateStats]
  }, {
    path: 'infos/:type',
    component: InfosComponent
  }]
}];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
