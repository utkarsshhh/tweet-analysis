import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
@Injectable({
  providedIn: 'root'
})
export class HashtagService {
  submitHashtag(hashtag:any){
    return this.http.post('http://127.0.0.1:5000/get_tweets',hashtag)
  }

  constructor(private http: HttpClient) { }
}
