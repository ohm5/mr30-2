<script lang="ts">

// @ts-ignore
import VueCal from 'vue-cal'
import 'vue-cal/dist/vuecal.css'

const dates: Record<string, string> = {
    "M": "2000-01-03", // some arbitrary date that is a monday (we just needed some date)
    "TU": "2000-01-04",
    "W": "2000-01-05",
    "TH": "2000-01-06",
    "F": "2000-01-07",
    "S": "2000-01-08",
    "SUN": "2000-01-09",
}

export default {
    components: { VueCal },
    props: {
        items: {
            type: Array<CourseEntry>,
            default: [],
        }
    },
    computed: {
        events() {
            var xs = this.items.map((x: CourseEntry) => {
                return {
                    start: `${dates[x.course_d]} ${x.course_t_start}`,
                    end: `${dates[x.course_d]} ${x.course_t_end}`,
                    title: x.course_num,
                }
            })
            console.log(xs)
            return xs
        },
        timeFrom() {
            const xs = this.items.map(x => parseInt(x.course_t_start.slice(0, 2)))
            console.log(xs)
            return Math.min(...xs) * 60
        },
        timeTo() {
            const xs = this.items.map(x => parseInt(x.course_t_end.slice(0, 2)))
            console.log(xs)
            return (Math.max(...xs) + 1) * 60
        }
    },
}

</script>

<template lang="pug">
.calendarContainer
    vue-cal(
        ":time-from"="timeFrom"
        ":time-to"="timeTo"
        ":events"="events"
        selected-date="2000-01-03"
        hideViewSelector
        hideTitleBar
        small
        disable-views="['years', 'year', 'month', 'day']"
    )
</template>

<style>
.calendarContainer {
    height: 800px;
}

.weekday-label > span:last-child {
    visibility: collapse;
}

.vuecal__event {
    background-color: #3498db;
    border: 1px solid #ffffff;
    color: white;
}
</style>