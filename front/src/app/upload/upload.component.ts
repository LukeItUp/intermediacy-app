import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';


@Component({
  selector: 'app-upload',
  templateUrl: './upload.component.html',
  styleUrls: ['./upload.component.css']
})
export class UploadComponent implements OnInit {

  public receivedFile: any;
  private url = 'http://0.0.0.0:5000/task';

  constructor(
    private http: HttpClient,
    private router: Router
  ) { }

  ngOnInit(): void {
  }

  onSubmit(event:any) {
    let task_name:string = event.target[0].value;
    let file:File = event.target[1].files[0];
    let source:string = event.target[2].value;
    let target:string = event.target[3].value;
    let formData:FormData = new FormData();
    formData.append('file', file, file.name);
    formData.append('task_name', task_name);
    formData.append('source', source);
    formData.append('target', target);
    let headers = new Headers();
    headers.append('Content-Type', 'multipart/form-data');
    headers.append('Accept', 'application/json');
    let options:any = {headers: headers};
    this.http.post(this.url, formData, options).subscribe(
      //@ts-ignore
      data => this.router.navigate(['/task', data.task.task_id])
      )    
  }

}
