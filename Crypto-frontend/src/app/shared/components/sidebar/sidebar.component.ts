import { Component, OnInit, ViewChild } from '@angular/core';
import { MatSidenav } from '@angular/material';
import { Router } from '@angular/router';
import { CryptocurrenciesService } from 'src/app/modules/cryptocurrencies.service';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-sidebar',
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.scss']
})
export class SidebarComponent implements OnInit {

  @ViewChild('sidenav', { static: true }) sidenav: MatSidenav;
  cryptocurrencies
  iconUrl = environment.CRYPTOIcon

  constructor(private cryptocurrenciesService:CryptocurrenciesService, private router:Router) {
    router.events.forEach((event) => {
      
    });
  }

  ngOnInit() {
    this.cryptocurrenciesService.getCryptocurrencies().subscribe(
      (data) => { this.cryptocurrencies = data['data'] },
      (error) => { console.log(error); }
    );
  }



}
