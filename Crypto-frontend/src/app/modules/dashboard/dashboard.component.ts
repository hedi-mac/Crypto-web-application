import { Component, OnInit } from '@angular/core';
import { ArticlesService } from '../articles.service';
import { CryptocurrenciesService } from '../cryptocurrencies.service';
import { DashboardService } from '../dashboard.service';
import { ReviewsService } from '../reviews.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {

  cards = [];
  cryptocurrencies;
  positivesWeek : string[]
  negativesWeek : string[]
  positivesMonth : string[]
  negativesMonth : string[]
  tab
  dataLoaded = false
  evolutionLoaded = false
  day1
  day7

  constructor(private reviewsService:ReviewsService,
    private cryptocurrenciesService:CryptocurrenciesService,
    private dashboardService: DashboardService) {

  }



  ngOnInit() {
    this.day7 = (new Date(new Date().setDate(new Date().getDate()-(7-0-1)))).toString().substring(0, 16);
    this.day1 = (new Date(new Date().setDate(new Date().getDate()-(0)))).toString().substring(0, 16);
    this.cryptocurrenciesService.getCryptocurrencies().subscribe(
      (data) => { 
        this.cryptocurrencies = data['data'];
      
        this.reviewsService.getEvolutionStats(7, "all").subscribe((res) => {
          this.tab = res['data']
        }, (err) => console.log(err));

      this.reviewsService.getBarStats(7).subscribe((data) => {
          this.positivesWeek = data["data"][0].positives
          this.negativesWeek = data["data"][0].negatives  
          this.reviewsService.getBarStats(28).subscribe((d) => {
            this.positivesMonth = d["data"][0].positives
            this.negativesMonth = d["data"][0].negatives  
            this.dataLoaded = true 
          }, (err) => console.log(err));
        }, (err) => console.log(err));
        
        
      },
      (error) => { console.log(error); }
    );
    
    
  }

}
