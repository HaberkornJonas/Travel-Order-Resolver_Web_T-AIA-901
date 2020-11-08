import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class PathfinderService {

  readonly ROOT_URL = 'https://jsonplaceholder.typicode.com/posts/1';

  bestPath: any;

  constructor(private http: HttpClient) { }

  getBestPath() {
    return this.bestPath = this.http.get(this.ROOT_URL);
  }

}
