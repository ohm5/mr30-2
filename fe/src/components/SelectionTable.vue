<script setup lang="ts">
</script>

<script lang="ts">
export default {
    props: {
        entries: {
            type: Array<CourseEntry>,
            default: [],
        },
        actionButtonText: {
            type: String,
            default: "",
        }
    },
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
        tr(v-for="entry in entries")
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
</style>