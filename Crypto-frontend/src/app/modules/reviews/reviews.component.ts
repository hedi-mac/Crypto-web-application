import { Component, Inject, LOCALE_ID, OnInit, ViewChild } from '@angular/core';
import { DashboardService } from '../dashboard.service';
import { MatTableDataSource, MatPaginator, Sort, MatSort } from '@angular/material';
import { Tweet } from 'src/app/models/tweet';
import { TweetsService } from '../tweets.service';
import { ActivatedRoute, ActivatedRouteSnapshot, NavigationEnd, NavigationStart, Router, RouterStateSnapshot } from '@angular/router';
import { ArticlesService } from '../articles.service';
import { Article } from 'src/app/models/article';
import { environment } from 'src/environments/environment';
import { ReviewsService } from '../reviews.service';
import { interval, Observable, Subscription } from 'rxjs';
import { delay } from 'rxjs/operators';
import { FormControl, FormGroup } from '@angular/forms';
import { DatePipe, formatNumber } from '@angular/common';
import { ChangeContext, LabelType, Options } from 'ng5-slider';

const TWEETS_ELEMENT_DATA: Tweet[] = [];

@Component({
  selector: 'app-reviews',
  templateUrl: './reviews.component.html',
  styleUrls: ['./reviews.component.scss']
})
export class ReviewsComponent implements OnInit {

  tweets
  articles
  crypto
  cryptocurrencyName
  pieChart = undefined
  public static pieChartLoaded = false
  tweetsDisplayedColumns: string[] = ['text', 'created_at', 'score', 'label'];
  tweetsDataSource : any = new MatTableDataSource<Tweet>([]);
  articlesDisplayedColumns: string[] = ['text', 'created_at', 'score', 'label', 'url', 'visits'];
  articlesDataSource : any = new MatTableDataSource<Article>([]);
  url = environment.APIEndpoint
  iconUrl = environment.CRYPTOIcon
  tweetsLength
  articlesLength

  @ViewChild('tweetsPaginator',  { static: true }) tweetsPaginator: MatPaginator;
  @ViewChild('articlesPaginator', { static: true }) articlesPaginator: MatPaginator;
  @ViewChild('sortArticles', { static: false }) sortArticles: MatSort;
  @ViewChild('sortTweets', { static: false }) sortTweets: MatSort;

  constructor(private reviewsService:ReviewsService,
    private tweetsService:TweetsService,
    private articlesService: ArticlesService,
    private activatedRoute: ActivatedRoute,
    @Inject(LOCALE_ID) private locale: string,
    private router: Router) {
      router.events.forEach((event) => {
        if (event instanceof NavigationEnd) {

      this.dateRange = this.createDateRange();
      this.value = this.dateRange[0].getDate();
      this.maxValue = this.dateRange[1].getDate();
      this.options = {
          floor: 0,
          step:1,
          stepsArray: this.dateRange.map((date: Date) => {
            return { value: date.getTime() };
          }),
        noSwitching: true,
        translate: (value: number): string => {
          return (new Date(new Date().setDate(new Date(value).getDate()))).toString().substring(4, 16)
        },
        animate: false,
        vertical: true
      };
      let day = new Date().getDate()
      this.sliderForm = new FormGroup({
        sliderControl: new FormControl([this.dateRange[day-5], this.dateRange[day+5]])
      });
      this.tweetsDataSource.paginator = this.tweetsPaginator;
      this.tweetsDataSource.paginator.pageIndex = 0;
      
      this.dateRangeArticles = this.createDateRange();
      this.valueArticles = this.dateRange[0].getDate();
      this.maxValueArticles = this.dateRange[1].getDate();
      this.optionsArticles = {
          floor: 0,
          step:1,
          stepsArray: this.dateRangeArticles.map((date: Date) => {
            return { value: date.getTime() };
          }),
        noSwitching: true,
        translate: (value: number): string => {
          return (new Date(new Date().setDate(new Date(value).getDate()))).toString().substring(4, 16)
        },
        animate: false,
        vertical: true
      };
      this.sliderFormArticles = new FormGroup({
        sliderControlArticles: new FormControl([this.dateRangeArticles[day-5], this.dateRangeArticles[day+5]])
      });
      


          const currentRoute = this.router.routerState;
          this.router.navigateByUrl(currentRoute.snapshot.url, { skipLocationChange: true });
          this.pieChart = undefined
          ReviewsComponent.pieChartLoaded = false
          this.activatedRoute.params.subscribe(s => {
            this.crypto = s["crypto"];
            this.reviewsService.getPieStatsByCryptocurrency(this.crypto).pipe(delay(1150)).subscribe(res => {
              this.pieChart = res["data"]
              ReviewsComponent.pieChartLoaded = true
              
            });
          });
        }
      });
      
    }
    
