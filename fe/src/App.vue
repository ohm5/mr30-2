<script lang="ts">
import TimeTable from './components/TimeTable.vue'
import 'vue-cal/dist/vuecal.css'
import SelectionTable from './components/SelectionTable.vue';
export default {
    data(): AppData {
        return {
            q: '',
            results: [],
            bucket: [],
        };
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
    components: { SelectionTable, TimeTable }
}
</script>

<template lang="pug">
main
  section
    h3 ค้นหา
    input("v-model"='q',type='text',"v-on:keyup.enter"='fetchResult')

    button("v-on:click"='fetchResult') ค้นหา
    .tableContainer
      SelectionTable(:entries='results' action-button-text='+' @action-button-clicked='selectCourse')

  section
    h3 วิชาที่เลือก
    .tableContainer
      SelectionTable(:entries='bucket' action-button-text='x' @action-button-clicked='deselectCourse')

  section
    TimeTable(:items='bucket')

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

</style>
