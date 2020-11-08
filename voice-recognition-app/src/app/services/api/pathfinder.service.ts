import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class PathfinderService {

  readonly ROOT_URL = 'https://http://localhost:5000/api/v1/getBestPath?phrase=';

  bestPath: any;

  constructor(private http: HttpClient) { }

  getBestPath(request: string) {
    return this.bestPath = this.http.get(this.ROOT_URL + request);
  }

}
