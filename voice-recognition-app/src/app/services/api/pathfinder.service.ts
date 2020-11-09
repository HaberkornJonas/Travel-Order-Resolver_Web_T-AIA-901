import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class PathfinderService {

  readonly ROOT_URL = 'http://localhost:5000/api/v1/getBestPath?phrase=';

  constructor(private http: HttpClient) { }

  getBestPath(request: string): Observable<string[]> {
    request.trim();
    return this.http.get<string[]>(this.ROOT_URL + request);
  }

}
