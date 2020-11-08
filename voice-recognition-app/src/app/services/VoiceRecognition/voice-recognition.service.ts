import { Injectable } from '@angular/core';

declare var webkitSpeechRecognition: any;

@Injectable({
  providedIn: 'root'
})
export class VoiceRecognitionService {

  recognition = new webkitSpeechRecognition();
  isStoppedSpeechRecog = false;
  public text = "";
  public showRequest = "";
  tempWords = "";

  constructor() { }

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

    console.log(this.text.length);
    setTimeout(() => {
      this.wordConcat();
      if (this.text.length === 0) {
        this.stop();
      }
    }, 3000);

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
    this.showRequest = this.text;
    this.isStoppedSpeechRecog = true;
    this.wordConcat()
    this.recognition.stop();
    console.log("End speech recognition")
    this.text = "";
  }

  wordConcat() {
    if (this.tempWords.length > 0) {
      this.text = this.text + ' ' + this.tempWords;
    }
    this.tempWords = '';
  }



}
