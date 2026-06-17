import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class Student {
  private apiUrl = 'http://127.0.0.1:5000/api/students';

  constructor(private http: HttpClient) {}

  private getHeaders() {
    const token = localStorage.getItem('token');

    return {
      headers: new HttpHeaders({
        Authorization: `Bearer ${token}`
      })
    };
  }

  getStudents(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/`, this.getHeaders());
  }

  createStudent(data: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/`, data, this.getHeaders());
  }

  updateStudent(id: number, data: any): Observable<any> {
    return this.http.put(`${this.apiUrl}/${id}`, data, this.getHeaders());
  }

  deleteStudent(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/${id}`, this.getHeaders());
  }

  getCourses(): Observable<any[]> {
    return this.http.get<any[]>(
      'http://127.0.0.1:5000/api/courses/',
      this.getHeaders()
    );
  }

  getParticipants(): Observable<any[]> {
    return this.http.get<any[]>(
      'http://127.0.0.1:5000/api/users/?role=PARTICIPANT',
      this.getHeaders()
    );
  }
}