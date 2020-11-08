import { Component, OnInit } from '@angular/core';
import { VoiceRecognitionService } from '../services/VoiceRecognition/voice-recognition.service'

@Component({
  selector: 'app-speech-to-text',
  templateUrl: './speech-to-text.component.html',
  styleUrls: ['./speech-to-text.component.scss'],
  providers: [VoiceRecognitionService]
})
export class SpeechToTextComponent implements OnInit {

  constructor(public service: VoiceRecognitionService) {
    this.service.init()
  }

  ngOnInit(): void {
  }

  startService() {
    this.service.start()
  }

  stopService() {
    this.service.stop()
  }

}
