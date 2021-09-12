import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-list',
  templateUrl: './list.component.html',
  styleUrls: ['./list.component.css']
})
export class ListComponent implements OnInit {

  public tasks = ["14ZVV2JQ", "ASDF2"]

  constructor(
    private router: Router
  ) { }

  ngOnInit(): void {
    // TODO: LOAD FROM COOKIES
  }

  goToTask(id: string) {
    this.router.navigate(['/task', id]);
  }
}
