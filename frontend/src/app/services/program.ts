import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class Program {
  private apiUrl = 'http://127.0.0.1:5000/api/programs';

  constructor(private http: HttpClient) {}

  private getHeaders() {
    const token = localStorage.getItem('token');

    return {
      headers: new HttpHeaders({
        Authorization: `Bearer ${token}`
      })
    };
  }

  getPrograms(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/`, this.getHeaders());
  }

  createProgram(data: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/`, data, this.getHeaders());
  }

  updateProgram(id: number, data: any): Observable<any> {
    return this.http.put(`${this.apiUrl}/${id}`, data, this.getHeaders());
  }

  cancelProgram(id: number): Observable<any> {
    return this.http.put(`${this.apiUrl}/${id}/cancel`, {}, this.getHeaders());
  }

  deleteProgram(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/${id}`, this.getHeaders());
  }

  assignFaculty(programId: number, facultyId: number): Observable<any> {
    return this.http.post(
      `${this.apiUrl}/${programId}/faculty/${facultyId}`,
      {},
      this.getHeaders()
    );
  }

  getCourses(): Observable<any[]> {
    return this.http.get<any[]>(
      'http://127.0.0.1:5000/api/courses/',
      this.getHeaders()
    );
  }

  getCoordinators(): Observable<any[]> {
    return this.http.get<any[]>(
      'http://127.0.0.1:5000/api/users/?role=COORDINATOR',
      this.getHeaders()
    );
  }

  getFaculties(): Observable<any[]> {
    return this.http.get<any[]>(
      'http://127.0.0.1:5000/api/faculties/',
      this.getHeaders()
    );
  }
}