    sliderForm : FormGroup
    dateRange: Date[];
    value: number;
    maxValue: number;
    options: Options;
    pipe = new DatePipe('en');
    sliderFormArticles : FormGroup
    dateRangeArticles: Date[];
    valueArticles: number;
    maxValueArticles: number;
    optionsArticles: Options;
    title = ""

    linkClick(id) {
      console.log(id)
      console.log(this.articlesDataSource)
      let data = this.articlesDataSource
      for(let i = 0; i < data.filteredData.length; i++) {
        if(data.filteredData[i].id == id)
          data.filteredData[i].visits = data.filteredData[i].visits+1
      }
      this.articlesDataSource = data
      this.articlesDataSource = new MatTableDataSource<Article>(data.filteredData);
      this.articlesDataSource.paginator = this.articlesPaginator;
      this.articlesDataSource.sort = this.sortArticles;
    }

    createDateRange(): Date[] {
      const dates: Date[] = [];
      let nbDays = (new Date(new Date().getUTCFullYear(), new Date().getUTCMonth(), 0)).getDate()
      for (let i: number = 1; i <= nbDays; i++) {
        dates.push(new Date(new Date().getUTCFullYear(), new Date().getUTCMonth(), i));
      }
      return dates;
    }
  

  valueChange($event): void {
    this.tweetsDataSource.filter = ''+Math.random();
    this.tweetsDataSource.filterPredicate = (data:Tweet, filter:string) => {
      //console.log("Created at :"+new Date(data.created_at).getTime()+" -> "+new Date(data.created_at))
      //console.log("date 1 : "+this.sliderForm.value.sliderControl[0]+" -> "+new Date(this.sliderForm.value.sliderControl[0]))
      //console.log("date 2 : "+this.sliderForm.value.sliderControl[1]+" -> "+new Date(new Date().setTime(new Date(this.sliderForm.value.sliderControl[1]).getTime()+(1000 * 60 * 60 * 24)-60)))
      return new Date(data.created_at).getTime() >= this.sliderForm.value.sliderControl[0]
        && new Date(data.created_at).getTime() <= new Date(new Date().setTime(new Date(this.sliderForm.value.sliderControl[1]).getTime()+(1000 * 60 * 60 * 24))).getTime();
    }
    this.tweetsLength = this.tweetsDataSource.filteredData.length;
  }

  valueChangeArticles($event): void {
    this.articlesDataSource.filter = ''+Math.random();
    this.articlesDataSource.filterPredicate = (data:Article, filter:string) => {
      return new Date(data.created_at).getTime() >= this.sliderFormArticles.value.sliderControlArticles[0]
        && new Date(data.created_at).getTime() <= new Date(new Date().setTime(new Date(this.sliderFormArticles.value.sliderControlArticles[1]).getTime()+(1000 * 60 * 60 * 24))).getTime();
    }
    this.articlesLength = this.articlesDataSource.filteredData.length;
  }


  ngOnInit() {
    this.activatedRoute.params.subscribe(s => {
      this.crypto = s["crypto"];
      
      // tweets : 
      this.tweetsService.getTweetsByCryptocurrency(this.crypto).subscribe(
        (data) => { 
          this.tweets = data['data']; 
          this.tweetsDataSource = new MatTableDataSource<Tweet>(this.tweets);
          this.tweetsDataSource.paginator = this.tweetsPaginator;
          this.tweetsDataSource.sort = this.sortTweets;
          this.tweetsLength = this.tweets.length;
          this.valueChange(undefined)
          this.valueChange(undefined)
        },
        (error) => { console.log(error); }
      );
      // articles : 
      this.articlesService.getArticlesByCryptocurrency(this.crypto).subscribe(
        (data) => { 
          this.articles = data['data']; 
          this.articlesDataSource = new MatTableDataSource<Article>(this.articles);
          this.articlesDataSource.paginator = this.articlesPaginator;
          this.articlesDataSource.sort = this.sortArticles;
          this.articlesLength = this.articles.length;
          this.cryptocurrencyName = data['data'][0].cryptocurrency;
          this.title = "Positive and Negative reviews percentage for "+this.cryptocurrencyName
          console.log(data['data'][0])
          this.valueChangeArticles(undefined)
          this.valueChangeArticles(undefined)
        },
        (error) => { console.log(error); }
      );
      
    });
  }


}

