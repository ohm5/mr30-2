<script setup lang="ts">
import TheWelcome from './components/TheWelcome.vue'
</script>

<script lang="ts">
export default {
  data() {
    return {
      queryText: "",
      results: [],
      bucket: [],
    }
  },
  methods: {
    fetchResult: function () {
      const q = this.queryText
      fetch(`http://localhost:5000/sugg?q=${q}`)
        .then(resp => resp.json())
        .then(data => {
          this.results = data.results
        })
    },
    selectCourse: function (course: any) {
      const found = this.bucket.findIndex(x => x.course_num == course.course_num) >= 0
      if(!found) {
        this.bucket.push(course);
      }
    },
    deselectCourse: function (course_num: any) {
      const ix = this.bucket.findIndex(x => x.course_num == course_num)
      this.bucket.splice(ix, 1)
    }
  }
}
</script>

<template>
  <main>
    <section>
      <h3>ค้นหา</h3>
      <input id="q" v-model="queryText" type="text" v-on:keyup.enter="fetchResult" />
      <button v-on:click="fetchResult">search</button>

      <div class="tableContainer">
        <table id="resultTable">
          <thead>
            <tr>
              <th>วิชา</th>
              <th>หน่วยกิต</th>
              <th>วันเวลาเรียน</th>
              <th>วันเวลาสอบ</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="entry in results">
              <td>{{ entry.course_num }}</td>
              <td>{{ entry.credit }}</td>
              <td>{{ entry.course_t_start }} - {{ entry.course_t_end }}</td>
              <td>{{ entry.exam_d }} {{ entry.exam_t }}</td>
              <td>
                <button v-on:click="selectCourse(entry)">+</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
    <section>
      <div class="tableContainer">
        <h3>วิชาที่เลือก</h3>
        <table id="resultTable">
          <thead>
            <tr>
              <th>วิชา</th>
              <th>หน่วยกิต</th>
              <th>วันเวลาเรียน</th>
              <th>วันเวลาสอบ</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="entry in bucket" :key="entry.course_num">
              <td>{{ entry.course_num }}</td>
              <td>{{ entry.credit }}</td>
              <td>{{ entry.course_t_start }} - {{ entry.course_t_end }}</td>
              <td>{{ entry.exam_d }} {{ entry.exam_t }}</td>
              <td>
                <button v-on:click="deselectCourse(entry.course_num)">x</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
  </main>
</template>

<style scoped>
section {
  margin: 0 20px;
}
.tableContainer {
  max-height: 300px;
  overflow: auto;
  margin: 20px 0;
}

table {
  border-collapse: collapse;
  max-height: 200px;
}

/* Zebra striping */
tr:nth-of-type(odd) {
  background: #eee;
  border: 1px solid #ccc;
}

th {
  background: #3498db;
  color: white;
  font-weight: bold;
}

td,
th {
  padding: 10px;
  text-align: left;
}
</style>
