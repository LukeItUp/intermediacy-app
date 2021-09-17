import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-task',
  templateUrl: './task.component.html',
  styleUrls: ['./task.component.css']
})
export class TaskComponent implements OnInit {

  public task_id = '-1';
  public task_name = 'My task'
  public task_ready = false;
  public source:any;
  public target:any;
  public results:any[] = [];

  constructor(
    private http: HttpClient,
    private route: ActivatedRoute
  ) {
    this.route.params.subscribe(routeParams => {
      this.task_id = '-1';
      this.task_name = 'My task'
      this.task_ready = false;
      this.source;
      this.target;
      this.results = [];
      
      if (this.results.length == 0) {
        this.fetchData(routeParams.task_id);
      }

    });
   }

  ngOnInit(): void {
  }

  public getCookieTaskList(): string[] {
    let ca: Array<string> = decodeURIComponent(document.cookie).split(';');
    let cookieName = `task_list=`
    for (let i=0; i < ca.length; i+=1) {
      let c = ca[i].replace(/^\s+/g, '');
      if (c.indexOf(cookieName) === 0) {
          return c.substring(cookieName.length, c.length).split('&');
      }
    }
    return [];
  }


  public addTaskToCookie(task:string) {
    var task_list: string[] = this.getCookieTaskList();
    if (!task_list.includes(task)) {
      task_list.push(task);
    }
    document.cookie=`task_list=${task_list.join("&")};SameSite=None`;
  }

  fetchData(task_id: string) {
    this.http.get<any>('http://0.0.0.0:5000/task/' + task_id).subscribe(data => {
      this.parseTask(data.task);
    })
  }

  prepareResult(result: any) {
    let out = {
      "title": result.data.title,
      "year": result.data.year,
      "intermediacy": result.intermediacy,
      "error": result.error,
      "url": "https://academic.microsoft.com/paper/" + result.data.ms_id
    };
    return out;
  }

  parseTask(task: any){
    this.task_id = task.task_id;
    this.task_name = task.task_name;
    if (task.status === 'done') {
      
      // source
      this.source = this.prepareResult(task.results.source);
      // target
      this.target = this.prepareResult(task.results.target);
      // results
      for (let result1 of task.results.results) {
        this.results.push(this.prepareResult(result1));
      }
      
      //
      this.task_ready = true;
      

      this.addTaskToCookie(`${this.task_id}\$${this.task_name}`);
      

    }
  }
}
