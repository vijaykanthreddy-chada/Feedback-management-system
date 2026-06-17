import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class Attendance {
  private apiUrl = 'http://127.0.0.1:5000/api/attendance';

  constructor(private http: HttpClient) {}

  private getHeaders() {
    const token = localStorage.getItem('token');

    return {
      headers: new HttpHeaders({
        Authorization: `Bearer ${token}`
      })
    };
  }

  getAttendance(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/`, this.getHeaders());
  }

  markAttendance(data: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/`, data, this.getHeaders());
  }

  getEnrollments(): Observable<any[]> {
    return this.http.get<any[]>(
      'http://127.0.0.1:5000/api/enrollments/',
      this.getHeaders()
    );
  }
}