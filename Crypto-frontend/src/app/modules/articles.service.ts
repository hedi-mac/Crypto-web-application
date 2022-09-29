import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ArticlesService {

  url:string = environment.APIEndpoint+"/api/v1/articles";

  constructor(private http:HttpClient) { }

  getArticlesByCryptocurrency(crypto) {
    return this.http.get(this.url+"?crypto="+crypto);
  }


}
