import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class Enrollment {
  private apiUrl = 'http://127.0.0.1:5000/api/enrollments';

  constructor(private http: HttpClient) {}

  private getHeaders() {
    const token = localStorage.getItem('token');

    return {
      headers: new HttpHeaders({
        Authorization: `Bearer ${token}`
      })
    };
  }

  getEnrollments(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/`, this.getHeaders());
  }

  createEnrollment(data: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/`, data, this.getHeaders());
  }

  deleteEnrollment(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/${id}`, this.getHeaders());
  }

  getStudents(): Observable<any[]> {
    return this.http.get<any[]>(
      'http://127.0.0.1:5000/api/students/',
      this.getHeaders()
    );
  }

  getPrograms(): Observable<any[]> {
    return this.http.get<any[]>(
      'http://127.0.0.1:5000/api/programs/',
      this.getHeaders()
    );
  }
}