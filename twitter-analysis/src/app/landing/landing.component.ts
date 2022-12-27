import { Component, OnInit } from '@angular/core';
// import { flatMap } from 'rxjs';
import { HashtagService } from '../hashtag.service';

@Component({
  selector: 'app-landing',
  templateUrl: './landing.component.html',
  styleUrls: ['./landing.component.css']
})
export class LandingComponent implements OnInit {

  constructor(private service:HashtagService) { }
  hashtag:string = '';
  labels:string[] = [];
  pieLabels:any[] = []
  pieCounts:any[] = []
  sentimentLabels:any[] = []
  sentiments:any[] = []
  counts = [];
  resp:any;
  isSearched:boolean = false
  sentiment:string = ''
  ngOnInit(): void {
    
  }
  searchTag(event: Event){
    event.preventDefault();
    console.log(this.hashtag)
    this.service.submitHashtag({"hashtag":this.hashtag}).subscribe((res)=>{
      console.log(JSON.stringify(res))

      this.resp= res
      // console.log(this.resp["labels"])
      // console.log(this.resp['labels'])
      this.labels = this.resp['labels']
      this.counts = this.resp['counts']
      this.sentiment = this.resp['sentiment']
      this.pieLabels = this.resp['pieLabels']
      this.sentimentLabels = this.resp['sentimentLabels']
      this.sentiments = this.resp['sentiments']

      for(let i =0;i<this.pieLabels.length;i++){
        if (this.pieLabels[i]==1.0){
          this.pieLabels[i] = "Posititve"
        }
        else if (this.pieLabels[i]==0.0){
          this.pieLabels[i] = 'Neutral'
        }
        else{
          this.pieLabels[i] = 'Negative'

        }

      }
      this.pieCounts = this.resp['pieCounts']

      this.isSearched = true
      // console.log(this.labels,"   31")

    },(err)=>{
      console.log("Search Failed. Try Again")
      this.isSearched = false
    })
  }
  hello(){
    console.log("hello")
  }

}
