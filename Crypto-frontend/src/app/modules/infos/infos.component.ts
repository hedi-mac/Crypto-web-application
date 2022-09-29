import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ArticlesService } from '../articles.service';
import { CryptocurrenciesService } from '../cryptocurrencies.service';
import { DashboardService } from '../dashboard.service';
import { ReviewsService } from '../reviews.service';

@Component({
  selector: 'app-infos',
  templateUrl: './infos.component.html',
  styleUrls: ['./infos.component.scss']
})
export class InfosComponent implements OnInit {

  type

  constructor(private activatedRoute: ActivatedRoute,
    private router: Router) {
      this.activatedRoute.params.subscribe(s => {
        this.type = s['type'];
      });
  }



  ngOnInit() {

    
  }

}
