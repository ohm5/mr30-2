<script lang="ts">
import 'vue-cal/dist/vuecal.css'
import TimeTable from './components/TimeTable.vue'
import ExamSchedule from './components/ExamSchedule.vue'
import SelectionTable from './components/SelectionTable.vue';
import { getIcsStream } from './ics'

export default {
    data(): AppData {
        return {
            q: '',
            results: [],
            bucket: [],
            selectedTab: 'exam-time'
        };
    },
    mounted() {
        const storedBucket = localStorage["bucket"]
        if (storedBucket) {
            this.bucket = JSON.parse(storedBucket)
        }
    },
    computed: {
        courseSelected() {
            return this.bucket.length > 0
        },
        icsStream() {
            return `data:text/calendar,${encodeURIComponent(getIcsStream(this.bucket))}`
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
                localStorage["bucket"] = JSON.stringify(this.bucket)
            }
        },
        deselectCourse(course: CourseEntry) {
            const ix = this.bucket.findIndex(x => x.course_num == course.course_num);
            this.bucket.splice(ix, 1);
            localStorage["bucket"] = JSON.stringify(this.bucket)
        },
        tabClasses(tabName: string) {
            return {
                'active-tab': this.selectedTab == tabName,
                'inactive-tab': !(this.selectedTab == tabName),
            }
        },
        setTabActive(tabName: 'lecture-time' | 'exam-time') {
            this.selectedTab = tabName
        }
    },
    components: { SelectionTable, TimeTable, ExamSchedule }
}
</script>

<template lang="pug">
main
    section
        div มร.30 ส่วนกลาง 1/67
        div(style="color: red") ไม่ได้ตรวจสอบ อาจสูญหาย,ไม่ถูกต้อง ตรวจสอบกับของจริงด้วยนะ

        h3 ค้นหา
        input("v-model"='q',type='text',"v-on:keyup.enter"='fetchResult')

        button("v-on:click"='fetchResult') ค้นหา
        .tableContainer
            SelectionTable(:entries='results' action-button-text='+' @action-button-clicked='selectCourse')

    section(v-if="courseSelected")
        h3 วิชาที่เลือก
        .tableContainer
            SelectionTable(:entries='bucket' action-button-text='x' @action-button-clicked='deselectCourse', exam-overlapping-class-name='exam-overlapping')
            
    
    section#tab-picker-section(v-if="courseSelected")
        a(href="#/" @click="setTabActive('exam-time')")
            div(:class='tabClasses("exam-time")') ตารางสอบ
        a(href="#/" @click="setTabActive('lecture-time')")
            div(:class='tabClasses("lecture-time")') ตารางเรียน
    
    section
        div(v-if="courseSelected && selectedTab == 'exam-time'")
            a(v-bind:href="icsStream" download='ram_exam.ics')
                div ดาวน์โหลด ICS
            ExamSchedule(:items='bucket')

    section
        div(v-if="courseSelected && selectedTab == 'lecture-time'")
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

#tab-picker-section {
    display: flex;
    flex-direction: row;
}

#tab-picker-section div {
    padding: 10px
}

#tab-picker-section a {
    text-decoration: none;
}
#tab-picker-section div.active-tab {
    font-weight: bolder;
    background-color: #3498db;
    color: white;
    border-radius: 20px 20px 0px 0px ;
}

#tab-picker-section div.inactive-tab {
    color: black;
}

</style>
