import { Component, OnInit, Input, OnChanges, SimpleChanges } from '@angular/core';
import { Chart } from 'chart.js/auto';
@Component({
  selector: 'app-linechart',
  templateUrl: './linechart.component.html',
  styleUrls: ['./linechart.component.css']
})
export class LinechartComponent implements OnChanges {

  constructor() { }

  @Input() label:string[] = [];
  @Input() data:any[] = []
  chart:any;
  createChart(){
  
    this.chart = new Chart("Mychart", {
      type: 'line', //this denotes tha type of chart

      data: {// values on X-Axis
        labels: this.label, 
	       datasets: [
          {
            label: "Average Sentiment",
            data: this.data,
            backgroundColor: 'red'
          }
          // ,
          // {
          //   label: "Profit",
          //   data: ['542', '542', '536', '327', '17',
					// 				 '0.00', '538', '541'],
          //   backgroundColor: 'limegreen'
          // }  
        ]
      },
      options: {
        aspectRatio:3
      }
      
    });
  }

  ngOnChanges(changes: SimpleChanges): void {
    console.log(this.label)
    console.log(this.data)
    if(changes['label']){
      console.log(this.label)
      console.log(this.data)
    }
    this.createChart()
  }

}
