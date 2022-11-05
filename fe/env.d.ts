/// <reference types="vite/client" />

interface CourseEntry {
  course_num: string;
  credit: string;
  course_d: string;
  course_t_start: string;
  course_t_end: string;
  exam_d: string;
  exam_t: string;
}

interface AppData {
  q: string;
  results: Array<CourseEntry>;
  bucket: Array<CourseEntry>;
}
