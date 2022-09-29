import { Component, OnInit, ViewChild } from '@angular/core';
import { DashboardService } from '../dashboard.service';
import { MatTableDataSource, MatPaginator } from '@angular/material';
import { ReviewsService } from '../reviews.service';
import { environment } from 'src/environments/environment';
import { ActivatedRoute, NavigationEnd, NavigationStart, Router } from '@angular/router';
import { AreaComponent } from 'src/app/shared/widgets/area/area.component';
import { delay } from 'rxjs/operators';

@Component({
  selector: 'app-stats',
  templateUrl: './stats.component.html',
  styleUrls: ['./stats.component.scss']
})
export class StatsComponent implements OnInit {

  tab = undefined;
  tab1 = undefined;
  tab2 = undefined;
  tab3 = undefined;
  duration = undefined;
  selected
  public static dataLoaded = false

  constructor(private reviewsService:ReviewsService,
    private activatedRoute: ActivatedRoute,
    private router: Router) {
      
      
      router.events.forEach((event) => {
        
        if(event instanceof NavigationEnd) {
          this.tab = undefined;
          this.tab1 = undefined;
          this.tab2 = undefined;
          this.duration = 0;
          StatsComponent.dataLoaded = false
          
        this.activatedRoute.params.subscribe(s => {
            if(s["duration"]=='weekly') {
              this.duration = 7
              
            }
            if(s["duration"]=='monthly') {
              this.duration = 28
              
            } 
            
        });

        }
        
      });
  }

  ngOnInit() {
    const currentRoute = this.router.routerState;
    this.router.navigateByUrl(currentRoute.snapshot.url, { skipLocationChange: true }); 
    StatsComponent.dataLoaded = false


        


        
      this.activatedRoute.params.subscribe(s => {
          if(this.duration == 7) {
            this.loadWeeklyStats('all')
            this.loadWeeklyStats('tweets')
            this.loadWeeklyStats('articles')
          }
          if(this.duration == 28) {
            this.loadMonthlyStats('all')
            this.loadMonthlyStats('tweets')
            this.loadMonthlyStats('articles')
          } 
          setTimeout(function(){
            StatsComponent.dataLoaded = true 
          }, 2500);
          
      });


      


    
  }

  loadWeeklyStats(type) {
    
    let t = undefined
    this.reviewsService.getEvolutionStats(this.duration, type).subscribe((res) => {
      let selected = JSON.parse(localStorage.getItem('selected'+type));
      t = res['data'];
      for(let i = 0; i<t[0].data.length; i++) {
        t[i]['events'] = {
          legendItemClick: function ($event) {
            let index : number = +$event.target.index
            let tab = []
            let verif = true;
            for(let i = 0; i<selected.length; i++) {
              if(selected[i] != index)
                tab.push(selected[i])
              else
                verif = false
            }
            if(verif)
              tab.push(index)
            localStorage.setItem('selected'+type, JSON.stringify(tab));
            
             
          }
        }
        t[i].data.splice(i, 1, {
          y: t[i].data[i],
          marker: {
            symbol: 'url('+environment.CRYPTOIconSize+'color/'+t[i].name.toLowerCase()+'.png'+')',
            width: 24,
            height: 24
          },
        })
      }
      selected = JSON.parse(localStorage.getItem('selected'+type));
      for(let i = 0; i<t.length; i++) {
        if(selected.indexOf(i) == -1) {
          t[i].visible = false
        }
        else {
          t[i].visible = true
        }
      }
      if(type == 'all')
        this.tab = t
      else if(type == 'tweets')
        this.tab1 = t
      else
        this.tab2 = t
    }, (err) => console.log(err));
  }

  loadMonthlyStats(type) {

    let selected = JSON.parse(localStorage.getItem('selected'+type));
    let t = undefined
    this.reviewsService.getEvolutionStats(this.duration, type).subscribe((res) => {
      selected = JSON.parse(localStorage.getItem('selected'+type));
      t = res['data'];
      for(let i = 0; i<t.length; i++) {
        t[i].data.splice(t[i].data.length - i -1, 1, {
          y: t[i].data[t[i].data.length - i -1],
          marker: {
            symbol: 'url('+environment.CRYPTOIconSize+'color/'+t[i].name.toLowerCase()+'.png'+')',
            width: 24,
            height: 24
          },
        })
      }
      for(let i = 0; i<t.length; i++) {
        t[i]['events'] = {
          legendItemClick: function ($event) {
            
            let index : number = +$event.target.index
            let tab = []
            let verif = true;
            for(let i = 0; i<selected.length; i++) {
              if(selected[i] != index)
                tab.push(selected[i])
              else
                verif = false
            }
            if(verif)
              tab.push(index)
            localStorage.setItem('selected'+type, JSON.stringify(tab));
          }
        }
        if(selected.indexOf(i) == -1) {
          t[i].visible = false
        }
        else {
          t[i].visible = true
        }
      }
      if(type == 'all')
        this.tab = t
      else if(type == 'tweets')
        this.tab1 = t
      else
        this.tab2 = t

    }, (err) => console.log(err));
  }

}
