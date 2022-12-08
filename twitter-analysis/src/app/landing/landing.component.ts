import { Component, OnInit } from '@angular/core';
import { HashtagService } from '../hashtag.service';

@Component({
  selector: 'app-landing',
  templateUrl: './landing.component.html',
  styleUrls: ['./landing.component.css']
})
export class LandingComponent implements OnInit {

  constructor(private service:HashtagService) { }
  hashtag:string = '';
  ngOnInit(): void {
  }
  searchTag(event: Event){
    event.preventDefault();
    console.log(this.hashtag)
    this.service.submitHashtag({"hashtag":this.hashtag}).subscribe((res)=>{
      console.log(res)
    },(err)=>{
      console.log("Search Failed. Try Again")
    })
  }
  hello(){
    console.log("hello")
  }

}
