import { Component, Input, OnInit,OnChanges, SimpleChanges } from '@angular/core';
import { Chart } from 'chart.js/auto';

@Component({
  selector: 'app-piechart',
  templateUrl: './piechart.component.html',
  styleUrls: ['./piechart.component.css']
})
export class PiechartComponent implements OnChanges {

  constructor() { }
  @Input() pieLabel:any[] = []
  @Input() pieData:any[] = []
  chart:any;
  arcColors = [
    "rgba(255,0,0)",
    "rgba(0,0,255)",
    "rgba(0,255,0)"
  ];

  ngOnChanges(changes: SimpleChanges): void {
    console.log(this.pieLabel)
    console.log(this.pieData)
    if(changes['pieLabel']){
      console.log(this.pieLabel)
      console.log(this.pieData)
    }
    this.createChart()
  }
  
  createChart(){
  this.chart = new Chart("myChart", {
    type: "pie",
    data: {
      labels: this.pieLabel,
      datasets: [{
        backgroundColor: this.arcColors,
        data: this.pieData
      }]
    },
    options: {
      aspectRatio:3
    }
  });
}

}
