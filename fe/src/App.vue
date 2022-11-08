<script lang="ts">
import 'vue-cal/dist/vuecal.css'
import TimeTable from './components/TimeTable.vue'
import ExamSchedule from './components/ExamSchedule.vue'
import SelectionTable from './components/SelectionTable.vue';
export default {
    data(): AppData {
        return {
            q: '',
            results: [],
            bucket: [],
        };
    },
    computed: {
        somethingSelected() {
            return this.bucket.length > 0
        }
    },
    methods: {
        fetchResult() {
            fetch(`sugg?q=${this.q}`)
                .then(resp => resp.json())
                .then(data => {
                    const json_results: Array<CourseEntry> = data.results;
                    this.results = json_results;
                });
        },
        selectCourse(course: CourseEntry) {
            const found = this.bucket.findIndex(x => x.course_num == course.course_num) >= 0;
            if (!found) {
                this.bucket.push(course);
            }
        },
        deselectCourse(course: CourseEntry) {
            const ix = this.bucket.findIndex(x => x.course_num == course.course_num);
            this.bucket.splice(ix, 1);
        },
    },
    components: { SelectionTable, TimeTable, ExamSchedule }
}
</script>

<template lang="pug">
main
    section
        div มร.30 ส่วนกลาง 2/2565
        div(style="color: red") ไม่ได้ตรวจสอบ อาจสูญหาย,ไม่ถูกต้อง ตรวจสอบกับของจริงด้วยนะ

        h3 ค้นหา
        input("v-model"='q',type='text',"v-on:keyup.enter"='fetchResult')

        button("v-on:click"='fetchResult') ค้นหา
        .tableContainer
            SelectionTable(:entries='results' action-button-text='+' @action-button-clicked='selectCourse')

    section
        h3 วิชาที่เลือก
        .tableContainer
            SelectionTable(:entries='bucket' action-button-text='x' @action-button-clicked='deselectCourse', exam-overlapping-class-name='exam-overlapping')

    section(v-if="somethingSelected")
        h3 ตารางสอบ
        ExamSchedule(:items='bucket')

    section(v-if="somethingSelected")
        h3 ตารางเรียน
        TimeTable(:items='bucket')

    section
        a(href="https://github.com/ohm5/mr30-2") Github
</template>

<style scoped>

h3 {
    margin-top: 12px;
    border-top: 1px solid black;
}

section {
    margin: 0 20px;
}

.tableContainer {
    max-height: 300px;
    overflow: auto;
    margin: 20px 0;
}
</style>
