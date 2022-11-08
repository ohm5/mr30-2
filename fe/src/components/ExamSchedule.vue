<script lang="ts">

// @ts-ignore
import VueCal from 'vue-cal'
import 'vue-cal/dist/vuecal.css'

const letterToTime = {
    "A": {start: "09:00", end: "12:00"},
    "B": {start: "14:00", end: "16:30"},
    "C": {start: "17:00", end: "19:00"},
}

const undefinedExamDate = "1970-01-01 00:00:00"

export default {
    components: { VueCal },
    props: {
        items: {
            type: Array<CourseEntry>,
            default: [],
        }
    },
    computed: {
        coursesByExamDate() {
            var undefinedDateCourses = this.items.filter(x => x.exam_d == undefinedExamDate)
            var definedDateCourses  = this.items.filter(x => x.exam_d != undefinedExamDate)

            return {
                undefined: undefinedDateCourses, // คณะจัดสอบเอง
                defined: definedDateCourses,
            }
        },
        definedExamDates() {
            return this.coursesByExamDate.defined.map(x => new Date(x.exam_d))
        },
        monthsToShow() {
            const allDates = this.definedExamDates.map(x =>
                new Date(x.getFullYear(), x.getMonth() + 1, 1).toISOString().split("T")[0] // get the date part only
            )
            // first date of months to show
            const xs = [...new Set(allDates)].sort() // distinct + sort
            return xs
        },
        events() {
            return this.coursesByExamDate.defined.map(x => {
                const examDate = x.exam_d.split(" ")[0] // get the date part only
                return {
                    start: `${examDate} ${letterToTime[x.exam_t].start}`,
                    end: `${examDate} ${letterToTime[x.exam_t].end}`,
                    title: x.course_num,
                }
            })
        },
    },
}

</script>


<template lang="pug">
.allCalendarContainer(v-for="firstDateOfMonth in monthsToShow")
    .calendarContainer
        vue-cal(
            ":events"="events"
            active-view="month"
            ":selected-date"="firstDateOfMonth"
            hideViewSelector
            small
            disable-views="['years', 'year', 'week', 'day']")
</template>

<style scoped>
.allCalendarContainer {
    height: 300px;
}
.calendarContainer {
    height: 300px;
}

</style>

<style>
.weekday-label > span:last-child {
    visibility: collapse;
}

.vuecal__event {
    background-color: #3498db;
    border: 1px solid #ffffff;
    color: white;
}

.vuecal--month-view .vuecal__cell--has-events {
    background-color: #3498db;
    color: white;
}
.vuecal--month-view .vuecal__cell-events-count {
    display: none;
}

</style>