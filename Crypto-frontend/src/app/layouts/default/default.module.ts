import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DefaultComponent } from './default.component';
import { RouterModule } from '@angular/router';
import { SharedModule } from 'src/app/shared/shared.module';
import { MatSidenavModule, MatDividerModule, MatCardModule, MatPaginatorModule, MatTableModule, MatIconModule, MatSidenavContainer, MatListModule, MatProgressSpinnerModule, MatDatepickerModule, MatFormField, MatFormFieldModule, MatNativeDateModule } from '@angular/material';
import { FlexLayoutModule } from '@angular/flex-layout';
import { DashboardService } from 'src/app/modules/dashboard.service';
import { ReviewsComponent } from 'src/app/modules/reviews/reviews.component';
import { TweetsService } from 'src/app/modules/tweets.service';
import { HttpClientModule } from '@angular/common/http';
import { CryptocurrenciesService } from 'src/app/modules/cryptocurrencies.service';
import { ArticlesService } from 'src/app/modules/articles.service';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatInputModule } from '@angular/material/input';
import { MatSort, Sort } from '@angular/material/sort';
import { Ng5SliderModule } from 'ng5-slider';
import { DashboardComponent } from 'src/app/modules/dashboard/dashboard.component';
import { StatsComponent } from 'src/app/modules/stats/stats.component';
import { MatSortModule } from '@angular/material/sort';
import { InfosComponent } from 'src/app/modules/infos/infos.component';

@NgModule({
  exports: [
    MatSidenavModule,
    MatTableModule,
    MatSort,
    MatSortModule
  ],
  declarations: [
    DefaultComponent,
    DashboardComponent,
    ReviewsComponent,
    StatsComponent,
    InfosComponent
  ],
  imports: [
    CommonModule,
    RouterModule,
    HttpClientModule,
    SharedModule,
    MatSidenavModule,
    MatListModule,
    MatDividerModule,
    MatProgressSpinnerModule,
    MatNativeDateModule,
    FlexLayoutModule,
    MatCardModule,
    MatPaginatorModule,
    MatIconModule,
    MatTableModule,
    MatDatepickerModule,
    MatFormFieldModule,
    MatInputModule,
    MatSortModule,
    SharedModule,
    Ng5SliderModule,
    FormsModule,
    ReactiveFormsModule
  ],
  providers: [
    DashboardService,
    TweetsService,
    ArticlesService,
    CryptocurrenciesService
  ]
})
export class DefaultModule { }
