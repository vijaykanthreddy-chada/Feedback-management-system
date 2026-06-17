import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class Report {
  private apiUrl = 'http://127.0.0.1:5000/api/reports';

  constructor(private http: HttpClient) {}

  private getHeaders() {
    const token = localStorage.getItem('token');

    return {
      headers: new HttpHeaders({
        Authorization: `Bearer ${token}`
      })
    };
  }

  getDashboardSummary(): Observable<any> {
    return this.http.get(`${this.apiUrl}/dashboard`, this.getHeaders());
  }

  getEnrollmentReport(programId: number): Observable<any> {
    return this.http.get(
      `${this.apiUrl}/programs/${programId}/enrollments`,
      this.getHeaders()
    );
  }

  getAttendanceReport(programId: number): Observable<any> {
    return this.http.get(
      `${this.apiUrl}/programs/${programId}/attendance`,
      this.getHeaders()
    );
  }

  getFacultyPerformance(facultyId: number): Observable<any> {
    return this.http.get(
      `${this.apiUrl}/faculty/${facultyId}/performance`,
      this.getHeaders()
    );
  }

  getProgramSummary(programId: number): Observable<any> {
    return this.http.get(
      `${this.apiUrl}/program/${programId}/summary`,
      this.getHeaders()
    );
  }

  getDefaulters(programId: number): Observable<any> {
    return this.http.get(
      `${this.apiUrl}/defaulters/${programId}`,
      this.getHeaders()
    );
  }

  downloadCsv(programId: number): Observable<any> {
    return this.http.get(
      `${this.apiUrl}/program/${programId}/summary?format=csv`,
      {
        ...this.getHeaders(),
        responseType: 'blob'
      }
    );
  }
}