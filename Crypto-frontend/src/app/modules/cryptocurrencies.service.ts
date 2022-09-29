import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class CryptocurrenciesService {

  url:string = environment.APIEndpoint+"/api/v1/cryptocurrencies";

  constructor(private http:HttpClient) { }

  getCryptocurrencies() {
    return this.http.get(this.url+"?per_page=8");
  }


}
