import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { UploadComponent } from './upload/upload.component';
import { TaskComponent } from './task/task.component';

const routes: Routes = [
  {path: 'upload', component: UploadComponent},
  {path: 'task/:task_id', component: TaskComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
export const routingComponents = [UploadComponent, TaskComponent];