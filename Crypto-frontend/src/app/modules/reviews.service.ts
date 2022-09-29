import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ReviewsService {

  url:string = environment.APIEndpoint+"/api/v1/reviews";

  constructor(private http:HttpClient) { }

  getPieStatsByCryptocurrency(crypto) {
    return this.http.get(this.url+"/pie-stats/"+crypto);
  }

  getBarStats(days) {
    return this.http.get(this.url+"/bar-stats?days="+days);
  }

  getEvolutionStatsByCryptocurrency(crypto) {
    return this.http.get(this.url+"/evolution-stats/"+crypto);
  }

  getEvolutionStats(duration, type) {
    return this.http.get(this.url+"/evolution-stats?days="+duration+"&type="+type);
  }

}
