import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {

  ngOnInit() {
    if(!(JSON.parse(localStorage.getItem('selectedall'))))
      localStorage.setItem('selectedall', JSON.stringify([0, 1]));
    if(!(JSON.parse(localStorage.getItem('selectedtweets'))))
      localStorage.setItem('selectedtweets', JSON.stringify([0, 1]));
    if(!(JSON.parse(localStorage.getItem('selectedarticles'))))
      localStorage.setItem('selectedarticles', JSON.stringify([0, 1]));
    
  }

}
