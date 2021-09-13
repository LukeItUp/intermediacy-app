import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-list',
  templateUrl: './list.component.html',
  styleUrls: ['./list.component.css']
})
export class ListComponent implements OnInit {

  public tasks: string[] = ["14ZVV2JQ", "ASDF2"]

  constructor(
    private router: Router
  ) { }

  ngOnInit(): void {
    console.log("cookies", document.cookie);
    // TODO: LOAD FROM COOKIES
    
    this.tasks = this.getCookieTaskList();
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

  goToTask(id: string) {
    this.router.navigate(['/task', id]);
    this.ngOnInit();
  }
}
