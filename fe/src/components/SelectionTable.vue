<script lang="ts">
const undefinedExamDate = "1970-01-01 00:00:00"

export default {
    props: {
        entries: {
            type: Array<CourseEntry>,
            default: [],
        },
        actionButtonText: {
            type: String,
            default: "",
        },
        examOverlappingClassName: {
          type: String,
          default: "",
        }
    },
    computed: {
        overlappingCourses() {
            const acc: Map<string, CourseEntry[]> = new Map()
            const dtToCourses = this.entries.filter(x => x.exam_d != undefinedExamDate)
                .reduce((acc, z) => { // reduce to Map of date+time -> course[]
                    const key = `${z.exam_d}-${z.exam_t}`
                    const val = acc.get(key) || []
                    val.push(z)
                    acc.set(key, val)
                    return acc
                }, acc)
            
            // date+time that has overlapping course
            return [...dtToCourses.values()].filter(x => x.length > 1)
        },
        overlappingCourseNames() {
            return Array.prototype.concat(...this.overlappingCourses).map(x => x.course_num)
        },
    },
    methods: {
      courseClassName(course_num: string) {
          var classes: any = {}
          classes[this.examOverlappingClassName] = this.overlappingCourseNames.includes(course_num)
          return classes
      }
    }
}
</script>

<template lang="pug">
table#resultTable
    thead
        tr
            th วิชา
            th หน่วยกิต
            th วันเวลาเรียน
            th วันเวลาสอบ
            th
    tbody
        tr(v-for="entry in entries" ":class"="courseClassName(entry.course_num)")
            td {{ entry.course_num }}
            td {{ entry.credit }}
            td {{ entry.course_d }} {{ entry.course_t_start }} - {{ entry.course_t_end }}
            td {{ entry.exam_d.split(' ')[0] }} {{ entry.exam_t }}
            td
                button(@click="$emit('action-button-clicked', entry)") {{ actionButtonText }}
</template>

<style scoped>
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

tr.exam-overlapping {
    background-color: #F26800;
    color: white;
}
</style>