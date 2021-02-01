import { Component, OnInit } from '@angular/core';
import { VoiceRecognitionService } from '../services/VoiceRecognition/voice-recognition.service'
import { Howl } from 'howler';

@Component({
  selector: 'app-speech-to-text',
  templateUrl: './speech-to-text.component.html',
  styleUrls: ['./speech-to-text.component.scss'],
  providers: [VoiceRecognitionService]
})
export class SpeechToTextComponent implements OnInit {

  recording = false;

  constructor(public service: VoiceRecognitionService) {
    this.service.init()
  }

  ngOnInit(): void {
  }

  startService() {
    if (!this.recording){ 
      this.service.start(); 
      this.recording = true; 
    }
  }

  getBestPath() {
    this.recording = false;
    this.service.getBestPath();
  }

}
