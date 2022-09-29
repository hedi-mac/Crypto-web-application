import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class TweetsService {

  url:string = environment.APIEndpoint+"/api/v1/tweets";

  constructor(private http:HttpClient) { }

  getTweets() {
    return this.http.get(this.url+"?per_page=20");
  }

  getTweetsByCryptocurrency(crypto) {
    return this.http.get(this.url+"?crypto="+crypto);
  }


}
