import { Injectable } from '@angular/core';
import { PathfinderService } from '../api/pathfinder.service';
import { HttpClient } from '@angular/common/http';

declare var webkitSpeechRecognition: any;

@Injectable({
  providedIn: 'root'
})
export class VoiceRecognitionService {

  pathFinderAPI = new PathfinderService(this.httpClient);

  recognition = new webkitSpeechRecognition();
  isStoppedSpeechRecog = false;
  public showRequest = "";
  tempWords = "";
  bestPath: string[];

  constructor(private httpClient: HttpClient) { }

  init() {

    this.recognition.interimResults = true;
    this.recognition.lang = 'fr-FR';

    this.recognition.addEventListener('result', (e) => {
      const transcript = Array.from(e.results)
        .map((result) => result[0])
        .map((result) => result.transcript)
        .join('');
      this.tempWords = transcript;
      console.log(transcript);
    });
  }

  start() {
    this.showRequest = "";
    this.isStoppedSpeechRecog = false;
    this.recognition.start();
    console.log("Speech recognition started");

    setTimeout(() => {
      if (this.tempWords.length === 0) {
        this.stop();
      }
    }, 2500);

    this.recognition.addEventListener('end', (condition) => {
      if (this.isStoppedSpeechRecog) {
        this.recognition.stop();
        console.log("End speech recognition")
      } else {
        this.wordConcat();
        this.recognition.start();
      }
    });
  }

  stop() {
    this.isStoppedSpeechRecog = true;
    this.wordConcat()
    this.recognition.stop();
    console.log("End speech recognition")

    if (this.showRequest.length > 0)
      this.pathFinderAPI.getBestPath(this.showRequest).subscribe(res => {
        this.bestPath = res;
        console.log(res)
      });
  }

  wordConcat() {
    if (this.tempWords.length > 0) {
      this.showRequest = this.showRequest + ' ' + this.tempWords;
    }

    this.tempWords = '';
  }
}